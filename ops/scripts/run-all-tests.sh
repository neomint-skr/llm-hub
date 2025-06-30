#!/bin/bash
# Test Runner Script
# Runs all test scripts sequentially with summary report

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

echo "LLM Hub Test Runner"
echo "==================="
echo "Project Root: $PROJECT_ROOT"
echo "Script Dir: $SCRIPT_DIR"
echo

# Test results tracking
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0
TEST_RESULTS=()

# Function to run a test and track results
run_test() {
    local test_name="$1"
    local test_command="$2"
    
    echo "Running: $test_name"
    echo "Command: $test_command"
    echo "-" | head -c 50
    echo
    
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    
    if eval "$test_command"; then
        echo "✓ $test_name PASSED"
        PASSED_TESTS=$((PASSED_TESTS + 1))
        TEST_RESULTS+=("PASS: $test_name")
    else
        echo "✗ $test_name FAILED"
        FAILED_TESTS=$((FAILED_TESTS + 1))
        TEST_RESULTS+=("FAIL: $test_name")
    fi
    
    echo
    echo "=" | head -c 50
    echo
}

# Start Mock Server
echo "Starting Mock LM Studio Server..."
python3 "$SCRIPT_DIR/lm-studio-mock.py" &
MOCK_PID=$!
echo "Mock Server PID: $MOCK_PID"

# Wait for Mock Server
sleep 3

# Verify Mock Server is running
if ! curl -f http://localhost:1234/v1/models >/dev/null 2>&1; then
    echo "ERROR: Mock LM Studio Server not responding"
    kill $MOCK_PID 2>/dev/null || true
    exit 1
fi
echo "✓ Mock Server running"
echo

# Cleanup function
cleanup() {
    echo "Cleaning up..."
    
    # Stop Docker services if running
    cd "$PROJECT_ROOT/ops/compose"
    docker-compose down >/dev/null 2>&1 || true
    
    # Stop Mock Server
    kill $MOCK_PID 2>/dev/null || true
    
    echo "✓ Cleanup completed"
}

# Set trap for cleanup
trap cleanup EXIT

# Run Integration Test
run_test "Integration Test" "cd '$SCRIPT_DIR' && bash integration-test.sh"

# Run Python Tests (only if integration passed)
if [ $FAILED_TESTS -eq 0 ]; then
    # Set environment for Python tests
    export API_KEY="${API_KEY:-changeme}"
    
    run_test "Inference Test" "cd '$SCRIPT_DIR' && python3 inference-test.py"
    run_test "Error Handling Test" "cd '$SCRIPT_DIR' && python3 error-test.py"
    run_test "Direct Access Test" "cd '$SCRIPT_DIR' && python3 direct-test.py"
else
    echo "Skipping Python tests due to integration test failure"
    TOTAL_TESTS=$((TOTAL_TESTS + 3))
    FAILED_TESTS=$((FAILED_TESTS + 3))
    TEST_RESULTS+=("SKIP: Inference Test (integration failed)")
    TEST_RESULTS+=("SKIP: Error Handling Test (integration failed)")
    TEST_RESULTS+=("SKIP: Direct Access Test (integration failed)")
fi

# Generate Summary Report
echo
echo "TEST SUMMARY REPORT"
echo "==================="
echo "Total Tests: $TOTAL_TESTS"
echo "Passed: $PASSED_TESTS"
echo "Failed: $FAILED_TESTS"
echo "Success Rate: $(( PASSED_TESTS * 100 / TOTAL_TESTS ))%"
echo

echo "Detailed Results:"
echo "-----------------"
for result in "${TEST_RESULTS[@]}"; do
    echo "$result"
done
echo

# Overall Status
if [ $FAILED_TESTS -eq 0 ]; then
    echo "✓ ALL TESTS PASSED"
    echo "System is ready for use!"
    exit 0
else
    echo "✗ SOME TESTS FAILED"
    echo "Please check the logs above for details"
    exit 1
fi
