#!/bin/bash
# Cleanup script to remove root-level duplicate directories
# Run this AFTER verifying the src/ directory has all the code

set -e

echo "🧹 Hacked-tool Architecture Cleanup"
echo "===================================="
echo ""

# Backup directory (optional)
BACKUP_DIR="backup_$(date +%Y%m%d_%H%M%S)"

if [ "$1" == "--backup" ]; then
    echo "📦 Creating backup in $BACKUP_DIR/"
    mkdir -p "$BACKUP_DIR"
    cp -r core/ "$BACKUP_DIR/" 2>/dev/null || true
    cp -r evasion/ "$BACKUP_DIR/" 2>/dev/null || true
    cp -r utils/ "$BACKUP_DIR/" 2>/dev/null || true
    cp -r modules/ "$BACKUP_DIR/" 2>/dev/null || true
    echo "✅ Backup created"
    echo ""
fi

# Remove old directories
echo "🗑️  Removing old root-level directories..."

if [ -d "core" ] && [ -d "src/core" ]; then
    echo "  ❌ Removing core/"
    rm -rf core/
    echo "  ✅ Removed"
fi

if [ -d "evasion" ] && [ -d "src/evasion" ]; then
    echo "  ❌ Removing evasion/"
    rm -rf evasion/
    echo "  ✅ Removed"
fi

if [ -d "utils" ] && [ -d "src/utils" ]; then
    echo "  ❌ Removing utils/"
    rm -rf utils/
    echo "  ✅ Removed"
fi

if [ -d "modules" ] && [ -d "src/modules" ]; then
    echo "  ❌ Removing modules/"
    rm -rf modules/
    echo "  ✅ Removed"
fi

echo ""
echo "✅ Cleanup Complete!"
echo ""
echo "Final structure:"
echo "  src/"
echo "  ├── core/        ✅"
echo "  ├── modules/     ✅"
echo "  ├── plugins/     ✅"
echo "  ├── utils/       ✅"
echo "  ├── evasion/     ✅"
echo "  └── __init__.py  ✅"
echo ""
echo "Run tests to verify:"
echo "  python -m pytest tests/ -v"
