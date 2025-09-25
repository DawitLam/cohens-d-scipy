#!/bin/bash
# Docker test runner script

echo "=== CROSS-PLATFORM COHEN'S D TESTING ==="
echo "OS: $(uname -a)"
echo "Python: $(python --version)"
echo "NumPy: $(python -c 'import numpy; print(numpy.__version__)')"
echo ""

echo "=== Running Standard Test Suite ==="
cd cohens_d_package
python -m pytest tests/ -v --tb=short
test_exit=$?

echo ""
echo "=== Running Intensive Validation ==="
cd ../intensive_testing

echo "1. Numerical validation..."
python test_numerical_validation.py
echo "2. Edge cases..."
python test_edge_cases.py
echo "3. Performance tests..."
python test_performance.py
echo "4. Multidimensional tests..."
python test_multidimensional.py

echo ""
echo "=== Testing Package Build ==="
cd ../cohens_d_package
python -m pip install build
python -m build
pip install dist/*.whl
python -c "import cohens_d; print(f'Package test: Cohen d v{cohens_d.__version__} works!')"

echo ""
if [ $test_exit -eq 0 ]; then
 echo "[PASS] All cross-platform tests PASSED"
 exit 0
else
 echo "[FAIL] Some tests FAILED"
 exit 1
fi