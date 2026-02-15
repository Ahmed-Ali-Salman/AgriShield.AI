# 🛡️ AgriShield AI

**Cyber-Resilient Food Supply Intelligence Platform**

A SaaS platform that protects food supply chains from cyberattacks, data manipulation, and operational disruptions — using AI-powered risk scoring, anomaly detection, and real-time alerting.

---

## ✨ Features

- **Supplier Risk Scoring** — Weighted multi-signal risk scores (IT security, data consistency, delivery reliability, compliance, external factors)
- **Anomaly Detection** — Flag invoice discrepancies, quantity deviations, price spikes, and behavioral anomalies
- **Real-Time Alerts** — Severity-based alerts (info / warning / critical) with status tracking
- **Role-Based Access Control** — JWT authentication with admin / analyst / viewer roles
- **Dashboard** — Live supplier count, open alerts, risk score trends
- **Data Ingestion** — CSV/Excel upload for supplier data

---

## 🏗️ Architecture

Four-layer **SOLID architecture** with Dependency Inversion:

```
Presentation  →  Application  →  Domain  ←  Infrastructure
(API routes)     (Use cases)     (Core)     (DB, ML, services)
```

| Layer          | Path                            | Responsibility                                |
|----------------|---------------------------------|-----------------------------------------------|
| Domain         | `backend/app/domain/`           | Entities, value objects, interfaces, pure logic |
| Application    | `backend/app/application/`      | Use cases, DTOs, orchestration                |
| Infrastructure | `backend/app/infrastructure/`   | Database, ML, external services, security     |
| Presentation   | `backend/app/presentation/`     | FastAPI routes, schemas, middleware           |

---

## 🛠️ Tech Stack

| Component  | Technology                          |
|------------|-------------------------------------|
| Backend    | Python 3.11+ / FastAPI / SQLAlchemy |
| Frontend   | Next.js 14 / TypeScript / React 18  |
| Database   | SQLite (dev) / PostgreSQL (prod)    |
| Auth       | JWT + bcrypt + RBAC                 |
| State      | Zustand                            |
| Charts     | Recharts                           |
| Icons      | Lucide React                       |

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+

### Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux
pip install -r requirements.txt
```

Create a `.env` file (see `.env.example`), then:

```bash
uvicorn main:app --reload
```

Seed demo data:

```bash
python seed.py
# Creates admin user: admin@agrishield.ai / admin123
# Creates 5 sample suppliers
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

### Docker (Production)

```bash
docker-compose up --build
```

---

## 📡 API Endpoints

**Base URL:** `http://localhost:8000/api/v1`

| Method | Endpoint                              | Description              |
|--------|---------------------------------------|--------------------------|
| POST   | `/auth/login`                         | Login, returns JWT       |
| POST   | `/auth/register`                      | Register new user        |
| GET    | `/suppliers/`                         | List all suppliers       |
| GET    | `/suppliers/{id}`                     | Get supplier by ID       |
| POST   | `/suppliers/`                         | Create supplier          |
| PATCH  | `/suppliers/{id}`                     | Update supplier          |
| POST   | `/risk-scores/{supplier_id}`          | Calculate risk score     |
| GET    | `/risk-scores/{supplier_id}/history`  | Risk score history       |
| GET    | `/alerts/`                            | List alerts              |
| POST   | `/alerts/`                            | Create alert             |
| GET    | `/anomalies/{supplier_id}`            | Anomalies by supplier    |
| GET    | `/anomalies/unreviewed`               | Unreviewed anomalies     |
| POST   | `/anomalies/detect/{supplier_id}`     | Detect anomalies         |
| GET    | `/dashboard/summary`                  | Dashboard stats          |
| POST   | `/data/upload`                        | Upload CSV/Excel         |
| GET    | `/health`                             | Health check             |

> All endpoints (except `/auth/*` and `/health`) require `Authorization: Bearer <token>` header.

---

## 📁 Project Structure

```
AgriShield.AI/
├── backend/                    # FastAPI backend
│   ├── app/
│   │   ├── domain/             # Entities, value objects, interfaces
│   │   ├── application/        # Use cases, DTOs
│   │   ├── infrastructure/     # DB repos, JWT, ML services
│   │   ├── presentation/       # API routes, schemas, middleware
│   │   └── shared/             # Cross-cutting concerns
│   ├── main.py                 # App entry point
│   ├── seed.py                 # Demo data seeder
│   ├── test_e2e.py             # E2E API tests
│   └── requirements.txt
├── frontend/                   # Next.js 14 frontend
│   └── src/
│       ├── app/                # Pages (login, dashboard, suppliers, etc.)
│       ├── components/         # UI components (Card, Button, Sidebar, etc.)
│       ├── hooks/              # Data hooks (useAuth, useSuppliers, etc.)
│       ├── services/           # API service layer (axios)
│       ├── store/              # Zustand state management
│       ├── types/              # TypeScript interfaces
│       └── lib/                # Utilities and formatters
├── docs/                       # Documentation
├── docker-compose.yml          # Docker orchestration
└── .env.example                # Environment template
```

---

## 🔐 Default Credentials

After running `seed.py`:

| Email                  | Password   | Role  |
|------------------------|------------|-------|
| admin@agrishield.ai    | admin123   | admin |

---

## 📄 License

Proprietary — All rights reserved.
