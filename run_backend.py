#!/usr/bin/env python3
"""
Run PAMS backend server
"""
import sys
import os

# Add parent directory to path so we can import backend module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Now run the main_simple module
from backend import main_simple

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(main_simple.app, host="0.0.0.0", port=8000)
