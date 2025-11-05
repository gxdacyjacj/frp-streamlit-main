#!/usr/bin/env python3
"""
FRP Streamlit App - Deployment Readiness Check
检查应用是否准备好部署
"""

import ast
import os
import sys

def check_python_syntax(file_path):
    """检查Python文件语法"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            source = f.read()
        
        # 检查语法
        ast.parse(source)
        return True, "✅ Syntax OK"
    except SyntaxError as e:
        return False, f"❌ Syntax Error: {e}"
    except Exception as e:
        return False, f"❌ Error: {e}"

def check_imports():
    """检查关键导入是否正确"""
    try:
        # 模拟检查导入（不实际导入以避免依赖问题）
        print("📦 Checking import statements in app.py...")
        
        with open('app.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        required_imports = [
            'streamlit',
            'pandas',
            'numpy', 
            'sqlalchemy',
            'pymysql',
            'plotly',
            'scikit-learn'
        ]
        
        missing = []
        for imp in required_imports:
            # 简单检查是否在文件中提到
            if imp not in content and imp.replace('-', '_') not in content:
                missing.append(imp)
        
        if missing:
            print(f"⚠️  Potentially missing imports: {missing}")
        else:
            print("✅ All required imports found in code")
        
        return True
    except Exception as e:
        print(f"❌ Import check failed: {e}")
        return False

def check_deployment_files():
    """检查部署相关文件"""
    files_to_check = {
        'requirements.txt': 'Dependencies file',
        '.env': 'Environment variables',
        'railway.toml': 'Railway deployment config',
        'Procfile': 'Heroku deployment config',
        '.streamlit/config.toml': 'Streamlit configuration'
    }
    
    print("\n📋 Deployment Files Check")
    print("=" * 50)
    
    all_present = True
    for file_path, description in files_to_check.items():
        if os.path.exists(file_path):
            print(f"✅ {file_path} - {description}")
        else:
            print(f"❌ {file_path} - {description} (Missing)")
            all_present = False
    
    return all_present

def main():
    print("🚀 FRP Streamlit App - Deployment Readiness Check")
    print("=" * 60)
    
    # 检查主应用文件语法
    print("1. Checking app.py syntax...")
    syntax_ok, syntax_msg = check_python_syntax('app.py')
    print(f"   {syntax_msg}")
    
    # 检查导入
    print("\n2. Checking imports...")
    imports_ok = check_imports()
    
    # 检查部署文件
    print("\n3. Checking deployment files...")
    deploy_files_ok = check_deployment_files()
    
    # 总结
    print("\n" + "=" * 60)
    print("📊 DEPLOYMENT READINESS SUMMARY")
    print("=" * 60)
    
    if syntax_ok and imports_ok and deploy_files_ok:
        print("🎉 ✅ APP IS READY FOR DEPLOYMENT!")
        print("\n📝 Next Steps:")
        print("   1. Push code to Git repository")
        print("   2. Deploy to Railway/Streamlit Cloud/Heroku")
        print("   3. Set environment variables on deployment platform")
        print("   4. Ensure Railway database is accessible")
        print("\n💡 Deployment Platforms:")
        print("   • Railway: Use railway.toml configuration")
        print("   • Streamlit Cloud: Will auto-detect streamlit app")
        print("   • Heroku: Use Procfile configuration")
    else:
        print("❌ APP NEEDS FIXES BEFORE DEPLOYMENT")
        if not syntax_ok:
            print("   • Fix Python syntax errors")
        if not imports_ok:
            print("   • Check import statements")
        if not deploy_files_ok:
            print("   • Add missing deployment files")

if __name__ == "__main__":
    main()