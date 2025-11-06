#!/usr/bin/env python3
"""
Simple test of environment variable loading
"""

import os
from dotenv import load_dotenv

def test_env_simple():
    """Simple test of environment variables"""
    
    print("🔍 Simple Environment Test")
    print("=" * 40)
    
    # Load .env file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    env_path = os.path.join(script_dir, '.env')
    
    print(f"📄 .env path: {env_path}")
    print(f"✅ .env exists: {os.path.exists(env_path)}")
    
    load_result = load_dotenv(env_path, override=True)
    print(f"📥 load_dotenv: {load_result}")
    
    # Check key variables
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT") 
    db_user = os.getenv("DB_USER")
    db_name = os.getenv("DB_NAME")
    
    print(f"\n📋 Variables:")
    print(f"  DB_HOST: {db_host}")
    print(f"  DB_PORT: {db_port}")
    print(f"  DB_USER: {db_user}")
    print(f"  DB_NAME: {db_name}")
    
    if db_host == "switchback.proxy.rlwy.net" and db_port == "17121":
        print(f"\n✅ Environment loaded correctly!")
    else:
        print(f"\n❌ Environment not loaded correctly!")

if __name__ == "__main__":
    test_env_simple()