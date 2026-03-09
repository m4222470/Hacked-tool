#!/usr/bin/env python3
"""
Hacked-tool Entry Point Wrapper
يحيل إلى نقطة الدخول الموحدة في src/main.py
"""

import sys
import importlib.util
from pathlib import Path

if __name__ == "__main__":
    # Load src/main.py directly to avoid circular imports
    src_main_path = Path(__file__).parent / 'src' / 'main.py'
    spec = importlib.util.spec_from_file_location("src_main", src_main_path)
    src_main = importlib.util.module_from_spec(spec)
    
    # Add root to sys.path for config imports in src/main.py
    sys.path.insert(0, str(Path(__file__).parent))
    
    spec.loader.exec_module(src_main)
    src_main.main()

