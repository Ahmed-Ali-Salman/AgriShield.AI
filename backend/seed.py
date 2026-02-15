"""
AgriShield AI — Seed Data Script.

Creates demo data: an admin user, 5 sample suppliers, and sample risk scores.
Run: python seed.py
"""

import asyncio

from app.config import settings
from app.infrastructure.database.connection import async_session_factory, init_db, engine

# Import models so tables get created
from app.infrastructure.database.models.supplier_model import SupplierModel  # noqa
from app.infrastructure.database.models.user_model import UserModel  # noqa
from app.infrastructure.database.models.risk_score_model import RiskScoreModel  # noqa
from app.infrastructure.database.models.alert_model import AlertModel  # noqa
from app.infrastructure.database.models.anomaly_model import AnomalyModel  # noqa

from app.domain.entities.user import User, UserRole
from app.domain.entities.supplier import Supplier
from app.infrastructure.database.repositories.pg_user_repository import PgUserRepository
from app.infrastructure.database.repositories.pg_supplier_repository import PgSupplierRepository
from app.infrastructure.security.jwt_handler import JWTAuthService


SUPPLIERS = [
    {"name": "Nile Valley Grains", "country": "Egypt", "category": "grain", "contact_email": "info@nilevalley.eg", "website": "https://nilevalley.eg"},
    {"name": "Cairo Fresh Produce", "country": "Egypt", "category": "produce", "contact_email": "supply@cairofresh.com", "website": "https://cairofresh.com"},
    {"name": "Alexandria Dairy Co.", "country": "Egypt", "category": "dairy", "contact_email": "ops@alexdairy.eg", "website": "https://alexdairy.eg"},
    {"name": "Red Sea Logistics", "country": "Egypt", "category": "logistics", "contact_email": "info@redsealogistics.com", "website": "https://redsealogistics.com"},
    {"name": "East Africa Spices Ltd.", "country": "Kenya", "category": "spices", "contact_email": "trade@easpices.ke", "website": "https://easpices.ke"},
]


async def seed():
    await init_db()
    print("✅ Tables created")

    async with async_session_factory() as session:
        try:
            user_repo = PgUserRepository(session)
            supplier_repo = PgSupplierRepository(session)
            auth_service = JWTAuthService()

            # --- Create admin user ---
            existing = await user_repo.get_by_email("admin@agrishield.ai")
            if existing:
                print("⏭️  Admin user already exists, skipping user creation")
            else:
                admin = User(
                    email="admin@agrishield.ai",
                    hashed_password=auth_service.hash_password("admin123"),
                    full_name="Admin User",
                    role=UserRole.ADMIN,
                )
                await user_repo.create(admin)
                print(f"👤 Created admin user: admin@agrishield.ai / admin123")

            # --- Create sample suppliers ---
            existing_suppliers = await supplier_repo.get_all(skip=0, limit=1)
            if existing_suppliers:
                print("⏭️  Suppliers already exist, skipping")
            else:
                for s_data in SUPPLIERS:
                    supplier = Supplier(**s_data)
                    created = await supplier_repo.create(supplier)
                    print(f"🏭 Created supplier: {created.name} ({created.country})")

            await session.commit()
            print("\n🎉 Seed data created successfully!")
            print("   Login with: admin@agrishield.ai / admin123")

        except Exception as e:
            await session.rollback()
            print(f"❌ Error: {e}")
            raise


if __name__ == "__main__":
    asyncio.run(seed())
