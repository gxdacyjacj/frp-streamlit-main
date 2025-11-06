#!/usr/bin/env python3
"""
Debug Railway Database Connection for Streamlit App
"""

import os
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

def debug_app_connection():
    """Debug the exact same connection logic used by the app"""
    
    # Load .env file exactly like the app does
    script_dir = os.path.dirname(os.path.abspath(__file__))
    env_path = os.path.join(script_dir, '.env')
    load_dotenv(env_path, override=True)
    
    print("🔍 Debugging Streamlit App Database Connection")
    print("=" * 60)
    
    # Use exact same logic as app
    def _get(key, default=None):
        return os.getenv(key, default)

    host_raw = _get("DB_HOST", "localhost")
    user = _get("DB_USER", "root")
    pwd = _get("DB_PASSWORD", "")
    dbname = _get("DB_NAME", "railway")
    
    # Railway hostname conversion (same as app)
    if host_raw == "mysql.railway.internal":
        host_raw = "switchback.proxy.rlwy.net"
        if not _get("DB_PORT"):
            port = 17121
        else:
            port = _get("DB_PORT")
    else:
        port = _get("DB_PORT")

    host = host_raw
    if ":" in host_raw:
        host, port = host_raw.split(":", 1)
    
    port = int(port) if port else 3306
    
    print(f"📋 Connection Configuration:")
    print(f"  Host: {host}")
    print(f"  Port: {port}")
    print(f"  User: {user}")
    print(f"  Password: {'*' * len(pwd) if pwd else 'None'}")
    print(f"  Database: {dbname}")
    
    # Create URL exactly like app does
    if pwd:
        url = f"mysql+pymysql://{user}:{pwd}@{host}:{port}/{dbname}?charset=utf8mb4"
    else:
        url = f"mysql+pymysql://{user}@{host}:{port}/{dbname}?charset=utf8mb4"
    
    print(f"  URL: mysql+pymysql://{user}:***@{host}:{port}/{dbname}?charset=utf8mb4")
    
    try:
        # Create engine exactly like app does
        engine = create_engine(
            url,
            pool_pre_ping=True,
            pool_recycle=3600,
            pool_size=2,
            max_overflow=3,
            pool_timeout=30,
        )
        
        print(f"\n✅ Engine created successfully")
        
        # Test connection exactly like load_default_data does
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
            
            # Try to load sample data exactly like app does
            df = pd.read_sql("SELECT * FROM research_data ORDER BY feature_name DESC LIMIT 10", engine)
            print(f"✅ Successfully loaded {len(df)} sample rows")
            
            # Show column info
            columns_result = conn.execute(text("DESCRIBE research_data")).fetchall()
            print(f"✅ Table has {len(columns_result)} columns")
            
            print(f"\n🎉 Database connection test PASSED!")
            print(f"📊 The app should be able to load research_data successfully")
            
        return True
        
    except Exception as e:
        print(f"\n❌ Database connection test FAILED: {e}")
        print(f"💡 This is likely why the app shows 'Failed to load data from database'")
        return False

if __name__ == "__main__":
    debug_app_connection()