#!/usr/bin/env python3
"""
Test environment variable loading exactly like the app does
"""

import os
import streamlit as st
from dotenv import load_dotenv

def test_env_loading():
    """Test if environment variables are loading correctly"""
    
    print("🔍 Testing Environment Variable Loading")
    print("=" * 60)
    
    # Exactly like the app does
    script_dir = os.path.dirname(os.path.abspath(__file__))
    env_path = os.path.join(script_dir, '.env')
    
    print(f"📁 Script directory: {script_dir}")
    print(f"📄 .env file path: {env_path}")
    print(f"✅ .env file exists: {os.path.exists(env_path)}")
    
    # Load .env file
    load_result = load_dotenv(env_path, override=True)
    print(f"📥 load_dotenv result: {load_result}")
    
    # Test _get function exactly like the app
    def _get(key, default=None):
        # Check if we're in Streamlit (we're not in this test)
        if hasattr(st, "secrets") and key in st.secrets:
            return st.secrets.get(key, default)
        return os.getenv(key, default)
    
    # Test each variable
    test_vars = [
        ("DB_HOST", "switchback.proxy.rlwy.net"),
        ("DB_PORT", "17121"), 
        ("DB_USER", "root"),
        ("DB_PASSWORD", "zAFTUZnwLefvYBrVaQSZNndcSmnZeuRe"),
        ("DB_NAME", "railway")
    ]
    
    print(f"\n📋 Environment Variables:")
    for var_name, expected_default in test_vars:
        env_value = os.getenv(var_name)
        app_value = _get(var_name, expected_default)
        print(f"  {var_name}:")
        print(f"    Raw env: {env_value}")
        print(f"    App value: {app_value}")
        print(f"    Match: {'✅' if env_value == app_value else '❌'}")
    
    # Test the full configuration function
    print(f"\n🔧 Testing full _load_db_config_from_env_or_secrets logic:")
    
    host_raw = _get("DB_HOST", "switchback.proxy.rlwy.net")
    user = _get("DB_USER", "root")
    pwd = _get("DB_PASSWORD", "zAFTUZnwLefvYBrVaQSZNndcSmnZeuRe")
    dbname = _get("DB_NAME", "railway")
    
    # Railway hostname conversion
    if host_raw == "mysql.railway.internal":
        host_raw = "switchback.proxy.rlwy.net"
        if not _get("DB_PORT"):
            port = 17121
        else:
            port = _get("DB_PORT", "17121")
    else:
        port = _get("DB_PORT", "17121")

    host = host_raw
    if ":" in host_raw:
        host, port = host_raw.split(":", 1)

    port = int(port) if port else 17121
    
    print(f"  Final host: {host}")
    print(f"  Final port: {port}")
    print(f"  Final user: {user}")
    print(f"  Final password: {'*' * len(pwd) if pwd else 'None'}")
    print(f"  Final database: {dbname}")
    
    # Check if this matches Railway configuration
    expected_host = "switchback.proxy.rlwy.net"
    expected_port = 17121
    
    if host == expected_host and port == expected_port:
        print(f"\n🎉 Configuration matches Railway settings!")
        return True
    else:
        print(f"\n❌ Configuration mismatch!")
        print(f"   Expected: {expected_host}:{expected_port}")
        print(f"   Got: {host}:{port}")
        return False

if __name__ == "__main__":
    test_env_loading()