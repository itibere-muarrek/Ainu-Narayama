#!/usr/bin/env python3
"""
Discover PostgreSQL connection string from Railway environment
"""
import os
import sys
import json

def get_database_url():
    """Get DATABASE_URL from environment or construct it"""

    # 1. Check if DATABASE_URL is already set
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        print(f"✅ Using DATABASE_URL from environment")
        return database_url

    # 2. Try Railway-provided PostgreSQL variables
    pg_host = os.getenv("PGHOST")
    pg_port = os.getenv("PGPORT", "5432")
    pg_user = os.getenv("PGUSER")
    pg_password = os.getenv("PGPASSWORD")
    pg_database = os.getenv("PGDATABASE")

    if all([pg_host, pg_user, pg_password, pg_database]):
        database_url = f"postgresql://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_database}"
        print(f"✅ Built DATABASE_URL from Railway PostgreSQL variables")
        print(f"   Host: {pg_host}:{pg_port}")
        print(f"   Database: {pg_database}")
        return database_url

    # 3. Try to find PostgreSQL via Railway's internal DNS
    # Railway services can communicate via servicename.railway.internal
    postgres_hosts = [
        "postgres.railway.internal",
        "postgres:5432",
        "localhost:5432"
    ]

    for host in postgres_hosts:
        try:
            import socket
            hostname = host.split(":")[0]
            socket.gethostbyname(hostname)

            # If we got here, the host is reachable
            # Try to construct URL with default credentials
            for user in ["postgres", "ainu", "railway"]:
                for password in [os.getenv(f"{user.upper()}_PASSWORD", ""), user]:
                    for db in ["ainu_narayama", "ainu", "postgres"]:
                        test_url = f"postgresql://{user}:{password}@{host}/{db}"
                        database_url = test_url
                        print(f"✅ Attempting connection to {host}")
                        return database_url
        except:
            continue

    # 4. Fallback to SQLite with warning
    database_url = "sqlite:///./test.db"
    print(f"⚠️  WARNING: No PostgreSQL configuration found!")
    print(f"   Falling back to SQLite (data will NOT persist)")
    print(f"   To fix: Set DATABASE_URL environment variable in Railway")

    return database_url

if __name__ == "__main__":
    url = get_database_url()
    # Export as environment variable for the app to use
    os.environ["DATABASE_URL"] = url
    print(f"\n🗄️  DATABASE_URL configured")
    print(f"   Connection: {url[:50]}...")
