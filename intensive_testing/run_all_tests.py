#!/usr/bin/env python3
"""
Comprehensive test runner for all intensive Cohen's d validation tests.
This script runs all test modules and provides a complete validation summary.
"""

import os
import sys
import subprocess
import time

def run_test_module(module_path, module_name):
 """Run a test module and return the results."""
 print(f"\n{'='*60}")
 print(f"🧪 RUNNING {module_name.upper()}")
 print(f"{'='*60}")

 start_time = time.time()

 try:
 # Use subprocess to get cleaner output
 python_exec = sys.executable
 result = subprocess.run(
 [python_exec, module_path],
 cwd=os.path.dirname(module_path),
 capture_output=True,
 text=True,
 timeout=300 # 5 minute timeout
 )

 elapsed = time.time() - start_time

 print(result.stdout)
 if result.stderr:
 print("STDERR:")
 print(result.stderr)

 success = result.returncode == 0

 print(f"\n⏱️ {module_name} completed in {elapsed:.2f} seconds")

 if success:
 print(f"[PASS] {module_name} PASSED")
 return True, elapsed, result.stdout
 else:
 print(f"[FAIL] {module_name} FAILED")
 return False, elapsed, result.stdout

 except subprocess.TimeoutExpired:
 print(f"⏰ {module_name} timed out after 5 minutes")
 return False, 300, ""
 except Exception as e:
 print(f"[ERROR] {module_name} crashed: {e}")
 return False, 0, ""


def main():
 """Run all intensive validation tests."""
 print(" COMPREHENSIVE COHEN'S D INTENSIVE VALIDATION")
 print("=" * 60)
 print("Running complete validation suite for SciPy proposal readiness...")

 # Define test modules
 test_dir = os.path.dirname(os.path.abspath(__file__))
 test_modules = [
 ("test_numerical_validation.py", "Numerical Validation"),
 ("test_edge_cases.py", "Edge Cases"),
 ("test_performance.py", "Performance"),
 ("test_multidimensional.py", "Multidimensional"),
 ]

 # Run all tests
 results = []
 total_start = time.time()

 for filename, name in test_modules:
 module_path = os.path.join(test_dir, filename)
 if os.path.exists(module_path):
 success, elapsed, output = run_test_module(module_path, name)
 results.append((name, success, elapsed, output))
 else:
 print(f"[WARN] Module {filename} not found")
 results.append((name, False, 0, f"Module {filename} not found"))

 total_elapsed = time.time() - total_start

 # Summary
 print(f"\n{'='*60}")
 print(" COMPREHENSIVE VALIDATION SUMMARY")
 print(f"{'='*60}")

 passed = sum(1 for _, success, _, _ in results if success)
 total = len(results)

 print(f"Overall Results: {passed}/{total} test modules passed")
 print(f"Total Runtime: {total_elapsed:.2f} seconds")
 print()

 for name, success, elapsed, output in results:
 status = "[PASS] PASSED" if success else "[FAIL] FAILED"
 print(f"{status:<12} {name:<25} ({elapsed:>6.2f}s)")

 # Extract test counts from output if available
 if "passed" in output and "failed" in output:
 # Try to extract test counts
 lines = output.split('\n')
 for line in lines:
 if " Results:" in line:
 print(f"{'':>14} {line.strip()}")
 break

 print("\n" + "="*60)

 if passed == total:
 print(" ALL INTENSIVE VALIDATION TESTS PASSED!")
 print("✨ Your Cohen's d implementation is ready for SciPy proposal!")
 print("\n Validation Coverage:")
 print(" [PASS] Mathematical correctness against literature")
 print(" [PASS] Edge cases and boundary conditions")
 print(" [PASS] Performance with large datasets")
 print(" [PASS] Multidimensional array handling")
 print(" [PASS] All parameter combinations")
 print(" [PASS] NaN handling strategies")
 print(" [PASS] Numerical precision limits")
 print(" [PASS] Broadcasting and axis operations")

 print("\n📝 Next Steps for SciPy Proposal:")
 print(" 1. Document all validation results")
 print(" 2. Prepare performance benchmarks")
 print(" 3. Create API documentation")
 print(" 4. Submit enhancement proposal")

 return 0
 else:
 print(f"[WARN] {total - passed} test module(s) failed")
 print("Please review and fix failing tests before SciPy proposal")
 return 1


if __name__ == "__main__":
 exit(main())