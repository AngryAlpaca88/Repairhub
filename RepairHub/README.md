# RepairHub

RepairHub is a multi-location electronics repair CRM + POS + inventory + staff management system.

## Tech Stack

- **Backend**: Python 3.12, FastAPI, SQLAlchemy (Async), PostgreSQL
- **Frontend**: React 18, TypeScript, Vite, TailwindCSS, React Query
- **Infrastructure**: Docker, Docker Compose

## Getting Started

### Prerequisites

- Docker and Docker Compose installed.

### Setup

1.  Clone the repository.
2.  Copy `.env.example` to `.env` (optional, defaults in docker-compose work for dev).
    ```bash
    cp .env.example .env
    ```
3.  Start the stack:
    ```bash
    docker compose up --build
    ```

### Migrations

To run database migrations (after the containers are up):

```bash
docker compose exec backend alembic upgrade head
```

### Seed Data

To populate the database with initial demo data (Company, Locations, Users, Parts):

```bash
docker compose exec backend python app/initial_data.py
```

### Accessing the App

- **Frontend**: http://localhost:5173
- **Backend API Docs**: http://localhost:8000/docs

### Default Login

You will need to create an initial user via the API or database directly as public signup is disabled.

To create a user via python shell in the container:
```bash
docker compose exec backend python
```
```python
import asyncio
from app.db.session import AsyncSessionLocal
from app.models.user import User
from app.core.security import get_password_hash

async def create_admin():
    async with AsyncSessionLocal() as db:
        user = User(
            email="admin@example.com",
            hashed_password=get_password_hash("admin123"),
            full_name="Admin User",
            role="OWNER",
            is_active=True
        )
        db.add(user)
        await db.commit()
        print("Admin created")

asyncio.run(create_admin())
```

## Features

- **Tickets**: Manage repair tickets with status tracking.
- **Inventory**: Track parts and stock levels per location.
- **Profit Rule**: Enforces minimum $100 pure profit on repairs involving parts.
- **Multi-location**: Support for multiple stores.
