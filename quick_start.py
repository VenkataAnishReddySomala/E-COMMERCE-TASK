#!/usr/bin/env python3
"""
Quick Start Script for E-commerce Project
This script automates the entire setup process for new developers.
"""

import os
import sys
import subprocess
import shutil

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error during {description}: {e}")
        print(f"Error output: {e.stderr}")
        return False

def main():
    """Main setup function"""
    print("🚀 E-commerce Project Quick Start")
    print("=" * 50)
    
    # Check if Python is available
    if not shutil.which('python'):
        print("❌ Python is not installed or not in PATH")
        sys.exit(1)
    
    # Check if pip is available
    if not shutil.which('pip'):
        print("❌ pip is not installed or not in PATH")
        sys.exit(1)
    
    # Step 1: Install dependencies
    if not run_command("pip install -r requirements.txt", "Installing Python dependencies"):
        sys.exit(1)
    
    # Step 2: Check if dataset exists, if not download it
    if not os.path.exists('ecommerce-dataset'):
        print("📥 Dataset not found. Downloading...")
        if not run_command("git clone https://github.com/recruit41/ecommerce-dataset.git", "Downloading dataset"):
            sys.exit(1)
    else:
        print("✅ Dataset already exists")
    
    # Step 3: Initialize database
    if os.path.exists('init_database.py'):
        print("🗄️  Initializing database...")
        try:
            # Import and run the database initialization
            from init_database import main as init_db
            init_db()
        except Exception as e:
            print(f"❌ Error initializing database: {e}")
            sys.exit(1)
    else:
        print("❌ init_database.py not found")
        sys.exit(1)
    
    # Step 4: Verify setup
    if os.path.exists('verify_data.py'):
        print("🔍 Verifying setup...")
        try:
            from verify_data import verify_database
            verify_database()
        except Exception as e:
            print(f"⚠️  Warning: Could not verify data: {e}")
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. The database is ready for development")
    print("2. You can now proceed to the next milestone")
    print("3. Run 'python verify_data.py' anytime to check the data")

if __name__ == "__main__":
    main() 