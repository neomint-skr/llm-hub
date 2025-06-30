#!/bin/bash
# Test Summary Script
# Collects all test results and generates overview report

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
REPORT_FILE="$SCRIPT_DIR/test-report.txt"

echo "LLM Hub Test Summary Generator"
echo "=============================="
echo "Project Root: $PROJECT_ROOT"
echo "Report File: $REPORT_FILE"
echo

# Initialize report file
cat > "$REPORT_FILE" << EOF
LLM Hub Test Summary Report
===========================
Generated: $(date)
Project: LLM Hub
Version: 1.0.0

EOF

# Function to add section to report
add_section() {
    local title="$1"
    local content="$2"
    
    echo "$title" >> "$REPORT_FILE"
    echo "$(echo "$title" | sed 's/./=/g')" >> "$REPORT_FILE"
    echo "$content" >> "$REPORT_FILE"
    echo "" >> "$REPORT_FILE"
}

# Function to run test and capture result
run_test_for_summary() {
    local test_name="$1"
    local test_command="$2"
    local start_time=$(date +%s)
    
    echo "Running $test_name..."
    
    if eval "$test_command" > /tmp/test_output.log 2>&1; then
        local end_time=$(date +%s)
        local duration=$((end_time - start_time))
        echo "✓ $test_name completed in ${duration}s"
        echo "$test_name | PASS | ${duration}s" >> /tmp/test_results.txt
        return 0
    else
        local end_time=$(date +%s)
        local duration=$((end_time - start_time))
        echo "✗ $test_name failed in ${duration}s"
        echo "$test_name | FAIL | ${duration}s" >> /tmp/test_results.txt
        return 1
    fi
}

# Initialize test results file
echo "Test Name | Status | Duration" > /tmp/test_results.txt
echo "---------|--------|----------" >> /tmp/test_results.txt

# Test execution summary
echo "Collecting test results..."
echo

# Check if mock server is available
if curl -f http://localhost:1234/v1/models >/dev/null 2>&1; then
    MOCK_STATUS="RUNNING"
else
    MOCK_STATUS="NOT RUNNING"
fi

# Check if services are running
if docker-compose -f "$PROJECT_ROOT/ops/compose/docker-compose.yml" ps | grep -q "Up"; then
    SERVICES_STATUS="RUNNING"
else
    SERVICES_STATUS="NOT RUNNING"
fi

# Run available tests
TOTAL_TESTS=0
PASSED_TESTS=0

# Rule0 compliance check
if [ -f "$SCRIPT_DIR/rule0-check.sh" ]; then
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    if run_test_for_summary "Rule0 Compliance" "bash '$SCRIPT_DIR/rule0-check.sh'"; then
        PASSED_TESTS=$((PASSED_TESTS + 1))
    fi
fi

# MCP compliance check
if [ -f "$SCRIPT_DIR/mcp-compliance-test.sh" ]; then
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    if run_test_for_summary "MCP Compliance" "bash '$SCRIPT_DIR/mcp-compliance-test.sh'"; then
        PASSED_TESTS=$((PASSED_TESTS + 1))
    fi
fi

# Integration test (only if services are running)
if [ "$SERVICES_STATUS" = "RUNNING" ] && [ -f "$SCRIPT_DIR/integration-test.sh" ]; then
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    if run_test_for_summary "Integration Test" "bash '$SCRIPT_DIR/integration-test.sh'"; then
        PASSED_TESTS=$((PASSED_TESTS + 1))
    fi
fi

# Python tests (only if services are running)
if [ "$SERVICES_STATUS" = "RUNNING" ]; then
    export API_KEY="${API_KEY:-changeme}"
    
    if [ -f "$SCRIPT_DIR/inference-test.py" ]; then
        TOTAL_TESTS=$((TOTAL_TESTS + 1))
        if run_test_for_summary "Inference Test" "cd '$SCRIPT_DIR' && python3 inference-test.py"; then
            PASSED_TESTS=$((PASSED_TESTS + 1))
        fi
    fi
    
    if [ -f "$SCRIPT_DIR/error-test.py" ]; then
        TOTAL_TESTS=$((TOTAL_TESTS + 1))
        if run_test_for_summary "Error Handling Test" "cd '$SCRIPT_DIR' && python3 error-test.py"; then
            PASSED_TESTS=$((PASSED_TESTS + 1))
        fi
    fi
    
    if [ -f "$SCRIPT_DIR/direct-test.py" ]; then
        TOTAL_TESTS=$((TOTAL_TESTS + 1))
        if run_test_for_summary "Direct Access Test" "cd '$SCRIPT_DIR' && python3 direct-test.py"; then
            PASSED_TESTS=$((PASSED_TESTS + 1))
        fi
    fi
    
    if [ -f "$SCRIPT_DIR/model-update-test.py" ]; then
        TOTAL_TESTS=$((TOTAL_TESTS + 1))
        if run_test_for_summary "Model Update Test" "cd '$SCRIPT_DIR' && python3 model-update-test.py"; then
            PASSED_TESTS=$((PASSED_TESTS + 1))
        fi
    fi
fi

FAILED_TESTS=$((TOTAL_TESTS - PASSED_TESTS))
SUCCESS_RATE=0
if [ $TOTAL_TESTS -gt 0 ]; then
    SUCCESS_RATE=$((PASSED_TESTS * 100 / TOTAL_TESTS))
fi

# Generate summary report
add_section "System Status" "Mock Server: $MOCK_STATUS
Docker Services: $SERVICES_STATUS
Test Environment: $(if [ "$SERVICES_STATUS" = "RUNNING" ]; then echo "READY"; else echo "LIMITED"; fi)"

add_section "Test Results Summary" "Total Tests: $TOTAL_TESTS
Passed: $PASSED_TESTS
Failed: $FAILED_TESTS
Success Rate: $SUCCESS_RATE%"

# Add detailed results table
if [ -f /tmp/test_results.txt ]; then
    add_section "Detailed Results" "$(cat /tmp/test_results.txt)"
fi

# Add recommendations
RECOMMENDATIONS=""
if [ $FAILED_TESTS -gt 0 ]; then
    RECOMMENDATIONS="- Review failed test logs for specific issues
- Check system requirements and dependencies
- Verify Docker and LM Studio are running properly"
elif [ "$SERVICES_STATUS" = "NOT RUNNING" ]; then
    RECOMMENDATIONS="- Start services with start.bat to run full test suite
- Current results show static validation only"
else
    RECOMMENDATIONS="- All tests passed successfully
- System is ready for production use
- Consider running tests periodically"
fi

add_section "Recommendations" "$RECOMMENDATIONS"

# Add system information
SYSTEM_INFO="Operating System: $(uname -s 2>/dev/null || echo "Windows")
Docker Version: $(docker --version 2>/dev/null || echo "Not available")
Python Version: $(python3 --version 2>/dev/null || echo "Not available")
Timestamp: $(date)"

add_section "System Information" "$SYSTEM_INFO"

# Display summary
echo
echo "Test Summary Generated"
echo "======================"
echo "Report saved to: $REPORT_FILE"
echo
echo "Quick Summary:"
echo "  Total Tests: $TOTAL_TESTS"
echo "  Passed: $PASSED_TESTS"
echo "  Failed: $FAILED_TESTS"
echo "  Success Rate: $SUCCESS_RATE%"
echo

# Display overall status
if [ $FAILED_TESTS -eq 0 ] && [ $TOTAL_TESTS -gt 0 ]; then
    echo "✓ ALL TESTS PASSED"
    exit 0
elif [ $TOTAL_TESTS -eq 0 ]; then
    echo "⚠ NO TESTS EXECUTED"
    echo "Start services to run full test suite"
    exit 0
else
    echo "✗ SOME TESTS FAILED"
    echo "Check $REPORT_FILE for details"
    exit 1
fi
