#!/usr/bin/env python3
"""
FRP Streamlit App - Railway Database Connection Test
测试Railway MySQL数据库连接
"""

import os
import sys
from dotenv import load_dotenv
import pymysql
from sqlalchemy import create_engine, text

def test_railway_connection():
    """测试Railway数据库连接"""
    
    # 加载环境变量
    load_dotenv()
    
    # 获取数据库配置
    db_config = {
        'host': os.getenv('DB_HOST', 'switchback.proxy.rlwy.net'),
        'port': int(os.getenv('DB_PORT', '17121')),
        'user': os.getenv('DB_USER', 'root'),
        'password': os.getenv('DB_PASSWORD', 'zAFTUZnwLefvYBrVaQSZNndcSmnZeuRe'),
        'database': os.getenv('DB_NAME', 'railway')
    }
    
    print("🚀 Railway Database Connection Test")
    print("=" * 50)
    print(f"Host: {db_config['host']}")
    print(f"Port: {db_config['port']}")
    print(f"User: {db_config['user']}")
    print(f"Database: {db_config['database']}")
    print("=" * 50)
    
    try:
        # 测试PyMySQL连接
        print("📡 Testing PyMySQL connection...")
        connection = pymysql.connect(**db_config, charset='utf8mb4')
        
        with connection.cursor() as cursor:
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()
            print(f"✅ MySQL Version: {version[0]}")
            
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            print(f"✅ Found {len(tables)} tables")
            
            # 检查research_data表
            cursor.execute("SHOW TABLES LIKE 'research_data'")
            research_table = cursor.fetchone()
            if research_table:
                cursor.execute("SELECT COUNT(*) FROM research_data")
                count = cursor.fetchone()
                print(f"✅ research_data table: {count[0]} records")
            else:
                print("❌ research_data table not found")
        
        connection.close()
        
        # 测试SQLAlchemy连接
        print("\n🔗 Testing SQLAlchemy connection...")
        url = f"mysql+pymysql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}?charset=utf8mb4"
        engine = create_engine(url)
        
        with engine.connect() as conn:
            result = conn.execute(text("SELECT COUNT(*) FROM research_data")).scalar()
            print(f"✅ SQLAlchemy query successful: {result} records")
        
        print("\n🎉 Database connection test PASSED!")
        print("✅ The Streamlit app should work correctly with Railway")
        return True
        
    except Exception as e:
        print(f"\n❌ Database connection test FAILED!")
        print(f"Error: {str(e)}")
        return False

def check_environment():
    """检查环境配置"""
    print("\n🔧 Environment Configuration Check")
    print("=" * 50)
    
    required_vars = ['DB_HOST', 'DB_PORT', 'DB_USER', 'DB_PASSWORD', 'DB_NAME']
    for var in required_vars:
        value = os.getenv(var)
        if value:
            # 隐藏密码
            display_value = value if var != 'DB_PASSWORD' else '*' * len(value)
            print(f"✅ {var}: {display_value}")
        else:
            print(f"❌ {var}: Not set")

if __name__ == "__main__":
    check_environment()
    test_railway_connection()