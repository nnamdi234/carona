import asyncio
import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.pool import StaticPool

from db import get_db
from main import app
from models import Base, User, Vehicle
from utils.security import hash_password


async def run_vehicle_tests():
    print("--- 1. Setting up In-Memory SQLite Test Database ---")
    test_engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    async_session = async_sessionmaker(test_engine, expire_on_commit=False)

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Database tables created successfully!")

    async def override_get_db():
        async with async_session() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise

    app.dependency_overrides[get_db] = override_get_db

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Create a test user to be a vehicle owner
        async with async_session() as session:
            test_user = User(
                first_name="Driver",
                last_name="Dan",
                email="dan@example.com",
                phone_number="+1122334455",
                password=hash_password("driverPass123"),
                role="driver"
            )
            session.add(test_user)
            await session.commit()
            user_id = str(test_user.id)

        print("\n--- 2. Testing Create Vehicle (POST /vehicles) ---")
        vehicle_payload = {
            "make": "Toyota",
            "model": "Camry",
            "colour": "Silver",
            "capacity": 4,
            "plate_number": "LAG-123-XY",
            "owner_id": user_id
        }
        res = await client.post("/vehicles", json=vehicle_payload)
        print("Create Vehicle status:", res.status_code)
        assert res.status_code == 201
        created_vehicle = res.json()
        assert created_vehicle["make"] == "Toyota"
        assert created_vehicle["plate_number"] == "LAG-123-XY"
        assert created_vehicle["owner_id"] == user_id
        vehicle_id = created_vehicle["id"]
        print("Vehicle created with ID:", vehicle_id)

        # Duplicate plate test
        dup_res = await client.post("/vehicles", json=vehicle_payload)
        print("Duplicate Plate status:", dup_res.status_code)
        assert dup_res.status_code == 400
        assert "plate number already exists" in dup_res.json()["detail"]

        print("\n--- 3. Testing List Vehicles (GET /vehicles) ---")
        # Create second vehicle
        await client.post("/vehicles", json={
            "make": "Honda",
            "model": "Civic",
            "colour": "Black",
            "capacity": 3,
            "plate_number": "ABJ-456-ZZ"
        })

        list_res = await client.get("/vehicles")
        print("List Vehicles status:", list_res.status_code)
        assert list_res.status_code == 200
        vehicles = list_res.json()
        assert len(vehicles) == 2

        # Filter by owner_id
        filtered_res = await client.get(f"/vehicles?owner_id={user_id}")
        assert filtered_res.status_code == 200
        assert len(filtered_res.json()) == 1
        assert filtered_res.json()[0]["owner_id"] == user_id
        print("List and filtering tests passed!")

        print("\n--- 4. Testing Get Vehicle by ID (GET /vehicles/{id}) ---")
        get_res = await client.get(f"/vehicles/{vehicle_id}")
        print("Get Vehicle status:", get_res.status_code)
        assert get_res.status_code == 200
        assert get_res.json()["id"] == vehicle_id

        # Non-existent ID test
        import uuid
        fake_id = str(uuid.uuid4())
        fake_res = await client.get(f"/vehicles/{fake_id}")
        assert fake_res.status_code == 404
        print("Get Vehicle by ID tests passed!")

        print("\n--- 5. Testing Update Vehicle (PATCH /vehicles/{id}) ---")
        update_res = await client.patch(
            f"/vehicles/{vehicle_id}",
            json={"colour": "Midnight Blue", "capacity": 5}
        )
        print("Update Vehicle status:", update_res.status_code)
        assert update_res.status_code == 200
        updated = update_res.json()
        assert updated["colour"] == "Midnight Blue"
        assert updated["capacity"] == 5
        assert updated["make"] == "Toyota"

        # Update plate to duplicate
        bad_plate_res = await client.patch(
            f"/vehicles/{vehicle_id}",
            json={"plate_number": "ABJ-456-ZZ"}
        )
        assert bad_plate_res.status_code == 400
        assert "plate number already exists" in bad_plate_res.json()["detail"]
        print("Update Vehicle tests passed!")

        print("\n--- 6. Testing Delete Vehicle (DELETE /vehicles/{id}) ---")
        del_res = await client.delete(f"/vehicles/{vehicle_id}")
        print("Delete Vehicle status:", del_res.status_code)
        assert del_res.status_code == 204

        # Verify soft-deleted vehicle is no longer returned
        get_after_del = await client.get(f"/vehicles/{vehicle_id}")
        assert get_after_del.status_code == 404

        list_after_del = await client.get("/vehicles")
        remaining = list_after_del.json()
        assert len(remaining) == 1
        assert remaining[0]["plate_number"] == "ABJ-456-ZZ"
        print("Delete Vehicle tests passed!")

    print("\n==========================================")
    print("ALL VEHICLE CRUD TESTS PASSED SUCCESSFULLY!")
    print("==========================================")


if __name__ == "__main__":
    asyncio.run(run_vehicle_tests())
