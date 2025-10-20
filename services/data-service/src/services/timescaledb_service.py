"""
TimescaleDB Integration Service for Data Service

This module provides TimescaleDB-specific operations including hypertable creation,
compression policies, and continuous aggregates for optimal time-series performance.
"""

import logging
from typing import Dict, List, Optional, Any

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)


class TimescaleDBService:
    """Service for TimescaleDB-specific operations."""

    def __init__(self, db_session: AsyncSession):
        self.db = db_session

    async def create_hypertable(
        self,
        table_name: str,
        time_column: str = "time",
        partition_column: Optional[str] = None,
        chunk_time_interval: str = "1 day",
        number_partitions: int = 4
    ) -> bool:
        """
        Create a TimescaleDB hypertable.
        
        Args:
            table_name: Name of the table to convert to hypertable
            time_column: Name of the time column
            partition_column: Optional partition column (e.g., 'symbol')
            chunk_time_interval: Time interval for chunks
            number_partitions: Number of partitions if using partition_column
            
        Returns:
            bool: True if successful
        """
        try:
            if partition_column:
                query = text(f"""
                    SELECT create_hypertable(
                        '{table_name}', 
                        '{time_column}',
                        chunk_time_interval => INTERVAL '{chunk_time_interval}',
                        partitioning_column => '{partition_column}',
                        number_partitions => {number_partitions}
                    );
                """)
            else:
                query = text(f"""
                    SELECT create_hypertable(
                        '{table_name}', 
                        '{time_column}',
                        chunk_time_interval => INTERVAL '{chunk_time_interval}'
                    );
                """)

            await self.db.execute(query)
            await self.db.commit()
            
            logger.info(f"Created hypertable for {table_name}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to create hypertable for {table_name}: {e}")
            await self.db.rollback()
            return False

    async def add_compression_policy(
        self,
        table_name: str,
        compress_after: str = "7 days",
        segment_by: Optional[str] = None,
        order_by: Optional[str] = None
    ) -> bool:
        """
        Add compression policy to a hypertable.
        
        Args:
            table_name: Name of the hypertable
            compress_after: Time after which to compress data
            segment_by: Column to segment by for compression
            order_by: Column to order by for compression
            
        Returns:
            bool: True if successful
        """
        try:
            if segment_by and order_by:
                query = text(f"""
                    ALTER TABLE {table_name} SET (
                        timescaledb.compress,
                        timescaledb.compress_segmentby = '{segment_by}',
                        timescaledb.compress_orderby = '{order_by}'
                    );
                    
                    SELECT add_compression_policy('{table_name}', INTERVAL '{compress_after}');
                """)
            elif segment_by:
                query = text(f"""
                    ALTER TABLE {table_name} SET (
                        timescaledb.compress,
                        timescaledb.compress_segmentby = '{segment_by}'
                    );
                    
                    SELECT add_compression_policy('{table_name}', INTERVAL '{compress_after}');
                """)
            else:
                query = text(f"""
                    ALTER TABLE {table_name} SET (timescaledb.compress);
                    SELECT add_compression_policy('{table_name}', INTERVAL '{compress_after}');
                """)

            await self.db.execute(query)
            await self.db.commit()
            
            logger.info(f"Added compression policy for {table_name}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to add compression policy for {table_name}: {e}")
            await self.db.rollback()
            return False

    async def create_continuous_aggregate(
        self,
        view_name: str,
        query: str,
        refresh_interval: str = "1 hour",
        start_offset: str = "1 day",
        end_offset: str = "1 hour"
    ) -> bool:
        """
        Create a continuous aggregate view.
        
        Args:
            view_name: Name of the continuous aggregate view
            query: SQL query for the aggregate
            refresh_interval: How often to refresh the aggregate
            start_offset: Start offset for refresh policy
            end_offset: End offset for refresh policy
            
        Returns:
            bool: True if successful
        """
        try:
            # Create the continuous aggregate
            create_query = text(f"""
                CREATE MATERIALIZED VIEW {view_name}
                WITH (timescaledb.continuous) AS
                {query};
            """)
            
            await self.db.execute(create_query)
            
            # Add refresh policy
            refresh_query = text(f"""
                SELECT add_continuous_aggregate_policy(
                    '{view_name}',
                    start_offset => INTERVAL '{start_offset}',
                    end_offset => INTERVAL '{end_offset}',
                    schedule_interval => INTERVAL '{refresh_interval}'
                );
            """)
            
            await self.db.execute(refresh_query)
            await self.db.commit()
            
            logger.info(f"Created continuous aggregate {view_name}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to create continuous aggregate {view_name}: {e}")
            await self.db.rollback()
            return False

    async def add_retention_policy(
        self,
        table_name: str,
        retention_period: str = "1 year"
    ) -> bool:
        """
        Add data retention policy to a hypertable.
        
        Args:
            table_name: Name of the hypertable
            retention_period: How long to keep data
            
        Returns:
            bool: True if successful
        """
        try:
            query = text(f"""
                SELECT add_retention_policy('{table_name}', INTERVAL '{retention_period}');
            """)
            
            await self.db.execute(query)
            await self.db.commit()
            
            logger.info(f"Added retention policy for {table_name}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to add retention policy for {table_name}: {e}")
            await self.db.rollback()
            return False

    async def get_hypertable_info(self, table_name: str) -> Optional[Dict[str, Any]]:
        """
        Get information about a hypertable.
        
        Args:
            table_name: Name of the hypertable
            
        Returns:
            Dictionary with hypertable information or None if not found
        """
        try:
            query = text("""
                SELECT 
                    schemaname,
                    tablename,
                    num_dimensions,
                    chunk_sizing_func,
                    num_chunks,
                    compression_enabled,
                    is_distributed
                FROM timescaledb_information.hypertables 
                WHERE tablename = :table_name;
            """)
            
            result = await self.db.execute(query, {"table_name": table_name})
            row = result.fetchone()
            
            if row:
                return {
                    "schema": row[0],
                    "table": row[1],
                    "dimensions": row[2],
                    "chunk_sizing_func": row[3],
                    "chunks": row[4],
                    "compression_enabled": row[5],
                    "is_distributed": row[6]
                }
            
            return None
            
        except Exception as e:
            logger.error(f"Failed to get hypertable info for {table_name}: {e}")
            return None

    async def get_chunk_info(self, table_name: str) -> List[Dict[str, Any]]:
        """
        Get information about chunks in a hypertable.
        
        Args:
            table_name: Name of the hypertable
            
        Returns:
            List of dictionaries with chunk information
        """
        try:
            query = text("""
                SELECT 
                    chunk_schema,
                    chunk_name,
                    range_start,
                    range_end,
                    is_compressed,
                    chunk_tablespace,
                    data_nodes
                FROM timescaledb_information.chunks 
                WHERE hypertable_name = :table_name
                ORDER BY range_start;
            """)
            
            result = await self.db.execute(query, {"table_name": table_name})
            rows = result.fetchall()
            
            chunks = []
            for row in rows:
                chunks.append({
                    "schema": row[0],
                    "name": row[1],
                    "range_start": row[2],
                    "range_end": row[3],
                    "is_compressed": row[4],
                    "tablespace": row[5],
                    "data_nodes": row[6]
                })
            
            return chunks
            
        except Exception as e:
            logger.error(f"Failed to get chunk info for {table_name}: {e}")
            return []

    async def setup_market_data_hypertables(self) -> Dict[str, bool]:
        """
        Set up all market data hypertables with optimal configuration.
        
        Returns:
            Dictionary with setup results for each table
        """
        results = {}
        
        # Market data hypertables configuration
        hypertables_config = [
            {
                "table": "market_stock_hist_bars_min_ts",
                "time_column": "time",
                "partition_column": "symbol",
                "chunk_interval": "1 day",
                "compression_after": "1 day",
                "retention": "6 months"
            },
            {
                "table": "market_stock_hist_bars_hour_ts", 
                "time_column": "time",
                "partition_column": "symbol",
                "chunk_interval": "7 days",
                "compression_after": "7 days",
                "retention": "2 years"
            },
            {
                "table": "market_stock_hist_bars_day_ts",
                "time_column": "time", 
                "partition_column": "symbol",
                "chunk_interval": "30 days",
                "compression_after": "30 days",
                "retention": "10 years"
            }
        ]
        
        for config in hypertables_config:
            table_name = config["table"]
            
            # Create hypertable
            hypertable_result = await self.create_hypertable(
                table_name=table_name,
                time_column=config["time_column"],
                partition_column=config["partition_column"],
                chunk_time_interval=config["chunk_interval"]
            )
            
            if hypertable_result:
                # Add compression policy
                compression_result = await self.add_compression_policy(
                    table_name=table_name,
                    compress_after=config["compression_after"],
                    segment_by=config["partition_column"],
                    order_by=config["time_column"]
                )
                
                # Add retention policy
                retention_result = await self.add_retention_policy(
                    table_name=table_name,
                    retention_period=config["retention"]
                )
                
                results[table_name] = all([hypertable_result, compression_result, retention_result])
            else:
                results[table_name] = False
        
        return results

    async def create_market_data_aggregates(self) -> Dict[str, bool]:
        """
        Create continuous aggregates for market data analysis.
        
        Returns:
            Dictionary with creation results for each aggregate
        """
        results = {}
        
        # Daily OHLCV aggregate from minute data
        daily_ohlcv_query = """
            SELECT 
                time_bucket('1 day', time) AS day,
                symbol,
                first(open, time) AS open,
                max(high) AS high,
                min(low) AS low,
                last(close, time) AS close,
                sum(volume) AS volume
            FROM market_stock_hist_bars_min_ts
            GROUP BY day, symbol;
        """
        
        daily_result = await self.create_continuous_aggregate(
            view_name="market_daily_ohlcv",
            query=daily_ohlcv_query,
            refresh_interval="1 hour"
        )
        results["market_daily_ohlcv"] = daily_result
        
        # Hourly OHLCV aggregate from minute data
        hourly_ohlcv_query = """
            SELECT 
                time_bucket('1 hour', time) AS hour,
                symbol,
                first(open, time) AS open,
                max(high) AS high,
                min(low) AS low,
                last(close, time) AS close,
                sum(volume) AS volume
            FROM market_stock_hist_bars_min_ts
            GROUP BY hour, symbol;
        """
        
        hourly_result = await self.create_continuous_aggregate(
            view_name="market_hourly_ohlcv",
            query=hourly_ohlcv_query,
            refresh_interval="15 minutes"
        )
        results["market_hourly_ohlcv"] = hourly_result
        
        return results

    async def get_compression_stats(self, table_name: str) -> Optional[Dict[str, Any]]:
        """
        Get compression statistics for a hypertable.
        
        Args:
            table_name: Name of the hypertable
            
        Returns:
            Dictionary with compression statistics or None if not found
        """
        try:
            query = text("""
                SELECT 
                    before_compression_total_bytes,
                    after_compression_total_bytes,
                    node_name
                FROM timescaledb_information.compression_stats 
                WHERE hypertable_name = :table_name;
            """)
            
            result = await self.db.execute(query, {"table_name": table_name})
            row = result.fetchone()
            
            if row:
                before_bytes = row[0] or 0
                after_bytes = row[1] or 0
                compression_ratio = (before_bytes - after_bytes) / before_bytes if before_bytes > 0 else 0
                
                return {
                    "before_compression_bytes": before_bytes,
                    "after_compression_bytes": after_bytes,
                    "compression_ratio": compression_ratio,
                    "space_saved_bytes": before_bytes - after_bytes,
                    "node_name": row[2]
                }
            
            return None
            
        except Exception as e:
            logger.error(f"Failed to get compression stats for {table_name}: {e}")
            return None

    async def optimize_hypertables(self) -> Dict[str, Any]:
        """
        Optimize all hypertables by running maintenance tasks.
        
        Returns:
            Dictionary with optimization results
        """
        results = {
            "vacuum_results": {},
            "analyze_results": {},
            "reindex_results": {}
        }
        
        # Get all hypertables
        query = text("""
            SELECT tablename 
            FROM timescaledb_information.hypertables;
        """)
        
        result = await self.db.execute(query)
        hypertables = [row[0] for row in result.fetchall()]
        
        for table in hypertables:
            try:
                # VACUUM
                vacuum_query = text(f"VACUUM ANALYZE {table};")
                await self.db.execute(vacuum_query)
                results["vacuum_results"][table] = True
                
                # ANALYZE
                analyze_query = text(f"ANALYZE {table};")
                await self.db.execute(analyze_query)
                results["analyze_results"][table] = True
                
                # REINDEX (if needed)
                reindex_query = text(f"REINDEX TABLE {table};")
                await self.db.execute(reindex_query)
                results["reindex_results"][table] = True
                
            except Exception as e:
                logger.error(f"Failed to optimize {table}: {e}")
                results["vacuum_results"][table] = False
                results["analyze_results"][table] = False
                results["reindex_results"][table] = False
        
        await self.db.commit()
        return results




