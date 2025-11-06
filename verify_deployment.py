#!/usr/bin/env python3
"""
Verify Railway Database Deployment
"""

import pandas as pd
from sqlalchemy import create_engine, text

def verify_deployment():
    """Verify the dataset deployment to Railway"""
    
    # Database configuration
    db_config = {
        'host': 'switchback.proxy.rlwy.net',
        'port': 17121,
        'user': 'root',
        'password': 'zAFTUZnwLefvYBrVaQSZNndcSmnZeuRe',
        'database': 'railway'
    }
    
    print("🔍 Railway Database Deployment Verification")
    print("=" * 60)
    
    try:
        url = f"mysql+pymysql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}?charset=utf8mb4"
        engine = create_engine(url)
        
        with engine.connect() as conn:
            # Check all tables
            print("🗄️ Database Tables:")
            tables = conn.execute(text('SHOW TABLES')).fetchall()
            for table in tables:
                count = conn.execute(text(f'SELECT COUNT(*) FROM `{table[0]}`')).scalar()
                print(f"  ✅ {table[0]}: {count:,} records")
            
            # Detailed research_data analysis
            print(f"\n📊 research_data table analysis:")
            
            # Get column count
            columns = conn.execute(text('DESCRIBE research_data')).fetchall()
            print(f"  📋 Columns: {len(columns)}")
            
            # Get record count
            total_records = conn.execute(text('SELECT COUNT(*) FROM research_data')).scalar()
            print(f"  📈 Total records: {total_records:,}")
            
            # Sample data
            sample = conn.execute(text('SELECT * FROM research_data LIMIT 3')).fetchall()
            print(f"  🔍 Sample records: {len(sample)}")
            
            # Check for duplicates
            unique_count = conn.execute(text('SELECT COUNT(DISTINCT feature_name) FROM research_data')).scalar()
            print(f"  🔄 Unique feature_names: {unique_count:,}")
            
            # Data completeness check
            non_null_titles = conn.execute(text('SELECT COUNT(*) FROM research_data WHERE Title IS NOT NULL AND Title != ""')).scalar()
            completeness = (non_null_titles / total_records * 100) if total_records > 0 else 0
            print(f"  📝 Title completeness: {completeness:.1f}%")
            
        print(f"\n🎉 Deployment verification completed!")
        print(f"✅ Dataset successfully deployed to Railway MySQL")
        
        return True
        
    except Exception as e:
        print(f"❌ Verification failed: {e}")
        return False

if __name__ == "__main__":
    verify_deployment()