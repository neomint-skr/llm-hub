#!/bin/bash
# Rule0 Compliance Checker
# Validates dedardf structure compliance

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

echo "Rule0 Compliance Check"
echo "Project Root: $PROJECT_ROOT"
echo "===================="

ERRORS=0

# Check for forbidden files in root
echo "Checking for forbidden files in root..."
if [ -f "$PROJECT_ROOT/Makefile" ]; then
    echo "ERROR: Makefile found in root (forbidden)"
    ERRORS=$((ERRORS + 1))
fi

if [ -f "$PROJECT_ROOT/.env" ]; then
    echo "ERROR: .env file found in root (forbidden)"
    ERRORS=$((ERRORS + 1))
fi

if [ -f "$PROJECT_ROOT/docker-compose.yml" ]; then
    echo "ERROR: docker-compose.yml found in root (forbidden)"
    ERRORS=$((ERRORS + 1))
fi

# Check for forbidden directories
echo "Checking for forbidden directories..."
if [ -d "$PROJECT_ROOT/tests" ]; then
    echo "ERROR: tests/ directory found (forbidden)"
    ERRORS=$((ERRORS + 1))
fi

if [ -d "$PROJECT_ROOT/platform/shared" ]; then
    echo "ERROR: platform/shared/ directory found (forbidden)"
    ERRORS=$((ERRORS + 1))
fi

# Check for relative imports between units
echo "Checking for relative imports between units..."
if [ -d "$PROJECT_ROOT/units" ]; then
    UNIT_IMPORTS=$(find "$PROJECT_ROOT/units" -name "*.py" -exec grep -l "from units\." {} \; 2>/dev/null || true)
    if [ -n "$UNIT_IMPORTS" ]; then
        echo "ERROR: Relative imports between units found:"
        echo "$UNIT_IMPORTS"
        ERRORS=$((ERRORS + 1))
    fi
fi

# Check for cross-unit imports
echo "Checking for cross-unit imports..."
if [ -d "$PROJECT_ROOT/units" ]; then
    for unit_dir in "$PROJECT_ROOT/units"/*; do
        if [ -d "$unit_dir" ]; then
            unit_name=$(basename "$unit_dir")
            OTHER_UNIT_IMPORTS=$(find "$unit_dir" -name "*.py" -exec grep -l "from units\.[^$unit_name]" {} \; 2>/dev/null || true)
            if [ -n "$OTHER_UNIT_IMPORTS" ]; then
                echo "ERROR: Cross-unit imports found in $unit_name:"
                echo "$OTHER_UNIT_IMPORTS"
                ERRORS=$((ERRORS + 1))
            fi
        fi
    done
fi

# Check required directory structure
echo "Checking required directory structure..."
REQUIRED_DIRS=(
    "platform"
    "platform/core"
    "platform/runtime"
    "platform/contracts"
    "units"
    "shared"
    "ops"
    "ops/scripts"
    "ops/compose"
    "docs"
    "docs/architecture"
    "docs/architecture/decisions"
    ".config"
)

for dir in "${REQUIRED_DIRS[@]}"; do
    if [ ! -d "$PROJECT_ROOT/$dir" ]; then
        echo "ERROR: Required directory missing: $dir"
        ERRORS=$((ERRORS + 1))
    fi
done

# Summary
echo "===================="
if [ $ERRORS -eq 0 ]; then
    echo "✓ Rule0 compliance check passed"
    exit 0
else
    echo "✗ Rule0 compliance check failed with $ERRORS errors"
    exit 1
fi
