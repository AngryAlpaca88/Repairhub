# RepairHub — Tech Revival Software

RepairHub is a multi-location electronics repair CRM + POS + inventory + staff management system.

This repo contains a 2025-modern stack:
- Backend: Python 3.12+, FastAPI, SQLAlchemy (async), Pydantic v2, Alembic-ready
- Auth: JWT access tokens + refresh tokens in HttpOnly Secure cookies (Argon2 password hashing)
- Database: PostgreSQL 15+ (assumes 16)
- Frontend: React 18 + TypeScript + Vite + TailwindCSS, React Query
- Containerized: Docker + docker-compose v2

This scaffold implements core domain models, ticket workflow, inventory basics, and the minimum pure-profit rule (default $100). It includes seed data to demo Company (Computer Corner), multiple locations, a few users, services, and parts.

## Quick start (dev)

1. Copy .env.example -> .env and edit values
2. Start the stack:
   ```bash
   docker compose up --build
   ```
3. Enter backend container to run migrations / seed (or run them locally):
   ```bash
   docker compose exec backend bash
   python -m alembic upgrade head
   python -m app.seed  # seeds demo data
   ```

## Default demo logins (seeded)

- owner@computercorner.test / Password123!
- manager@store1.test / Password123!
- tech@store1.test / Password123!

(See backend/app/seed.py for details)

## API

- Base: /api/v1/
- OpenAPI: /api/v1/openapi.json
- Auth:
  - POST /api/v1/auth/login
  - POST /api/v1/auth/refresh
  - POST /api/v1/auth/logout
  - GET /api/v1/auth/me

## Enforced business rules

- Minimum pure profit enforcement: default $100 per repair when inventory parts are used.
  - Technicians/Cashiers cannot create ticket prices violating the rule.
  - Managers/Owners can override; overrides are logged to AuditLog.

## Notes & assumptions

- This repo is a scaffold and MVP: many features (full UI flows, advanced reporting charts, webhook retries) are intentionally left as next steps but models and hooks are included.
- Passwords and secrets must be set through environment variables — never hardcoded.
- Cloudflare Tunnel: app listens internally (backend 8000, frontend 5173/static) and assumes tunnel exposes the ports publicly.

## What's next (already scaffolded)

- Add Alembic revision files and run migrations.
- Expand APIs: Tickets CRUD, Inventory receiving, Supplier POs, Payments.
- Build out the React UI pages and wire React Query hooks to endpoints.
- Add ESLint/Prettier, Ruff/Black config, and CI workflows for lint/test.

## Files of interest

- backend/app: FastAPI app, models, api routers, pricing enforcement
- frontend/: Vite React app with Tailwind, starter pages
- docker-compose.yml / .env.example