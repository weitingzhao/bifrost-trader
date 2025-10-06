"""
Shared utilities for Bifrost Trader services.
Common utilities used across all microservices.
"""

import asyncio
import json
import logging
import os
from datetime import datetime, timedelta
from typing import Any, Dict, Optional

import httpx
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import redis


def get_database_connection():
    """Get database connection using SQLAlchemy."""
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        # Fallback to individual components
        db_engine = os.getenv("DB_ENGINE", "postgresql")
        db_name = os.getenv("DB_NAME", "bifrost_trader")
        db_username = os.getenv("DB_USERNAME", "postgres")
        db_pass = os.getenv("DB_PASS", "password")
        db_host = os.getenv("DB_HOST", "localhost")
        db_port = os.getenv("DB_PORT", "5432")

        database_url = (
            f"{db_engine}://{db_username}:{db_pass}@{db_host}:{db_port}/{db_name}"
        )

    engine = create_engine(database_url)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal()


def get_redis_connection():
    """Get Redis connection."""
    redis_url = os.getenv("REDIS_URL")
    if not redis_url:
        redis_host = os.getenv("REDIS_HOST", "localhost")
        redis_port = int(os.getenv("REDIS_PORT", 6379))
        redis_url = f"redis://{redis_host}:{redis_port}/0"

    return redis.from_url(redis_url)


def setup_logging(service_name: str, log_level: str = "INFO") -> logging.Logger:
    """Setup structured logging for a service."""
    logger = logging.getLogger(service_name)
    logger.setLevel(getattr(logging, log_level.upper()))

    # Create formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger


class ServiceClient:
    """HTTP client for inter-service communication."""

    def __init__(self, service_url: str, timeout: int = 30):
        self.service_url = service_url
        self.timeout = timeout
        self.client = httpx.AsyncClient(timeout=timeout)

    async def get(self, endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Make GET request to service."""
        try:
            response = await self.client.get(
                f"{self.service_url}{endpoint}", params=params
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            raise Exception(f"HTTP error calling {self.service_url}{endpoint}: {e}")

    async def post(self, endpoint: str, data: Optional[Dict] = None) -> Dict[str, Any]:
        """Make POST request to service."""
        try:
            response = await self.client.post(
                f"{self.service_url}{endpoint}", json=data
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            raise Exception(f"HTTP error calling {self.service_url}{endpoint}: {e}")

    async def put(self, endpoint: str, data: Optional[Dict] = None) -> Dict[str, Any]:
        """Make PUT request to service."""
        try:
            response = await self.client.put(f"{self.service_url}{endpoint}", json=data)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            raise Exception(f"HTTP error calling {self.service_url}{endpoint}: {e}")

    async def delete(self, endpoint: str) -> Dict[str, Any]:
        """Make DELETE request to service."""
        try:
            response = await self.client.delete(f"{self.service_url}{endpoint}")
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            raise Exception(f"HTTP error calling {self.service_url}{endpoint}: {e}")

    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()


class ServiceRegistry:
    """Service registry for managing service URLs."""

    def __init__(self):
        self.services = {
            "data-service": os.getenv("DATA_SERVICE_URL", "http://10.0.0.75:8001"),
            "portfolio-service": os.getenv(
                "PORTFOLIO_SERVICE_URL", "http://10.0.0.80:8002"
            ),
            "strategy-service": os.getenv(
                "STRATEGY_SERVICE_URL", "http://10.0.0.60:8003"
            ),
            "risk-service": os.getenv("RISK_SERVICE_URL", "http://10.0.0.80:8004"),
            "ml-service": os.getenv("ML_SERVICE_URL", "http://10.0.0.60:8005"),
            "analytics-service": os.getenv(
                "ANALYTICS_SERVICE_URL", "http://10.0.0.60:8006"
            ),
            "compliance-service": os.getenv(
                "COMPLIANCE_SERVICE_URL", "http://10.0.0.80:8007"
            ),
            "news-service": os.getenv("NEWS_SERVICE_URL", "http://10.0.0.75:8008"),
            "microstructure-service": os.getenv(
                "MICROSTRUCTURE_SERVICE_URL", "http://10.0.0.60:8009"
            ),
            "web-portal": os.getenv("WEB_PORTAL_URL", "http://10.0.0.75:8010"),
            "api-gateway": os.getenv("API_GATEWAY_URL", "http://10.0.0.75:8000"),
        }

    def get_service_url(self, service_name: str) -> str:
        """Get service URL by name."""
        return self.services.get(service_name, "")

    def get_service_client(self, service_name: str) -> ServiceClient:
        """Get service client by name."""
        service_url = self.get_service_url(service_name)
        if not service_url:
            raise ValueError(f"Service {service_name} not found in registry")
        return ServiceClient(service_url)


class CacheManager:
    """Redis-based cache manager."""

    def __init__(self):
        self.redis_client = get_redis_connection()

    def get(self, key: str) -> Optional[str]:
        """Get value from cache."""
        try:
            return self.redis_client.get(key)
        except Exception:
            return None

    def set(self, key: str, value: str, expire: int = 3600) -> bool:
        """Set value in cache with expiration."""
        try:
            self.redis_client.setex(key, expire, value)
            return True
        except Exception:
            return False

    def delete(self, key: str) -> bool:
        """Delete key from cache."""
        try:
            self.redis_client.delete(key)
            return True
        except Exception:
            return False

    def exists(self, key: str) -> bool:
        """Check if key exists in cache."""
        try:
            return bool(self.redis_client.exists(key))
        except Exception:
            return False


class HealthChecker:
    """Health check utilities for services."""

    def __init__(self, service_name: str):
        self.service_name = service_name
        self.start_time = datetime.now()
        self.logger = setup_logging(f"{service_name}-health")

    def get_uptime(self) -> float:
        """Get service uptime in seconds."""
        return (datetime.now() - self.start_time).total_seconds()

    def check_database(self) -> bool:
        """Check database connectivity."""
        try:
            db = get_database_connection()
            db.execute("SELECT 1")
            db.close()
            return True
        except Exception as e:
            self.logger.error(f"Database health check failed: {e}")
            return False

    def check_redis(self) -> bool:
        """Check Redis connectivity."""
        try:
            redis_client = get_redis_connection()
            redis_client.ping()
            return True
        except Exception as e:
            self.logger.error(f"Redis health check failed: {e}")
            return False

    def get_health_status(self) -> Dict[str, Any]:
        """Get comprehensive health status."""
        return {
            "service": self.service_name,
            "status": "healthy",
            "uptime": self.get_uptime(),
            "timestamp": datetime.now().isoformat(),
            "checks": {
                "database": self.check_database(),
                "redis": self.check_redis(),
            },
        }


class RateLimiter:
    """Rate limiting utility."""

    def __init__(
        self, redis_client: redis.Redis, max_requests: int = 100, window: int = 3600
    ):
        self.redis_client = redis_client
        self.max_requests = max_requests
        self.window = window

    def is_allowed(self, key: str) -> bool:
        """Check if request is allowed based on rate limit."""
        try:
            current_time = datetime.now()
            window_start = current_time - timedelta(seconds=self.window)

            # Clean old entries
            self.redis_client.zremrangebyscore(key, 0, window_start.timestamp())

            # Count current requests
            current_requests = self.redis_client.zcard(key)

            if current_requests < self.max_requests:
                # Add current request
                self.redis_client.zadd(
                    key, {str(current_time.timestamp()): current_time.timestamp()}
                )
                return True

            return False
        except Exception:
            return True  # Allow on error


class MessagePublisher:
    """Message publisher for inter-service communication."""

    def __init__(self, redis_client: redis.Redis):
        self.redis_client = redis_client

    def publish(self, channel: str, message: Dict[str, Any]) -> bool:
        """Publish message to channel."""
        try:
            self.redis_client.publish(channel, json.dumps(message))
            return True
        except Exception:
            return False

    def subscribe(self, channel: str, callback):
        """Subscribe to channel with callback."""
        try:
            pubsub = self.redis_client.pubsub()
            pubsub.subscribe(channel)

            for message in pubsub.listen():
                if message["type"] == "message":
                    data = json.loads(message["data"])
                    callback(data)
        except Exception as e:
            logging.error(f"Subscription error: {e}")


def load_environment():
    """Load environment variables from .env file."""
    from dotenv import load_dotenv

    load_dotenv()


def get_service_config(service_name: str) -> Dict[str, Any]:
    """Get service configuration."""
    return {
        "service_name": service_name,
        "version": "1.0.0",
        "environment": os.getenv("ENVIRONMENT", "development"),
        "debug": os.getenv("DEBUG", "False").lower() == "true",
        "log_level": os.getenv("LOG_LEVEL", "INFO"),
    }


def validate_required_env_vars(required_vars: list) -> bool:
    """Validate that required environment variables are set."""
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)

    if missing_vars:
        raise ValueError(
            f"Missing required environment variables: {', '.join(missing_vars)}"
        )

    return True
