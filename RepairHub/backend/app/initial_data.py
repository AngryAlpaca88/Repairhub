import asyncio
import logging

from app.db.session import AsyncSessionLocal
from app.models.user import User, UserRole
from app.models.company import Company, Location
from app.models.inventory import Part, Supplier, InventoryItem
from app.models.service import ServiceDefinition
from app.core.security import get_password_hash

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def init_db():
    async with AsyncSessionLocal() as db:
        # 1. Create Company
        company = Company(name="Computer Corner")
        db.add(company)
        await db.flush()
        
        # 2. Create Locations
        loc1 = Location(company_id=company.id, name="Computer Corner HQ", address="123 Main St")
        loc2 = Location(company_id=company.id, name="Computer Corner North", address="456 North Ave")
        loc3 = Location(company_id=company.id, name="Computer Corner South", address="789 South Blvd")
        db.add_all([loc1, loc2, loc3])
        await db.flush()
        
        # 3. Create Users
        owner = User(
            email="owner@computercorner.com",
            hashed_password=get_password_hash("admin123"),
            full_name="Big Boss",
            role=UserRole.OWNER,
            primary_location_id=loc1.id
        )
        manager = User(
            email="manager@computercorner.com",
            hashed_password=get_password_hash("manager123"),
            full_name="Store Manager",
            role=UserRole.STORE_MANAGER,
            primary_location_id=loc1.id
        )
        tech = User(
            email="tech@computercorner.com",
            hashed_password=get_password_hash("tech123"),
            full_name="Fix It Felix",
            role=UserRole.TECHNICIAN,
            primary_location_id=loc1.id
        )
        db.add_all([owner, manager, tech])
        
        # 4. Create Supplier & Parts
        supplier = Supplier(name="MobileSentrix")
        db.add(supplier)
        await db.flush()
        
        screen = Part(
            supplier_id=supplier.id,
            name="iPhone 11 Screen (Premium)",
            category="Screen",
            sku="IP11-LCD-PREM",
            cost=25.00,
            list_price=60.00
        )
        battery = Part(
            supplier_id=supplier.id,
            name="iPhone 11 Battery",
            category="Battery",
            sku="IP11-BATT",
            cost=10.00,
            list_price=30.00
        )
        db.add_all([screen, battery])
        await db.flush()
        
        # 5. Inventory
        inv1 = InventoryItem(location_id=loc1.id, part_id=screen.id, quantity_on_hand=10)
        inv2 = InventoryItem(location_id=loc1.id, part_id=battery.id, quantity_on_hand=5)
        db.add_all([inv1, inv2])
        
        # 6. Services
        svc1 = ServiceDefinition(name="iPhone 11 Screen Repair", default_price=140.00) # 140 - 25 = 115 profit (>100)
        svc2 = ServiceDefinition(name="iPhone 11 Battery Replacement", default_price=80.00) # 80 - 10 = 70 profit (<100, should trigger warning)
        db.add_all([svc1, svc2])
        
        await db.commit()
        logger.info("Initial data created")

if __name__ == "__main__":
    asyncio.run(init_db())
