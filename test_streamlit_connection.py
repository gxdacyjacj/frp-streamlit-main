#!/usr/bin/env python3
"""
Quick Railway Connection Test for Streamlit Cloud Deployment
"""

import streamlit as st
from sqlalchemy import create_engine, text

def test_deployment_connection():
    """Test database connection using Streamlit secrets"""
    
    st.title("🚀 Railway Database Connection Test")
    
    try:
        # Get database config from Streamlit secrets
        host = st.secrets.get("DB_HOST", "Not configured")
        port = st.secrets.get("DB_PORT", "Not configured") 
        user = st.secrets.get("DB_USER", "Not configured")
        password = st.secrets.get("DB_PASSWORD", "Not configured")
        database = st.secrets.get("DB_NAME", "Not configured")
        
        st.write("### Configuration:")
        st.write(f"- **Host**: {host}")
        st.write(f"- **Port**: {port}")
        st.write(f"- **User**: {user}")
        st.write(f"- **Database**: {database}")
        st.write(f"- **Password**: {'*' * len(str(password)) if password != 'Not configured' else 'Not configured'}")
        
        if host == "Not configured":
            st.error("❌ Database configuration not found in secrets!")
            st.info("Please set up the database secrets in Streamlit Cloud.")
            return False
        
        # Test connection
        with st.spinner("Testing database connection..."):
            url = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}?charset=utf8mb4"
            engine = create_engine(url)
            
            with engine.connect() as conn:
                # Test basic connection
                version = conn.execute(text("SELECT VERSION()")).scalar()
                st.success(f"✅ **Connection successful!**")
                st.info(f"MySQL Version: {version}")
                
                # Test research_data table
                try:
                    count = conn.execute(text("SELECT COUNT(*) FROM research_data")).scalar()
                    st.success(f"✅ **research_data table found**: {count:,} records")
                except Exception as e:
                    st.warning(f"⚠️ research_data table issue: {str(e)}")
                
                # Test table creation permissions
                try:
                    conn.execute(text("CREATE TABLE IF NOT EXISTS test_permissions (id INT PRIMARY KEY)"))
                    conn.execute(text("DROP TABLE test_permissions"))
                    st.success("✅ **Database permissions**: Full access (CREATE/DROP)")
                except Exception as e:
                    st.warning(f"⚠️ Limited database permissions: {str(e)}")
        
        return True
        
    except Exception as e:
        st.error(f"❌ **Connection failed**: {str(e)}")
        
        # Show debugging info
        if "Access denied" in str(e):
            st.error("🔑 **Authentication Error**: Check username/password")
        elif "Can't connect" in str(e) or "timed out" in str(e):
            st.error("🌐 **Network Error**: Check hostname/port")
        elif "Unknown database" in str(e):
            st.error("🗄️ **Database Error**: Check database name")
        
        return False

if __name__ == "__main__":
    test_deployment_connection()