#!/usr/bin/env python3
"""
Check research_data table structure
"""

import os
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

def check_table_structure():
    """Check the actual structure of research_data table"""
    
    # Load .env file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    env_path = os.path.join(script_dir, '.env')
    load_dotenv(env_path, override=True)
    
    print("🔍 Checking research_data Table Structure")
    print("=" * 60)
    
    # Database configuration
    db_config = {
        'host': 'switchback.proxy.rlwy.net',
        'port': 17121,
        'user': 'root',
        'password': 'zAFTUZnwLefvYBrVaQSZNndcSmnZeuRe',
        'database': 'railway'
    }
    
    try:
        url = f"mysql+pymysql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}?charset=utf8mb4"
        engine = create_engine(url)
        
        with engine.connect() as conn:
            # Get table structure
            print("📋 Table Columns:")
            columns = conn.execute(text('DESCRIBE research_data')).fetchall()
            for i, col in enumerate(columns, 1):
                print(f"  {i:2d}. {col[0]} ({col[1]})")
            
            print(f"\n📊 Total columns: {len(columns)}")
            
            # Check if there's any ID-like column
            id_columns = [col[0] for col in columns if 'id' in col[0].lower() or col[0].lower() in ['index', 'rowid']]
            if id_columns:
                print(f"🔍 ID-like columns found: {id_columns}")
            else:
                print("⚠️  No ID-like columns found")
            
            # Get a sample row to see the data
            print(f"\n📄 Sample record (first row):")
            sample = conn.execute(text('SELECT * FROM research_data LIMIT 1')).fetchone()
            if sample:
                col_names = [col[0] for col in columns]
                for col_name, value in zip(col_names[:10], sample[:10]):  # Show first 10 columns
                    print(f"  {col_name}: {value}")
                if len(col_names) > 10:
                    print(f"  ... and {len(col_names) - 10} more columns")
            
        return True
        
    except Exception as e:
        print(f"❌ Error checking table structure: {e}")
        return False

if __name__ == "__main__":
    check_table_structure()