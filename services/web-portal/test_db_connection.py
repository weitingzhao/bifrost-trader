#!/usr/bin/env python3
"""
Test script to verify PostgreSQL database connection for Bifrost Trader Web Portal
"""

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "shared"))

from database.connection import get_db_connection


def test_database_connection():
    """Test database connection and basic operations."""
    print("🔍 Testing PostgreSQL database connection...")

    try:
        # Get database connection
        db = get_db_connection()

        # Test connection
        if not db.test_connection():
            print("❌ Database connection failed!")
            return False

        print("✅ Database connection successful!")

        # Test basic query
        print("📊 Testing basic query...")
        result = db.execute_query("SELECT COUNT(*) as count FROM market_symbol")

        if result:
            count = result[0]["count"]
            print(f"✅ Found {count} market symbols in database")
        else:
            print("⚠️ No market symbols found in database")

        # Test portfolio query
        print("💼 Testing portfolio query...")
        result = db.execute_query("SELECT COUNT(*) as count FROM portfolio")

        if result:
            count = result[0]["count"]
            print(f"✅ Found {count} portfolios in database")
        else:
            print("⚠️ No portfolios found in database")

        # Test holdings query
        print("📈 Testing holdings query...")
        result = db.execute_query("SELECT COUNT(*) as count FROM holding")

        if result:
            count = result[0]["count"]
            print(f"✅ Found {count} holdings in database")
        else:
            print("⚠️ No holdings found in database")

        print("🎉 Database connection test completed successfully!")
        return True

    except Exception as e:
        print(f"❌ Database connection test failed: {e}")
        return False


if __name__ == "__main__":
    success = test_database_connection()
    if success:
        print("\n✅ Database is ready for Bifrost Trader Web Portal!")
    else:
        print("\n❌ Database connection test failed!")
        sys.exit(1)
