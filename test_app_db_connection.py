#!/usr/bin/env python3
"""
Test database connection using the exact same code as the app
"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
import pandas as pd

def _load_db_config_from_env_or_secrets():
    """
    Exact copy of the function from app.py
    """
    # Load .env file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    env_path = os.path.join(script_dir, '.env')
    load_dotenv(env_path, override=True)
    
    def _get(key, default=None):
        return os.getenv(key, default)

    host_raw = _get("DB_HOST", "switchback.proxy.rlwy.net")  # Default to Railway host
    user = _get("DB_USER", "root")
    pwd = _get("DB_PASSWORD", "zAFTUZnwLefvYBrVaQSZNndcSmnZeuRe")  # Default Railway password
    dbname = _get("DB_NAME", "railway")
    
    print(f"[DEBUG] DB Config - Host: {host_raw}, User: {user}, DB: {dbname}")
    print(f"[DEBUG] .env file path: {env_path}")
    print(f"[DEBUG] .env file exists: {os.path.exists(env_path)}")
    
    # Railway hostname conversion for external access
    if host_raw == "mysql.railway.internal":
        host_raw = "switchback.proxy.rlwy.net"
        if not _get("DB_PORT"):
            port = 17121
        else:
            port = _get("DB_PORT", "17121")
    else:
        port = _get("DB_PORT", "17121")  # Default to Railway port

    host = host_raw
    if ":" in host_raw:
        host, port = host_raw.split(":", 1)

    port = int(port) if port else 17121  # Default to Railway port instead of 3306
    return host, port, user, pwd, dbname

def test_db_connection():
    """Test database connection exactly like the app"""
    
    print("🔍 Testing Database Connection (App Logic)")
    print("=" * 60)
    
    try:
        # Get config exactly like app
        host, port, user, pwd, dbname = _load_db_config_from_env_or_secrets()
        
        print(f"[DEBUG] Final DB connection - Host: {host}, Port: {port}, User: {user}, DB: {dbname}")
        
        # Create URL exactly like app
        if pwd:
            url = f"mysql+pymysql://{user}:{pwd}@{host}:{port}/{dbname}?charset=utf8mb4"
            print(f"[DEBUG] Connection URL: mysql+pymysql://{user}:***@{host}:{port}/{dbname}?charset=utf8mb4")
        else:
            url = f"mysql+pymysql://{user}@{host}:{port}/{dbname}?charset=utf8mb4"
            print(f"[DEBUG] Connection URL: mysql+pymysql://{user}@{host}:{port}/{dbname}?charset=utf8mb4")
        
        # Create engine exactly like app (without caching)
        engine = create_engine(
            url,
            pool_pre_ping=True,
            pool_recycle=3600,
            pool_size=2,
            max_overflow=3,
            pool_timeout=30,
        )
        
        print(f"✅ Engine created successfully")
        
        # Test connection exactly like load_default_data
        with engine.connect() as conn:
            # Check if research_data table exists
            result = conn.execute(text("SHOW TABLES LIKE 'research_data'")).fetchone()
            if not result:
                print("❌ research_data table does not exist")
                return False
            
            print("✅ research_data table exists")
            
            # Get record count
            count = conn.execute(text("SELECT COUNT(*) FROM research_data")).scalar()
            print(f"✅ Found {count:,} records in research_data table")
            
            # Try the exact query from the app
            df = pd.read_sql("SELECT * FROM research_data ORDER BY feature_name DESC LIMIT 10", engine)
            print(f"✅ Successfully loaded {len(df)} sample rows using app query")
            
        print(f"\n🎉 Database connection test PASSED!")
        print(f"📊 The app should be able to load research_data successfully")
        return True
        
    except Exception as e:
        print(f"\n❌ Database connection test FAILED: {e}")
        print(f"💡 This is why the app shows connection errors")
        return False

if __name__ == "__main__":
    test_db_connection()