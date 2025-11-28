"""Seed script to populate the database with demo data."""
import asyncio
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from app.core.config import settings
from app.core.security import hash_password
from app.models import Base, Company, Customer, Location, Part, Service, User


async def seed_database():
    """Seed the database with demo data."""
    engine = create_async_engine(settings.DATABASE_URL, echo=True)
    AsyncSessionLocal = async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    async with AsyncSessionLocal() as db:
        # Check if already seeded
        result = await db.execute(select(Company).limit(1))
        if result.scalar_one_or_none():
            print("Database already seeded, skipping...")
            return

        print("Seeding database with demo data...")

        # Create company
        company = Company(name="Computer Corner")
        db.add(company)
        await db.flush()

        # Create locations
        location1 = Location(
            company_id=company.id,
            name="Downtown Store",
            address="123 Main St, Downtown, TX 75001",
            phone="(555) 123-4567",
        )
        location2 = Location(
            company_id=company.id,
            name="Westside Shop",
            address="456 West Ave, Westside, TX 75002",
            phone="(555) 987-6543",
        )
        db.add_all([location1, location2])
        await db.flush()

        # Create users with demo passwords
        # NOTE: In production, use strong unique passwords!
        demo_password = hash_password("Password123!")

        owner = User(
            company_id=company.id,
            email="owner@computercorner.test",
            hashed_password=demo_password,
            full_name="John Owner",
            role="owner",
        )
        owner.locations.extend([location1, location2])

        manager = User(
            company_id=company.id,
            email="manager@store1.test",
            hashed_password=demo_password,
            full_name="Jane Manager",
            role="manager",
        )
        manager.locations.append(location1)

        tech = User(
            company_id=company.id,
            email="tech@store1.test",
            hashed_password=demo_password,
            full_name="Bob Technician",
            role="technician",
        )
        tech.locations.append(location1)

        cashier = User(
            company_id=company.id,
            email="cashier@store1.test",
            hashed_password=demo_password,
            full_name="Alice Cashier",
            role="cashier",
        )
        cashier.locations.append(location1)

        db.add_all([owner, manager, tech, cashier])
        await db.flush()

        # Create services
        services = [
            Service(
                company_id=company.id,
                name="Diagnostic",
                description="Initial device diagnostic and assessment",
                base_price=Decimal("49.99"),
            ),
            Service(
                company_id=company.id,
                name="Virus Removal",
                description="Complete virus and malware removal",
                base_price=Decimal("99.99"),
            ),
            Service(
                company_id=company.id,
                name="Screen Repair",
                description="LCD/LED screen replacement",
                base_price=Decimal("149.99"),
            ),
            Service(
                company_id=company.id,
                name="Data Recovery",
                description="Recovery of data from damaged drives",
                base_price=Decimal("199.99"),
            ),
            Service(
                company_id=company.id,
                name="OS Reinstall",
                description="Fresh operating system installation",
                base_price=Decimal("79.99"),
            ),
        ]
        db.add_all(services)
        await db.flush()

        # Create parts/inventory
        parts = [
            Part(
                company_id=company.id,
                location_id=location1.id,
                sku="RAM-8GB-DDR4",
                name="8GB DDR4 RAM",
                description="Generic 8GB DDR4 desktop memory",
                cost=Decimal("25.00"),
                price=Decimal("49.99"),
                quantity=20,
                min_quantity=5,
            ),
            Part(
                company_id=company.id,
                location_id=location1.id,
                sku="SSD-256-SATA",
                name="256GB SATA SSD",
                description="2.5-inch SATA SSD drive",
                cost=Decimal("30.00"),
                price=Decimal("69.99"),
                quantity=15,
                min_quantity=3,
            ),
            Part(
                company_id=company.id,
                location_id=location1.id,
                sku="PSU-500W",
                name="500W Power Supply",
                description="Standard ATX power supply",
                cost=Decimal("35.00"),
                price=Decimal("79.99"),
                quantity=10,
                min_quantity=2,
            ),
            Part(
                company_id=company.id,
                location_id=location1.id,
                sku="SCREEN-15-LCD",
                name='15.6" LCD Screen',
                description="Generic 15.6 inch laptop LCD panel",
                cost=Decimal("55.00"),
                price=Decimal("129.99"),
                quantity=5,
                min_quantity=2,
            ),
            Part(
                company_id=company.id,
                location_id=location1.id,
                sku="BATT-LAPTOP-GEN",
                name="Laptop Battery (Generic)",
                description="Universal laptop replacement battery",
                cost=Decimal("20.00"),
                price=Decimal("49.99"),
                quantity=12,
                min_quantity=3,
            ),
        ]
        db.add_all(parts)
        await db.flush()

        # Create sample customers
        customers = [
            Customer(
                company_id=company.id,
                first_name="Sarah",
                last_name="Johnson",
                email="sarah.johnson@email.test",
                phone="(555) 111-2222",
                address="789 Oak Lane, Downtown, TX 75001",
            ),
            Customer(
                company_id=company.id,
                first_name="Mike",
                last_name="Williams",
                email="mike.w@email.test",
                phone="(555) 333-4444",
                address="321 Pine St, Westside, TX 75002",
            ),
            Customer(
                company_id=company.id,
                first_name="Emily",
                last_name="Davis",
                email="emily.davis@email.test",
                phone="(555) 555-6666",
            ),
        ]
        db.add_all(customers)

        await db.commit()
        print("Database seeded successfully!")
        print("\nDemo accounts created:")
        print("  - owner@computercorner.test / Password123! (Owner)")
        print("  - manager@store1.test / Password123! (Manager)")
        print("  - tech@store1.test / Password123! (Technician)")
        print("  - cashier@store1.test / Password123! (Cashier)")


if __name__ == "__main__":
    asyncio.run(seed_database())
