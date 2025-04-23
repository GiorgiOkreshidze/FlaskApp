#!/usr/bin/env python3
import datetime
import requests
import time
import os

# Configuration
HEALTH_CHECK_URL = "http://localhost:5000/health"
LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "health_check.log")
CHECK_INTERVAL = 60  # seconds

def log_message(message, status="INFO"):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] [{status}] {message}\n")
    print(f"[{status}] {message}")

def check_health():
    try:
        response = requests.get(HEALTH_CHECK_URL, timeout=10)
        if response.status_code == 200 and response.json().get('status') == 'healthy':
            log_message("Application is healthy", "SUCCESS")
            return True
        else:
            log_message(f"Health check failed with status code: {response.status_code}", "ERROR")
            return False
    except Exception as e:
        log_message(f"Health check failed: {str(e)}", "ERROR")
        return False

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "daemon":
        log_message("Starting health check daemon")
        while True:
            check_health()
            time.sleep(CHECK_INTERVAL)
    else:
        # Run a single check
        check_health()