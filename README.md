# VillageFood — Backend API

A production-ready FastAPI backend for the VillageFood e-commerce platform.

## Tech Stack & Design Decisions

| Choice | What | Why |
|--------|------|-----|
| **FastAPI** | Python web framework | Async, auto-docs (Swagger), Pydantic validation, fastest Python framework |
| **MongoDB** | Database | Flexible schema for products/orders, great with Python (motor), free Atlas tier for cloud |
| **Motor** | Async MongoDB driver | Non-blocking DB calls, perfect with FastAPI's async nature |
| **JWT + bcrypt** | Authentication | Industry standard. JWT for stateless auth, bcrypt for password hashing |
| **Mock Razorpay** | Payments | Mirrors real Razorpay API contract — swap to real with just API keys |
| **Mock Shiprocket** | Logistics | Mirrors real Shiprocket API — auto-assigns courier + AWB on order creation |

## Architecture

```
backend/
├── app/
│   ├── api/
│   │   ├── deps.py          # Auth dependency (JWT extraction)
│   │   └── endpoints/
│   │       ├── auth.py       # Signup, Login, /me
│   │       ├── products.py   # Product catalog (auto-seeds on first run)
│   │       ├── cart.py       # Cart sync
│   │       ├── addresses.py  # User delivery addresses
│   │       ├── orders.py     # Order creation + tracking
│   │       └── payments.py   # Payment create/verify
│   ├── auth/
│   │   └── security.py       # JWT token creation + verification
│   ├── core/
│   │   ├── config.py         # Settings from .env (auto-detects mock vs real services)
│   │   └── database.py       # MongoDB connection (works with local or Atlas)
│   ├── domain/models/         # Pydantic models
│   ├── services/
│   │   ├── payments.py       # Mock Razorpay (same data contract as real)
│   │   └── logistics.py      # Mock Shiprocket (same data contract as real)
│   └── main.py               # FastAPI app entry point
├── .env.example               # Template for environment variables
├── requirements.txt
└── Dockerfile
```

## Running Locally

### Prerequisites
- Python 3.10+
- MongoDB (running on `localhost:27017`)

### Steps
```bash
# 1. Clone
git clone git@github.com:ppandeyvinay22/vill-proj-backend.git
cd vill-proj-backend

# 2. Create virtual environment
python -m venv villageenv
source villageenv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment
cp .env.example .env
# Edit .env if needed (defaults work for local dev)

# 5. Start MongoDB (if not running)
sudo systemctl start mongod

# 6. Run the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API is now live at **http://localhost:8000**  
Swagger docs at **http://localhost:8000/docs**

## Running with Docker

```bash
# From the parent directory (where docker-compose.yml is)
docker-compose up --build
```

This starts MongoDB, Backend, and Frontend together.

## Switching to Production

| Service | How to Switch |
|---------|-------------|
| **MongoDB Atlas** | Change `MONGODB_URL` in `.env` to your Atlas connection string |
| **Razorpay** | Add `RAZORPAY_KEY_ID` and `RAZORPAY_KEY_SECRET` in `.env` |
| **Shiprocket** | Add `SHIPROCKET_EMAIL` and `SHIPROCKET_PASSWORD` in `.env` |

The code auto-detects whether real credentials are present. No code changes needed.

## API Endpoints

| Method | Endpoint | Auth | Description |
|--------|---------|------|-------------|
| POST | `/api/auth/signup` | ❌ | Create account |
| POST | `/api/auth/login` | ❌ | Login (returns JWT) |
| GET | `/api/auth/me` | ✅ | Get current user |
| GET | `/api/products/` | ❌ | List all products |
| POST | `/api/cart/sync` | ✅ | Sync cart |
| GET | `/api/cart/` | ✅ | Get cart |
| POST | `/api/addresses/` | ✅ | Add address |
| GET | `/api/addresses/` | ✅ | List addresses |
| POST | `/api/payments/create` | ✅ | Create payment order |
| POST | `/api/payments/verify` | ✅ | Verify payment |
| POST | `/api/orders/` | ✅ | Place order |
| GET | `/api/orders/` | ✅ | List user's orders |
| GET | `/api/orders/{id}/track` | ✅ | Track shipment |
