import asyncio
from sqlalchemy import text
from app.core.database import engine

async def fix():
    async with engine.begin() as conn:
        await conn.execute(text("UPDATE alembic_version SET version_num='0c7230ed6515'"))
    print("Database version fixed to 0c7230ed6515")

if __name__ == "__main__":
    asyncio.run(fix())
