#!/usr/bin/env python3
"""
Test script để debug logger
"""

import sys
from pathlib import Path

# Thêm current directory vào Python path
sys.path.insert(0, str(Path(__file__).parent))

try:
    print("1. Importing logger...")
    from app.logger import setup_logger
    print("✅ Logger imported successfully")
    
    print("2. Checking logs directory...")
    logs_dir = Path("logs")
    if logs_dir.exists():
        print(f"✅ Logs directory exists: {logs_dir}")
        print(f"   Contents: {list(logs_dir.iterdir())}")
    else:
        print("❌ Logs directory not found")
    
    print("3. Testing logger...")
    from loguru import logger
    logger.info("Test message from script")
    logger.error("Test error message")
    
    print("4. Checking log files...")
    forward_log = logs_dir / "forward.log"
    error_log = logs_dir / "error.log"
    
    if forward_log.exists():
        print(f"✅ Forward log exists: {forward_log.stat().st_size} bytes")
        print("   Last 5 lines:")
        with open(forward_log, 'r') as f:
            lines = f.readlines()
            for line in lines[-5:]:
                print(f"   {line.strip()}")
    else:
        print("❌ Forward log not found")
    
    if error_log.exists():
        print(f"✅ Error log exists: {error_log.stat().st_size} bytes")
    else:
        print("❌ Error log not found")
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc() 