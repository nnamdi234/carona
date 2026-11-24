# Carona API: notes for whoever works on this next (person or AI)

Read this first. It holds the background that isn't obvious from the code.

## What this is

Carona is a carpooling app for daily commuters in Lagos: drivers offer the empty seats on trips they already make, and passengers book them. This repo is the **FastAPI backend**. The React frontend is a sibling folder, `../carona-frontend` (see its `AGENTS.md`).

It is also a **teaching project**. The owner (Akorede) teaches a student who is learning to code. The student types the code from a lesson page into their own IDE, class by class. So:

- Keep code simple and readable for a beginner. Follow the patterns already in the repo; don't refactor wholesale.
- Don't silently fix the student's work on `main`. Point out bugs, or put fixes on a branch, unless the owner asks otherwise.
- Every endpoint is built in four steps: **Schemas → Logic (controllers/) → Route (routes/) → Test (Swagger at /docs)**.

## Run it

```bash
python -m venv .venv && .venv\Scripts\activate    # Windows
pip install -r requirements.txt bcrypt PyJWT       # see "Open issues": these two are missing from requirements.txt
uvicorn main:app --reload
```

`.env` needs `DATABASE_URL` (async Postgres, hosted on Render), `SECRET_KEY`, `ALGORITHM` and `CORS_ORIGINS` (comma-separated, e.g. `http://localhost:5173`). See `.env.example`. Tables are created at startup with `Base.metadata.create_all`; there are no Alembic migrations yet, so `create_all` never changes an existing table (an empty table can be dropped and recreated; a table with data needs a migration).

## Layout

```
main.py            app, CORS, routers
db.py              async engine and get_db (one session per request, commits at the end)
models/            SQLAlchemy models; every table inherits id (UUID), created_at, updated_at, deleted_at from models/base.py
schemas/           Pydantic input/output schemas (note: schemas/___init__.py has three underscores; it works, leave it unless asked)
controllers/       the logic; every success returns {"success": True, "message": ..., "data": ...}
routes/            the routers (routers/ is an empty leftover)
utils/security.py  bcrypt hashing, JWT creation, get_current_user
```

Lesson pages and the domain brief live in the sibling folder `../carona-lessons` (published at https://carona-lessons.web.app).

## Decisions (the owner's; don't change them without asking)

- **Being a driver comes from owning a vehicle, not from `role`.** `role` stays `user` (later `admin`). Offer a ride asks for a vehicle first if the user has none.
- **Users can't change their email.** `PATCH /users/me` edits first name, last name and phone only; the update schema leaves email out.
- Vehicle `capacity` means **passenger seats** (driver not counted). Fare is **per seat**, set by the driver, **naira**, **cash at pickup**. **Instant booking** (no driver approval). Passengers can cancel until departure, no penalty.
- Places are free text for version 1. Sample data uses Lagos places.
- Times are timezone-aware (`AwareDatetime`). Lagos is UTC+1 all year; a search "day" is 00:00–24:00 Lagos time.
- Ride responses are built by hand (`format_ride`) so passengers see the driver's name only: never email, phone, password hash or plate number. The plate is shown only after booking.
- Error `detail` strings are matched by the frontend; keep them exact once written.

## Where things stand (24 Nov 2026)

Done: register, login (JWT, 24 h), `GET /users/me`, `PATCH /users/me` (phone can be cleared with `null`), vehicles CRUD minus delete (`PATCH /vehicles/{id}` fixed), CORS, Ride model with `seats_offered` and nullable `distance_km`, `RideCreate`, `create_ride` (with `origin` length, `seats_offered` insert, and seat-limit error message fixed in commit `4f64f0c`).

Next two lessons ready in `../carona-lessons` (https://carona-lessons.web.app):
- **Rides, part 3** (`2026-11-20-rides-search-and-get.html`): wire `rides_router` in `main.py`, test `POST /rides/`, build `search_rides` (`GET /rides/?origin=&destination=&day=`) and `get_ride_by_id` (`GET /rides/{ride_id}`).
- **Response shaping and privacy** (`2026-11-24-response-shaping-and-privacy.html`): hide password hashes with `UserOut` + `response_model`, and shape ride responses with `format_ride` + SQL `JOIN`s (unlocking the full Offer → Search → Ride Detail flow in `../carona-frontend`).

After that: bookings (Booking table, `POST /rides/{id}/bookings`, `GET /bookings/me`, cancel, then `seats_left` = `seats_offered` minus booked seats), then `GET /rides/mine`, `PATCH /rides/{id}/status`, `DELETE /vehicles/{id}`. Later: ratings, notifications, maps, payments, admin, Alembic. The full plan is in the domain brief (`https://carona-lessons.web.app/domain-brief.html`).

## Open issues

- **Password hashes are sent to clients.** User routes use `response_model=None` and return the ORM object, so `password` is in every user response, and `GET /users/` needs no login. The fix (`UserOut`, `UserResponse`, `UserListResponse` with `response_model`) is covered in the `2026-11-24-response-shaping-and-privacy.html` lesson.
- `requirements.txt` is missing `bcrypt` and `PyJWT` (installed in `.venv` only).
- Login returns 403 and says whether the email exists ("This account does not exist" / "Incorrect password"). The design wants 401 and one message: "Email or password is incorrect". (The frontend already shows that one message either way.)
- Vehicle `capacity` has no bounds (the form allows 1–8).
- Nothing filters on `deleted_at`.
- `driver_id` and `vehicle_id` on Ride are nullable; the server sets them, but they should be required.

## Lessons & domain brief

- Live site: https://carona-lessons.web.app (Firebase Hosting project `carona-lessons`, source in sibling folder `../carona-lessons/public/`).
- `../carona-lessons/public/domain-brief.html`: the domain brief (glossary, data model, API contract, lifecycles, journeys, roadmap, open questions). Written at commit `5a234ed`, so its "known issues" list is older than the one above.
- `../carona-lessons/public/lessons/`: one HTML page per class, in date order. Each has the exact code for that class, Swagger test steps and the complete files. Publish updates from `../carona-lessons` with `npx -y firebase-tools@latest deploy --only hosting`.
- The designs (21 screens and the design system) live in the frontend: `../carona-frontend/public/design/`.

## How lessons are made

One HTML page per class. The owner prefers **short pages**: the code snippets matter most (file name, where in the file, a copy button), plus Swagger test steps and the complete files at the end. They explain the rest out loud, so no long prose, diagrams or big tables. Before writing a new lesson, check the student's latest code against the previous lesson; they often commit with small bugs (the last time: a missing import and four schema typos), and the next lesson starts by fixing those.
