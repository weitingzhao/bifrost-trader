"""
Development configuration for Bifrost Trader.
Provides easy access to Smart Trader components during migration and sets up Python paths.
"""

import os
import sys
from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
BIFROST_ROOT = Path(__file__).parent.parent
SMART_TRADER_ROOT = PROJECT_ROOT / "smart-trader"

# Ensure smart-trader is accessible
if not SMART_TRADER_ROOT.exists():
    raise FileNotFoundError(f"Smart Trader project not found at {SMART_TRADER_ROOT}")

# Add paths to Python path for development
paths_to_add = [
    str(BIFROST_ROOT),
    str(SMART_TRADER_ROOT),
    str(BIFROST_ROOT / "shared"),
    str(BIFROST_ROOT / "services" / "data-service" / "src"),
    str(BIFROST_ROOT / "services" / "portfolio-service" / "src"),
    str(BIFROST_ROOT / "services" / "strategy-service" / "src"),
    str(BIFROST_ROOT / "services" / "risk-service" / "src"),
    str(BIFROST_ROOT / "services" / "ml-service" / "src"),
    str(BIFROST_ROOT / "services" / "analytics-service" / "src"),
    str(BIFROST_ROOT / "services" / "compliance-service" / "src"),
    str(BIFROST_ROOT / "services" / "news-service" / "src"),
    str(BIFROST_ROOT / "services" / "microstructure-service" / "src"),
    str(BIFROST_ROOT / "services" / "web-portal" / "src"),
    str(BIFROST_ROOT / "services" / "api-gateway"),
]

# Add paths that don't already exist
for path in paths_to_add:
    if os.path.exists(path) and path not in sys.path:
        sys.path.insert(0, path)

# Set environment variables for easy access
os.environ.setdefault("BIFROST_ROOT", str(BIFROST_ROOT))
os.environ.setdefault("SMART_TRADER_ROOT", str(SMART_TRADER_ROOT))
os.environ.setdefault("PROJECT_ROOT", str(PROJECT_ROOT))

# Smart Trader component paths for easy reference
SMART_TRADER_PATHS = {
    # Models
    "models": {
        "market": SMART_TRADER_ROOT / "apps" / "common" / "models" / "market.py",
        "market_stock": SMART_TRADER_ROOT
        / "apps"
        / "common"
        / "models"
        / "market_stock.py",
        "portfolio": SMART_TRADER_ROOT / "apps" / "common" / "models" / "portfolio.py",
        "strategy": SMART_TRADER_ROOT / "apps" / "common" / "models" / "strategy.py",
        "screening": SMART_TRADER_ROOT / "apps" / "common" / "models" / "screening.py",
        "main": SMART_TRADER_ROOT / "apps" / "common" / "models" / "main.py",
        "wishlist": SMART_TRADER_ROOT / "apps" / "common" / "models" / "wishlist.py",
    },
    # Services
    "services": {
        "fetching": SMART_TRADER_ROOT / "business" / "services" / "fetching",
        "engines": SMART_TRADER_ROOT / "business" / "engines",
        "research": SMART_TRADER_ROOT / "business" / "researchs",
    },
    # Views
    "views": {
        "position": SMART_TRADER_ROOT / "home" / "views" / "position",
        "cash_flow": SMART_TRADER_ROOT / "home" / "views" / "cash_flow",
        "api": SMART_TRADER_ROOT / "apps" / "api",
    },
    # Strategy Framework
    "strategy": {
        "cerebro": SMART_TRADER_ROOT / "cerebro",
        "backtrader": SMART_TRADER_ROOT / "backtrader",
    },
    # Tasks
    "tasks": {
        "controller": SMART_TRADER_ROOT / "apps" / "tasks" / "controller",
    },
    # Configuration
    "config": {
        "settings": SMART_TRADER_ROOT / "core" / "settings.py",
        "requirements": SMART_TRADER_ROOT / "requirements.txt",
    },
}

# Bifrost Trader service paths
BIFROST_SERVICE_PATHS = {
    "data_service": BIFROST_ROOT / "services" / "data-service",
    "portfolio_service": BIFROST_ROOT / "services" / "portfolio-service",
    "strategy_service": BIFROST_ROOT / "services" / "strategy-service",
    "risk_service": BIFROST_ROOT / "services" / "risk-service",
    "ml_service": BIFROST_ROOT / "services" / "ml-service",
    "analytics_service": BIFROST_ROOT / "services" / "analytics-service",
    "compliance_service": BIFROST_ROOT / "services" / "compliance-service",
    "news_service": BIFROST_ROOT / "services" / "news-service",
    "microstructure_service": BIFROST_ROOT / "services" / "microstructure-service",
    "web_portal": BIFROST_ROOT / "services" / "web-portal",
    "api_gateway": BIFROST_ROOT / "services" / "api-gateway",
}


def get_smart_trader_path(category: str, component: str) -> Path:
    """Get path to Smart Trader component."""
    if category not in SMART_TRADER_PATHS:
        raise KeyError(f"Category '{category}' not found")
    if component not in SMART_TRADER_PATHS[category]:
        raise KeyError(f"Component '{component}' not found in category '{category}'")
    return SMART_TRADER_PATHS[category][component]


def get_bifrost_service_path(service: str) -> Path:
    """Get path to Bifrost Trader service."""
    if service not in BIFROST_SERVICE_PATHS:
        raise KeyError(f"Service '{service}' not found")
    return BIFROST_SERVICE_PATHS[service]


def copy_smart_trader_reference(
    category: str, component: str, target_service: str, target_name: str = None
):
    """Copy Smart Trader component as reference to Bifrost service."""
    source_path = get_smart_trader_path(category, component)
    target_service_path = get_bifrost_service_path(target_service)

    if target_name is None:
        target_name = f"{component}_reference.py"

    target_path = target_service_path / "src" / "models" / target_name

    # Create target directory if it doesn't exist
    target_path.parent.mkdir(parents=True, exist_ok=True)

    # Copy file
    import shutil

    shutil.copy2(source_path, target_path)

    print(f"Copied {source_path} -> {target_path}")
    return target_path


def list_available_components():
    """List all available Smart Trader components."""
    print("Available Smart Trader Components:")
    print("=" * 50)

    for category, components in SMART_TRADER_PATHS.items():
        print(f"\n{category.upper()}:")
        for component, path in components.items():
            status = "✓" if path.exists() else "✗"
            print(f"  {status} {component}: {path}")


def list_bifrost_services():
    """List all Bifrost Trader services."""
    print("Available Bifrost Trader Services:")
    print("=" * 50)

    for service, path in BIFROST_SERVICE_PATHS.items():
        status = "✓" if path.exists() else "✗"
        print(f"  {status} {service}: {path}")


# Example usage functions
def migrate_market_models():
    """Example: Migrate market models from Smart Trader to Data Service."""
    try:
        copy_smart_trader_reference(
            "models", "market", "data_service", "market_reference.py"
        )
        copy_smart_trader_reference(
            "models", "market_stock", "data_service", "market_stock_reference.py"
        )
        print("Market models copied to data service")
    except Exception as e:
        print(f"Error migrating market models: {e}")


def migrate_portfolio_models():
    """Example: Migrate portfolio models from Smart Trader to Portfolio Service."""
    try:
        copy_smart_trader_reference(
            "models", "portfolio", "portfolio_service", "portfolio_reference.py"
        )
        copy_smart_trader_reference(
            "models", "wishlist", "portfolio_service", "wishlist_reference.py"
        )
        print("Portfolio models copied to portfolio service")
    except Exception as e:
        print(f"Error migrating portfolio models: {e}")


def migrate_strategy_models():
    """Example: Migrate strategy models from Smart Trader to Strategy Service."""
    try:
        copy_smart_trader_reference(
            "models", "strategy", "strategy_service", "strategy_reference.py"
        )
        copy_smart_trader_reference(
            "models", "screening", "strategy_service", "screening_reference.py"
        )
        print("Strategy models copied to strategy service")
    except Exception as e:
        print(f"Error migrating strategy models: {e}")


if __name__ == "__main__":
    print("Bifrost Trader Development Configuration")
    print("=" * 50)
    print(f"Project Root: {PROJECT_ROOT}")
    print(f"Bifrost Root: {BIFROST_ROOT}")
    print(f"Smart Trader Root: {SMART_TRADER_ROOT}")
    print()

    list_available_components()
    print()
    list_bifrost_services()

    print("\nExample migration commands:")
    print("  migrate_market_models()")
    print("  migrate_portfolio_models()")
    print("  migrate_strategy_models()")
