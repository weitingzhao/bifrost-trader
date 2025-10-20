"""
Async Database Connection Manager for Data Service

This module provides async database connection management using SQLAlchemy 2.0+
with proper connection pooling and session management for FastAPI.
"""

import logging
import os
from contextlib import asynccontextmanager
from typing import AsyncGenerator, Optional

from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import NullPool

logger = logging.getLogger(__name__)


class DatabaseConfig:
    """Database configuration management."""

    def __init__(self):
        self.host = os.getenv("DB_HOST", "localhost")
        self.port = os.getenv("DB_PORT", "5432")
        self.dbname = os.getenv("DB_NAME", "bifrost_trader")
        self.user = os.getenv("DB_USERNAME", "postgres")
        self.password = os.getenv("DB_PASS", "")
        
        # Connection pool settings
        self.pool_size = int(os.getenv("DB_POOL_SIZE", "10"))
        self.max_overflow = int(os.getenv("DB_MAX_OVERFLOW", "20"))
        self.pool_timeout = int(os.getenv("DB_POOL_TIMEOUT", "30"))
        self.pool_recycle = int(os.getenv("DB_POOL_RECYCLE", "3600"))

    def get_async_connection_string(self) -> str:
        """Get async SQLAlchemy connection string."""
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.dbname}"

    def get_sync_connection_string(self) -> str:
        """Get sync SQLAlchemy connection string."""
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.dbname}"


class DatabaseManager:
    """Async database connection manager."""

    def __init__(self, config: Optional[DatabaseConfig] = None):
        self.config = config or DatabaseConfig()
        self._async_engine = None
        self._async_session_factory = None
        self._sync_engine = None

    @property
    def async_engine(self):
        """Get async SQLAlchemy engine."""
        if self._async_engine is None:
            self._async_engine = create_async_engine(
                self.config.get_async_connection_string(),
                pool_size=self.config.pool_size,
                max_overflow=self.config.max_overflow,
                pool_timeout=self.config.pool_timeout,
                pool_recycle=self.config.pool_recycle,
                pool_pre_ping=True,
                echo=os.getenv("DB_ECHO", "false").lower() == "true",
            )
        return self._async_engine

    @property
    def async_session_factory(self):
        """Get async session factory."""
        if self._async_session_factory is None:
            self._async_session_factory = async_sessionmaker(
                bind=self.async_engine,
                class_=AsyncSession,
                expire_on_commit=False,
            )
        return self._async_session_factory

    @property
    def sync_engine(self):
        """Get sync SQLAlchemy engine for migrations and admin tasks."""
        if self._sync_engine is None:
            self._sync_engine = create_engine(
                self.config.get_sync_connection_string(),
                pool_size=self.config.pool_size,
                max_overflow=self.config.max_overflow,
                pool_timeout=self.config.pool_timeout,
                pool_recycle=self.config.pool_recycle,
                pool_pre_ping=True,
                echo=os.getenv("DB_ECHO", "false").lower() == "true",
            )
        return self._sync_engine

    @asynccontextmanager
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """
        Get async database session with context manager.
        
        Yields:
            AsyncSession: Database session
        """
        async with self.async_session_factory() as session:
            try:
                yield session
            except Exception as e:
                await session.rollback()
                logger.error(f"Database session error: {e}")
                raise
            finally:
                await session.close()

    async def test_connection(self) -> bool:
        """
        Test database connection.
        
        Returns:
            bool: True if connection successful
        """
        try:
            async with self.get_session() as session:
                result = await session.execute(text("SELECT 1"))
                return result.scalar() == 1
        except Exception as e:
            logger.error(f"Database connection test failed: {e}")
            return False

    async def create_tables(self):
        """Create all tables."""
        from .models import Base
        
        async with self.async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def drop_tables(self):
        """Drop all tables."""
        from .models import Base
        
        async with self.async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

    async def close(self):
        """Close database connections."""
        if self._async_engine:
            await self._async_engine.dispose()
        if self._sync_engine:
            self._sync_engine.dispose()


# Global database manager instance
db_manager = DatabaseManager()


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency function to get database session for FastAPI.
    
    Yields:
        AsyncSession: Database session
    """
    async with db_manager.get_session() as session:
        yield session


async def init_database():
    """Initialize database connection and create tables."""
    try:
        # Test connection
        if await db_manager.test_connection():
            logger.info("Database connection successful")
            
            # Create tables
            await db_manager.create_tables()
            logger.info("Database tables created successfully")
        else:
            logger.error("Database connection failed")
            raise Exception("Database connection failed")
            
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        raise


async def close_database():
    """Close database connections."""
    await db_manager.close()
    logger.info("Database connections closed")




