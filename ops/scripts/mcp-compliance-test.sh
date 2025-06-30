#!/bin/bash
# MCP Compliance Test Script
# Runs mcp-validate.py for both units to check full MCP compliance

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

echo "MCP Compliance Validation"
echo "========================="
echo "Project Root: $PROJECT_ROOT"
echo

# Check if mcp-validate.py exists
if [ ! -f "$SCRIPT_DIR/mcp-validate.py" ]; then
    echo "ERROR: mcp-validate.py not found in $SCRIPT_DIR"
    exit 1
fi

echo "Found MCP validator: $SCRIPT_DIR/mcp-validate.py"
echo

# Validation results tracking
TOTAL_VALIDATIONS=0
PASSED_VALIDATIONS=0
FAILED_VALIDATIONS=0

# Function to run validation for a unit
validate_unit() {
    local unit_name="$1"
    local unit_path="$PROJECT_ROOT/units/$unit_name"
    
    echo "Validating unit: $unit_name"
    echo "Unit path: $unit_path"
    echo "-" | head -c 40
    echo
    
    TOTAL_VALIDATIONS=$((TOTAL_VALIDATIONS + 1))
    
    if [ ! -d "$unit_path" ]; then
        echo "✗ Unit directory not found: $unit_path"
        FAILED_VALIDATIONS=$((FAILED_VALIDATIONS + 1))
        return 1
    fi
    
    # Check for required files
    if [ ! -f "$unit_path/unit.yml" ]; then
        echo "✗ Missing unit.yml in $unit_name"
        FAILED_VALIDATIONS=$((FAILED_VALIDATIONS + 1))
        return 1
    fi
    
    if [ ! -f "$unit_path/mcp-validation.yml" ]; then
        echo "✗ Missing mcp-validation.yml in $unit_name"
        FAILED_VALIDATIONS=$((FAILED_VALIDATIONS + 1))
        return 1
    fi
    
    echo "✓ Required files present"
    
    # Run MCP validation
    echo "Running MCP validation..."
    
    if python3 "$SCRIPT_DIR/mcp-validate.py" "$unit_path"; then
        echo "✓ $unit_name MCP validation PASSED"
        PASSED_VALIDATIONS=$((PASSED_VALIDATIONS + 1))
        return 0
    else
        echo "✗ $unit_name MCP validation FAILED"
        FAILED_VALIDATIONS=$((FAILED_VALIDATIONS + 1))
        return 1
    fi
}

# Validate lm-studio-bridge
echo "Validation 1: LM Studio Bridge"
echo "==============================="
validate_unit "lm-studio-bridge"
echo

# Validate unified-gateway
echo "Validation 2: Unified Gateway"
echo "============================="
validate_unit "unified-gateway"
echo

# Summary
echo "MCP Compliance Summary"
echo "======================"
echo "Total validations: $TOTAL_VALIDATIONS"
echo "Passed: $PASSED_VALIDATIONS"
echo "Failed: $FAILED_VALIDATIONS"
echo

# Overall result
if [ $FAILED_VALIDATIONS -eq 0 ]; then
    echo "✓ ALL UNITS PASS MCP COMPLIANCE"
    echo "Both units are fully MCP 2025-06-18 compliant"
    exit 0
else
    echo "✗ SOME UNITS FAILED MCP COMPLIANCE"
    echo "Please check the validation errors above"
    exit 1
fi
