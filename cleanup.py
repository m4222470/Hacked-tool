"""
Python cleanup script to consolidate all source code into src/
Run this to remove root-level duplicate directories after verification.
"""

import os
import sys
import shutil
from pathlib import Path
from datetime import datetime

def cleanup_old_directories(backup=False):
    """Remove old root-level source code directories"""
    
    root_dirs_to_remove = ['core', 'evasion', 'utils', 'modules']
    src_path = Path('src')
    
    print("🧹 Hacked-tool Architecture Consolidation Cleanup")
    print("=" * 50)
    print()
    
    # Verify src/ versions exist
    missing_dirs = []
    for dir_name in root_dirs_to_remove:
        src_version = src_path / dir_name
        if not src_version.exists():
            missing_dirs.append(dir_name)
    
    if missing_dirs:
        print(f"❌ ERROR: src/ is missing: {', '.join(missing_dirs)}")
        print("Cannot proceed with cleanup until src/ has all directories.")
        return False
    
    # Backup if requested
    if backup:
        backup_dir = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        print(f"📦 Creating backup in {backup_dir}/")
        os.makedirs(backup_dir, exist_ok=True)
        
        for dir_name in root_dirs_to_remove:
            src_dir = Path(dir_name)
            if src_dir.exists():
                dest = Path(backup_dir) / dir_name
                shutil.copytree(src_dir, dest)
                print(f"  ✅ Backed up {dir_name}/")
        print()
    
    # Remove old directories
    print("🗑️  Removing old root-level directories...")
    removed_count = 0
    
    for dir_name in root_dirs_to_remove:
        root_dir = Path(dir_name)
        src_version = src_path / dir_name
        
        if root_dir.exists() and src_version.exists():
            shutil.rmtree(root_dir)
            print(f"  ❌ Removed {dir_name}/")
            removed_count += 1
        elif root_dir.exists():
            print(f"  ⚠️  Skipped {dir_name}/ (src/ version missing)")
        else:
            print(f"  ℹ️  {dir_name}/ not found (already removed?)")
    
    print()
    print("✅ Cleanup Complete!")
    print(f"   Removed {removed_count} directories")
    print()
    
    # Display final structure
    print("Final structure:")
    for item in sorted(src_path.iterdir()):
        if item.is_dir() and not item.name.startswith('__'):
            print(f"  src/{item.name}/ ✅")
    print()
    
    return True

def verify_imports():
    """Verify that imports work correctly"""
    print("🔍 Verifying imports...")
    
    try:
        # Add src to path for imports
        sys.path.insert(0, str(Path('src').absolute()))
        
        from core.engine import engine
        from core.rate_limiter import AdaptiveRateLimiter
        from evasion.header_randomizer import HeaderRandomizer
        from utils import URLUtils, URLValidator
        from plugins import BasePlugin
        
        print("  ✅ All imports successful!")
        return True
    except ImportError as e:
        print(f"  ❌ Import failed: {e}")
        return False

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Consolidate Hacked-tool source code structure'
    )
    parser.add_argument(
        '--backup',
        action='store_true',
        help='Create backup before removing directories'
    )
    parser.add_argument(
        '--verify',
        action='store_true',
        help='Verify imports before cleanup'
    )
    parser.add_argument(
        '--force',
        action='store_true',
        help='Skip confirmation prompts'
    )
    
    args = parser.parse_args()
    
    # Verify if requested
    if args.verify:
        if not verify_imports():
            print("\n⚠️  Import verification failed. Aborting cleanup.")
            sys.exit(1)
        print()
    
    # Confirm before cleanup
    if not args.force:
        print("⚠️  This will remove old directories from root:")
        print("   core/, evasion/, utils/, modules/")
        print()
        response = input("Continue? (yes/no): ").lower().strip()
        if response not in ['yes', 'y']:
            print("Cleanup cancelled.")
            sys.exit(0)
        print()
    
    # Run cleanup
    success = cleanup_old_directories(backup=args.backup)
    
    if success:
        print("✅ Next: Run tests to verify")
        print("   python -m pytest tests/ -v")
        sys.exit(0)
    else:
        print("❌ Cleanup failed. Please check errors above.")
        sys.exit(1)
