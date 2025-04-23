#!/usr/bin/env python3
import os
import shutil
import subprocess
import datetime
import sys

# Configuration
APP_DIR = os.path.dirname(os.path.abspath(__file__))
DEPLOY_DIR = os.path.join(os.path.dirname(APP_DIR), "flask_app_production")
BACKUP_DIR = os.path.join(os.path.dirname(APP_DIR), "flask_app_backup")
LOG_FILE = os.path.join(APP_DIR, "deployment.log")

def log_message(message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {message}\n")
    print(message)

def create_backup():
    """Create backup of current production"""
    if os.path.exists(DEPLOY_DIR):
        log_message("Creating backup of current deployment...")
        
        # Remove old backup if exists
        if os.path.exists(BACKUP_DIR):
            shutil.rmtree(BACKUP_DIR)
            
        # Create backup
        shutil.copytree(DEPLOY_DIR, BACKUP_DIR)
        log_message("Backup created successfully at " + BACKUP_DIR)
    else:
        log_message("No existing deployment to backup.")

def deploy():
    """Deploy application to production directory"""
    log_message("Starting deployment...")
    
    # Create backup first
    create_backup()
    
    # Remove existing deployment if any
    if os.path.exists(DEPLOY_DIR):
        shutil.rmtree(DEPLOY_DIR)
    
    # Create deployment directory
    os.makedirs(DEPLOY_DIR, exist_ok=True)
    
    # Copy application files
    log_message("Copying application files...")
    
    # Only copy necessary files and directories
    dirs_to_copy = ['app', 'tests']
    files_to_copy = ['run.py', 'requirements.txt']
    
    for dir_name in dirs_to_copy:
        src_dir = os.path.join(APP_DIR, dir_name)
        dst_dir = os.path.join(DEPLOY_DIR, dir_name)
        if os.path.exists(src_dir):
            shutil.copytree(src_dir, dst_dir)
    
    for file_name in files_to_copy:
        src_file = os.path.join(APP_DIR, file_name)
        dst_file = os.path.join(DEPLOY_DIR, file_name)
        if os.path.exists(src_file):
            shutil.copy2(src_file, dst_file)
    
    log_message("Files copied successfully.")
    
    try:
        # Create virtual environment in production
        log_message("Setting up virtual environment...")
        venv_path = os.path.join(DEPLOY_DIR, "venv")
        
        # Try different approaches to create venv
        try:
            # Try with the current Python executable
            subprocess.run([sys.executable, "-m", "venv", venv_path], check=True)
        except subprocess.CalledProcessError:
            # Try with python command directly
            try:
                if os.name == 'nt':  # Windows
                    subprocess.run(["python", "-m", "venv", venv_path], check=True)
                else:
                    subprocess.run(["python3", "-m", "venv", venv_path], check=True)
            except subprocess.CalledProcessError as e:
                log_message(f"Error creating virtual environment: {e}")
                return False
        
        # Install dependencies
        log_message("Installing dependencies...")
        
        # Get the correct pip path based on the OS
        if os.name == 'nt':  # Windows
            pip_path = os.path.join(venv_path, "Scripts", "pip")
        else:  # Unix/Linux/Mac
            pip_path = os.path.join(venv_path, "bin", "pip")
        
        requirements_path = os.path.join(DEPLOY_DIR, "requirements.txt")
        
        subprocess.run([pip_path, "install", "-r", requirements_path], check=True)
        
        log_message("Deployment completed successfully.")
        return True
        
    except Exception as e:
        log_message(f"Deployment failed: {str(e)}")
        return False

def rollback():
    """Rollback to previous version"""
    if not os.path.exists(BACKUP_DIR):
        log_message("No backup found. Cannot rollback.")
        return False
    
    log_message("Starting rollback...")
    
    # Remove current deployment
    if os.path.exists(DEPLOY_DIR):
        shutil.rmtree(DEPLOY_DIR)
    
    # Restore from backup
    shutil.copytree(BACKUP_DIR, DEPLOY_DIR)
    
    log_message("Rollback completed successfully.")
    return True

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "rollback":
        rollback()
    else:
        deploy()