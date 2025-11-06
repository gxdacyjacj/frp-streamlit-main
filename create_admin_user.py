#!/usr/bin/env python3
"""
Create Admin User Script for FRP Streamlit App
Creates the admin@frp.com user directly in the Railway database
"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

def create_admin_user():
    """Create admin user in the database"""
    
    # Load environment variables
    load_dotenv()
    
    # Database configuration
    db_config = {
        'host': os.getenv('DB_HOST', 'switchback.proxy.rlwy.net'),
        'port': int(os.getenv('DB_PORT', '17121')),
        'user': os.getenv('DB_USER', 'root'),
        'password': os.getenv('DB_PASSWORD', 'zAFTUZnwLefvYBrVaQSZNndcSmnZeuRe'),
        'database': os.getenv('DB_NAME', 'railway')
    }
    
    print("🔧 Creating Admin User for FRP Streamlit App")
    print("=" * 50)
    print(f"Database: {db_config['host']}:{db_config['port']}/{db_config['database']}")
    
    try:
        # Create database connection
        url = f"mysql+pymysql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}?charset=utf8mb4"
        engine = create_engine(url)
        
        with engine.begin() as conn:
            # First, create the users table if it doesn't exist
            print("📋 Creating users table...")
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    email VARCHAR(255) UNIQUE NOT NULL,
                    name VARCHAR(255) NOT NULL,
                    institution VARCHAR(255),
                    ip_address VARCHAR(45),
                    role VARCHAR(50) DEFAULT 'viewer',
                    status VARCHAR(50) DEFAULT 'pending',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    approved_by VARCHAR(255),
                    approved_at TIMESTAMP NULL
                )
            """))
            
            # Check if admin user already exists
            existing_admin = conn.execute(
                text("SELECT email, name, role, status FROM users WHERE email = 'admin@frp.com'")
            ).fetchone()
            
            if existing_admin:
                print(f"👤 Admin user already exists:")
                print(f"   Email: {existing_admin[0]}")
                print(f"   Name: {existing_admin[1]}")
                print(f"   Role: {existing_admin[2]}")
                print(f"   Status: {existing_admin[3]}")
                
                # Update to ensure admin has correct permissions
                conn.execute(text("""
                    UPDATE users 
                    SET role = 'admin', status = 'approved', approved_by = 'system', approved_at = NOW()
                    WHERE email = 'admin@frp.com'
                """))
                print("✅ Admin permissions updated!")
                
            else:
                # Create new admin user
                print("👤 Creating new admin user...")
                conn.execute(text("""
                    INSERT INTO users (name, email, institution, role, status, approved_by, approved_at, ip_address)
                    VALUES ('System Administrator', 'admin@frp.com', 'System', 'admin', 'approved', 'system', NOW(), '127.0.0.1')
                """))
                print("✅ Admin user created successfully!")
            
            # Show all users for verification
            print("\n📊 Current users in database:")
            all_users = conn.execute(text("SELECT email, name, role, status FROM users")).fetchall()
            for user in all_users:
                status_icon = "✅" if user[3] == "approved" else "⏳"
                role_icon = "👑" if user[2] == "admin" else "👤"
                print(f"   {status_icon} {role_icon} {user[0]} - {user[1]} ({user[2]}, {user[3]})")
            
            print("\n🎉 Setup complete!")
            print("You can now login with: admin@frp.com")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False
    
    return True

if __name__ == "__main__":
    create_admin_user()