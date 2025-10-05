"""
Python path configuration for Bifrost Trader development.
This file ensures that both bifrost-trader and smart-trader can be imported.
"""

import sys
import os
from pathlib import Path

# Get the project root directory
PROJECT_ROOT = Path(__file__).parent.parent.parent
BIFROST_ROOT = Path(__file__).parent.parent
SMART_TRADER_ROOT = PROJECT_ROOT / "smart-trader"

# Add paths to Python path
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
os.environ.setdefault('BIFROST_ROOT', str(BIFROST_ROOT))
os.environ.setdefault('SMART_TRADER_ROOT', str(SMART_TRADER_ROOT))
os.environ.setdefault('PROJECT_ROOT', str(PROJECT_ROOT))

# Print configuration for debugging
if __name__ == "__main__":
    print("Python Path Configuration:")
    print(f"Project Root: {PROJECT_ROOT}")
    print(f"Bifrost Root: {BIFROST_ROOT}")
    print(f"Smart Trader Root: {SMART_TRADER_ROOT}")
    print("\nAdded to sys.path:")
    for path in paths_to_add:
        if os.path.exists(path):
            print(f"  ✓ {path}")
        else:
            print(f"  ✗ {path} (not found)")