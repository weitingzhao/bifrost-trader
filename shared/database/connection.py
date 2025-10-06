"""
Database Connection Utilities for Bifrost Trader

Provides database connection management and utilities for all microservices.
"""

import logging
import os
from contextlib import contextmanager
from typing import Any, Dict, List, Optional

import pandas as pd
import psycopg2
from sqlalchemy import create_engine, text

logger = logging.getLogger(__name__)


class DatabaseConfig:
    """Database configuration management."""

    def __init__(self):
        self.host = os.getenv("DB_HOST", "localhost")
        self.port = os.getenv("DB_PORT", "5432")
        self.dbname = os.getenv("DB_NAME", "bifrost_trader")
        self.user = os.getenv("DB_USERNAME", "postgres")
        self.password = os.getenv("DB_PASS", "")

    def get_connection_string(self) -> str:
        """Get SQLAlchemy connection string."""
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.dbname}"

    def get_psycopg2_params(self) -> Dict[str, Any]:
        """Get psycopg2 connection parameters."""
        return {
            "host": self.host,
            "port": self.port,
            "dbname": self.dbname,
            "user": self.user,
            "password": self.password,
        }


class DatabaseConnection:
    """Database connection manager."""

    def __init__(self, config: Optional[DatabaseConfig] = None):
        self.config = config or DatabaseConfig()
        self._engine = None
        self._connection = None

    @property
    def engine(self):
        """Get SQLAlchemy engine."""
        if self._engine is None:
            self._engine = create_engine(
                self.config.get_connection_string(),
                pool_size=10,
                max_overflow=20,
                pool_pre_ping=True,
                pool_recycle=3600,
            )
        return self._engine

    @contextmanager
    def get_connection(self):
        """Get psycopg2 connection with context manager."""
        conn = None
        try:
            conn = psycopg2.connect(**self.config.get_psycopg2_params())
            yield conn
        except Exception as e:
            if conn:
                conn.rollback()
            logger.error(f"Database connection error: {e}")
            raise
        finally:
            if conn:
                conn.close()

    def execute_query(
        self, query: str, params: Optional[tuple] = None
    ) -> List[Dict[str, Any]]:
        """Execute a SELECT query and return results."""
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                columns = [desc[0] for desc in cursor.description]
                results = []
                for row in cursor.fetchall():
                    results.append(dict(zip(columns, row)))
                return results

    def execute_insert(self, query: str, params: Optional[tuple] = None) -> int:
        """Execute an INSERT query and return affected rows."""
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                conn.commit()
                return cursor.rowcount

    def execute_update(self, query: str, params: Optional[tuple] = None) -> int:
        """Execute an UPDATE query and return affected rows."""
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                conn.commit()
                return cursor.rowcount

    def execute_delete(self, query: str, params: Optional[tuple] = None) -> int:
        """Execute a DELETE query and return affected rows."""
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                conn.commit()
                return cursor.rowcount

    def get_dataframe(self, query: str, params: Optional[tuple] = None) -> pd.DataFrame:
        """Execute query and return pandas DataFrame."""
        return pd.read_sql_query(query, self.engine, params=params)

    def test_connection(self) -> bool:
        """Test database connection."""
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT 1")
                    return True
        except Exception as e:
            logger.error(f"Database connection test failed: {e}")
            return False


class TimescaleDBManager:
    """TimescaleDB specific utilities."""

    def __init__(self, db_connection: DatabaseConnection):
        self.db = db_connection

    def create_hypertable(
        self, table_name: str, time_column: str, partition_column: Optional[str] = None
    ) -> bool:
        """Create a TimescaleDB hypertable."""
        try:
            if partition_column:
                query = f"""
                SELECT create_hypertable('{table_name}', '{time_column}', 
                                       chunk_time_interval => INTERVAL '1 day',
                                       partitioning_column => '{partition_column}',
                                       number_partitions => 4);
                """
            else:
                query = f"""
                SELECT create_hypertable('{table_name}', '{time_column}', 
                                       chunk_time_interval => INTERVAL '1 day');
                """

            self.db.execute_query(query)
            logger.info(f"Created hypertable for {table_name}")
            return True
        except Exception as e:
            logger.error(f"Failed to create hypertable for {table_name}: {e}")
            return False

    def add_compression_policy(
        self, table_name: str, compress_after: str = "7 days"
    ) -> bool:
        """Add compression policy to a hypertable."""
        try:
            query = f"""
            SELECT add_compression_policy('{table_name}', INTERVAL '{compress_after}');
            """
            self.db.execute_query(query)
            logger.info(f"Added compression policy for {table_name}")
            return True
        except Exception as e:
            logger.error(f"Failed to add compression policy for {table_name}: {e}")
            return False

    def create_continuous_aggregate(
        self, view_name: str, query: str, refresh_interval: str = "1 hour"
    ) -> bool:
        """Create a continuous aggregate view."""
        try:
            create_query = f"""
            CREATE MATERIALIZED VIEW {view_name}
            WITH (timescaledb.continuous) AS
            {query};
            """
            self.db.execute_query(create_query)

            # Add refresh policy
            refresh_query = f"""
            SELECT add_continuous_aggregate_policy('{view_name}',
                start_offset => INTERVAL '1 day',
                end_offset => INTERVAL '1 hour',
                schedule_interval => INTERVAL '{refresh_interval}');
            """
            self.db.execute_query(refresh_query)
            logger.info(f"Created continuous aggregate {view_name}")
            return True
        except Exception as e:
            logger.error(f"Failed to create continuous aggregate {view_name}: {e}")
            return False


class DatabaseSchemaManager:
    """Database schema management utilities."""

    def __init__(self, db_connection: DatabaseConnection):
        self.db = db_connection

    def get_table_schema(self, table_name: str) -> List[Dict[str, Any]]:
        """Get table schema information."""
        query = """
        SELECT 
            column_name,
            data_type,
            is_nullable,
            column_default,
            character_maximum_length,
            numeric_precision,
            numeric_scale
        FROM information_schema.columns 
        WHERE table_name = %s
        ORDER BY ordinal_position;
        """
        return self.db.execute_query(query, (table_name,))

    def get_table_indexes(self, table_name: str) -> List[Dict[str, Any]]:
        """Get table indexes information."""
        query = """
        SELECT 
            indexname,
            indexdef
        FROM pg_indexes 
        WHERE tablename = %s;
        """
        return self.db.execute_query(query, (table_name,))

    def get_table_constraints(self, table_name: str) -> List[Dict[str, Any]]:
        """Get table constraints information."""
        query = """
        SELECT 
            constraint_name,
            constraint_type,
            column_name
        FROM information_schema.table_constraints tc
        JOIN information_schema.constraint_column_usage ccu 
            ON tc.constraint_name = ccu.constraint_name
        WHERE tc.table_name = %s;
        """
        return self.db.execute_query(query, (table_name,))

    def export_schema(self, output_file: str) -> bool:
        """Export database schema to SQL file."""
        try:
            # Get all tables
            tables_query = """
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            ORDER BY table_name;
            """
            tables = self.db.execute_query(tables_query)

            schema_sql = []
            schema_sql.append("-- Bifrost Trader Database Schema")
            schema_sql.append("-- Generated automatically")
            schema_sql.append("")

            for table in tables:
                table_name = table["table_name"]
                schema_sql.append(f"-- Table: {table_name}")

                # Get table creation SQL
                create_query = f"""
                SELECT pg_get_tabledef('{table_name}');
                """
                result = self.db.execute_query(create_query)
                if result:
                    schema_sql.append(result[0]["pg_get_tabledef"])
                    schema_sql.append("")

            # Write to file
            with open(output_file, "w") as f:
                f.write("\n".join(schema_sql))

            logger.info(f"Schema exported to {output_file}")
            return True
        except Exception as e:
            logger.error(f"Failed to export schema: {e}")
            return False


# Global database connection instance
db_config = DatabaseConfig()
db_connection = DatabaseConnection(db_config)
timescale_manager = TimescaleDBManager(db_connection)
schema_manager = DatabaseSchemaManager(db_connection)


def get_db_connection() -> DatabaseConnection:
    """Get global database connection instance."""
    return db_connection


def get_timescale_manager() -> TimescaleDBManager:
    """Get TimescaleDB manager instance."""
    return timescale_manager


def get_schema_manager() -> DatabaseSchemaManager:
    """Get schema manager instance."""
    return schema_manager
