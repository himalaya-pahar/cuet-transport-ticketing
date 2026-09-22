# 🚌 CUET Transport Ticketing & Billing Backend

An automated transport ticketing, scan logging, and monthly billing system designed for Chittagong University of Engineering and Technology (CUET).

Built with **FastAPI**, **SQLAlchemy 2.0**, and **APScheduler**, this system enables university buses to log teacher boardings and automatically calculates monthly transport bills.

---

## 🛠️ Tech Stack

* **Framework:** [FastAPI](https://fastapi.tiangolo.com/) (Python 3.9+)
* **Database & ORM:** SQLite / PostgreSQL with [SQLAlchemy 2.0](https://www.sqlalchemy.org/)
* **Authentication:** OAuth2 with Password Bearer & Role-Based JWT tokens (`admin`, `bus`)
* **Password Hashing:** `pwdlib` (Argon2id)
* **Configuration:** `pydantic-settings`
* **Task Scheduling:** [APScheduler](https://apscheduler.readthedocs.io/)
* **Testing:** Python `unittest` with FastAPI `TestClient`

---

## 📁 Project Structure

```text
cuet-transport-ticketing/
├── config.py                 # Centralized configuration & environment variables
├── database.py               # SQLAlchemy 2.0 engine, sessions & SQLite PRAGMA hook
├── models.py                 # SQLAlchemy ORM models (Teacher, Bus, Logs, Admin, Bill)
├── schemas.py                # Pydantic v2 schemas for request validation & responses
├── main.py                   # FastAPI app with modern lifespan management & CORS
├── migrate_db.py             # Database migration helper script
├── test_app.py               # Automated test suite
├── .env.example              # Template for environment configuration
├── .gitignore                # Git ignore rules for DB, logs, environments, and caches
├── security/
│   ├── hashing.py            # Password hashing & verification (Argon2id)
│   ├── token.py              # JWT creation and decoding
│   └── oauth.py              # Role-based OAuth2 guards (get_current_admin, get_current_bus)
├── repository/               # Database operations & business logic
│   ├── admin.py              # Admin CRUD
│   ├── authentication.py     # Login logic for Bus & Admin
│   ├── bus.py                # Bus registration & lookup
│   ├── teacher.py            # Teacher registration & management
│   ├── scan.py               # RFID/QR scan logging & anti-double-tap debounce
│   ├── generatebill.py       # Accurate monthly billing cron calculation
│   └── bill.py               # Bill retrieval & payment status updates
└── routers/                  # API endpoints
    ├── admin.py              # /admin endpoints
    ├── authentication.py     # /login/bus and /login/admin
    ├── bus.py                # /bus endpoints
    ├── teacher.py            # /teacher endpoints
    ├── scan.py               # /scan endpoints
    └── bill.py               # /bill endpoints
```

---

## 🚀 Getting Started

### 1. Prerequisites
* Python 3.9 or higher
* `venv` or `conda`

### 2. Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/himalaya-pahar/cuet-transport-ticketing.git
   cd cuet-transport-ticketing
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   Copy the example environment file:
   ```bash
   cp .env.example .env
   ```
   Modify `.env` as needed:
   ```ini
   PROJECT_NAME="CUET Transport Ticketing"
   SECRET_KEY="your-random-production-secret-key"
   ACCESS_TOKEN_EXPIRE_MINUTES=1440
   DATABASE_URL="sqlite:///./transport.db"
   FARE_PER_TRIP=15
   CORS_ORIGINS=["*"]
   ```

5. **Initialize / Migrate the database:**
   ```bash
   python migrate_db.py
   ```

6. **Run the development server:**
   ```bash
   fastapi dev main.py
   # Or using uvicorn directly:
   uvicorn main:app --reload
   ```

Interactive API documentation will be available at:
* Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 🔐 Authentication & Roles

The system uses **Role-Based JWT Tokens**. In Swagger UI (`/docs`), clicking the **Authorize** button presents two separate authentication schemes:
* **`AdminAuth`**: Authenticates against `/login/admin` (e.g. `nafis` / `nafis`).
* **`BusAuth`**: Authenticates against `/login/bus` (e.g. `Surma` / `surma`).

| Role | Token Endpoint | Capabilities |
| :--- | :--- | :--- |
| **Unified** | `POST /login` | Auto-detects whether the credentials belong to an Admin or a Bus. |
| **Admin** | `POST /login/admin` | Full control: manage teachers, buses, admins, view all logs, generate/manage bills. |
| **Bus** | `POST /login/bus` | Terminal access: log teacher scans via `POST /scan/`. |

> **First-Time Bootstrapping**: If no admin accounts exist in the database, `POST /admin/` allows registering the initial administrator without requiring existing authentication. Subsequent registrations require admin privileges.

---

## 📡 API Endpoints Overview

### Authentication (`/login`)
* `POST /login` - Unified login (auto-detects Admin or Bus).
* `POST /login/admin` - Admin login (OAuth2 password form: username & password).
* `POST /login/bus` - Bus terminal login (OAuth2 password form: bus name & password).

### Admin Management (`/admin`)
* `POST /admin/` - Register an admin.
* `GET /admin/` - List all administrators *(Admin only)*.
* `GET /admin/{id}` - View specific administrator *(Admin only)*.

### Teachers (`/teacher`)
* `POST /teacher/` - Register a teacher (`id`, `name`, `department`, `email`, `phone`) *(Admin only)*.
* `GET /teacher/` - List all teachers *(Admin only)*.
* `GET /teacher/{id}` - Get teacher profile by CUET ID.
* `DELETE /teacher/{id}` - Delete a teacher record *(Admin only)*.

### Buses (`/bus`)
* `POST /bus/` - Register a university bus (`name`, `route`, `password`) *(Admin only)*.
* `GET /bus/` - List all buses *(Admin only)*.
* `GET /bus/{name}` - Get bus details *(Admin only)*.
* `DELETE /bus/{name}` - Remove a bus *(Admin only)*.

### Scans & Boarding Logs (`/scan`)
* `POST /scan/` - Log teacher boarding (`{"teacher_id": 1234}`) *(Bus only)*.
  * *Includes a 60-second anti-double-tap debounce to prevent accidental double scans.*
* `GET /scan/` - Paginated scan history (`skip`, `limit`) *(Admin only)*.
* `GET /scan/teacher/{id}` - Scan history for a teacher *(Admin only)*.
* `GET /scan/bus/{bus_name}` - Scan history for a specific bus *(Admin only)*.
* `GET /scan/teacher/{id}/bus/{bus_name}` - Filter scans by teacher and bus *(Admin only)*.

### Monthly Billing (`/bill`)
* `GET /bill/` - View bills with optional `month` and `status` filters *(Admin only)*.
* `GET /bill/teacher/{teacher_id}` - View all billing history for a teacher *(Admin only)*.
* `GET /bill/{id}` - View a specific bill *(Admin only)*.
* `PATCH /bill/{id}/status` - Mark bill as `'paid'` or `'unpaid'` *(Admin only)*.
* `POST /bill/generate` - Manually trigger billing calculation for the preceding month *(Admin only)*.

---

## ⏰ Automated Monthly Billing

The background scheduler (APScheduler) triggers on the **1st of every month at midnight (00:00 UTC)**:
* Calculates all trips recorded in the interval: `[first_day_of_previous_month, first_day_of_current_month)`.
* Computes `total_bill = total_trips * FARE_PER_TRIP` (default: 15 BDT).
* Records are stored with a unique composite key `(teacher_id, billing_month)` to ensure idempotency. Re-running the billing process updates existing records rather than producing duplicates.

---

## 🧪 Running Automated Tests

Run the test suite using Python's built-in `unittest`:
```bash
python test_app.py
```
Or with `pytest` if installed:
```bash
pytest test_app.py -v
```

---

## 🔒 Security Best Practices

1. **Environment Variables**: Never commit `.env` or production secrets to source control.
2. **Key Rotation**: Change `SECRET_KEY` in production to a cryptographically secure 256-bit string (`openssl rand -hex 32`).
3. **Database Backups**: Regularly backup your production SQLite database or use PostgreSQL for high-concurrency environments.
