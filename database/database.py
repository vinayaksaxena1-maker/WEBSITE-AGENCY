from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from config.config import settings
from core.logger import logger

Base = declarative_base()

class DatabaseManager:
    def __init__(self, db_url: str = settings.DATABASE_URL):
        self.db_url = db_url
        self.engine = create_async_engine(
            self.db_url,
            pool_size=20,
            max_overflow=10,
            pool_pre_ping=True
        )
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            expire_on_commit=False
        )

    async def verify_connection(self) -> bool:
        try:
            async with self.engine.connect() as conn:
                from sqlalchemy import text
                await conn.execute(text("SELECT 1"))
            logger.info("Database connection verified successfully.")
            return True
        except Exception as e:
            logger.error(f"Database connection verification failed: {e}", exc_info=True)
            return False

    async def close(self) -> None:
        await self.engine.dispose()
        logger.info("Database connection engine disposed.")

db_manager = DatabaseManager()
