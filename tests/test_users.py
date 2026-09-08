import asyncio
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.pool import StaticPool

from db import get_db
from main import app
from models import Base, User
from utils.security import hash_password, verify_password


async def run_tests():
    print("--- 1. Testing Security Utility (hash_password & verify_password) ---")
    raw_pwd = "mySuperSecretPassword@123"
    hashed = hash_password(raw_pwd)
    assert hashed != raw_pwd
    assert verify_password(raw_pwd, hashed) is True
    assert verify_password("wrongpassword", hashed) is False
    print("Security utility tests passed!")

    print("\n--- 2. Setting up In-Memory SQLite Test Database ---")
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
            yield session
            await session.commit()

    app.dependency_overrides[get_db] = override_get_db

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        print("\n--- 3. Testing User Registration (/users/register) ---")
        user_payload = {
            "first_name": "Alice",
            "last_name": "Smith",
            "email": "alice@example.com",
            "phone_number": "+1234567890",
            "password": "strongPassword123",
            "role": "passenger"
        }

        # Successful registration
        response = await client.post("/users/register", json=user_payload)
        print("Register Response status:", response.status_code)
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "alice@example.com"
        assert data["first_name"] == "Alice"
        assert data["last_name"] == "Smith"
        assert "password" not in data
        assert "id" in data
        assert "created_at" in data
        print("User registered successfully:", data["id"])

        # Duplicate email registration
        duplicate_email_payload = {
            "first_name": "Bob",
            "last_name": "Jones",
            "email": "alice@example.com",
            "phone_number": "+1987654321",
            "password": "anotherPassword123",
            "role": "driver"
        }
        dup_email_resp = await client.post("/users/register", json=duplicate_email_payload)
        print("Duplicate email status:", dup_email_resp.status_code, dup_email_resp.json())
        assert dup_email_resp.status_code == 400
        assert "email already exists" in dup_email_resp.json()["detail"]

        # Duplicate phone number registration
        duplicate_phone_payload = {
            "first_name": "Bob",
            "last_name": "Jones",
            "email": "bob@example.com",
            "phone_number": "+1234567890",
            "password": "anotherPassword123",
            "role": "driver"
        }
        dup_phone_resp = await client.post("/users/register", json=duplicate_phone_payload)
        print("Duplicate phone status:", dup_phone_resp.status_code, dup_phone_resp.json())
        assert dup_phone_resp.status_code == 400
        assert "phone number already exists" in dup_phone_resp.json()["detail"]

        print("\n--- 4. Testing User Login (/users/login) ---")
        # Successful login
        login_payload = {
            "email": "alice@example.com",
            "password": "strongPassword123"
        }
        login_resp = await client.post("/users/login", json=login_payload)
        print("Login status:", login_resp.status_code)
        assert login_resp.status_code == 200
        login_data = login_resp.json()
        assert login_data["message"] == "Login successful"
        assert login_data["user"]["email"] == "alice@example.com"
        assert "password" not in login_data["user"]
        print("Login successful for alice@example.com")

        # Wrong password
        bad_pwd_payload = {
            "email": "alice@example.com",
            "password": "wrongPassword"
        }
        bad_pwd_resp = await client.post("/users/login", json=bad_pwd_payload)
        print("Bad password status:", bad_pwd_resp.status_code)
        assert bad_pwd_resp.status_code == 401
        assert bad_pwd_resp.json()["detail"] == "Invalid email or password."

        # Non-existent email
        nonexistent_payload = {
            "email": "nobody@example.com",
            "password": "strongPassword123"
        }
        nonexistent_resp = await client.post("/users/login", json=nonexistent_payload)
        print("Nonexistent user status:", nonexistent_resp.status_code)
        assert nonexistent_resp.status_code == 401
        assert nonexistent_resp.json()["detail"] == "Invalid email or password."

        # Soft-deleted user test
        print("\n--- 5. Testing Soft-deleted Account Login ---")
        async with async_session() as session:
            deleted_user = User(
                first_name="Deleted",
                last_name="User",
                email="deleted@example.com",
                phone_number="+1000000000",
                password=hash_password("deletedPassword123"),
                role="passenger",
                deleted_at=datetime.now(timezone.utc)
            )
            session.add(deleted_user)
            await session.commit()

        deleted_login_resp = await client.post("/users/login", json={
            "email": "deleted@example.com",
            "password": "deletedPassword123"
        })
        print("Deleted user login status:", deleted_login_resp.status_code)
        assert deleted_login_resp.status_code == 403
        assert deleted_login_resp.json()["detail"] == "Account is deactivated."

    print("\n==========================================")
    print("ALL TESTS PASSED SUCCESSFULLY!")
    print("==========================================")


if __name__ == "__main__":
    asyncio.run(run_tests())
