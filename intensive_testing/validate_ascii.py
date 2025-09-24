#!/usr/bin/env python3
"""
ASCII-compatible version of comprehensive test runner.
All tests but with ASCII-only output for Windows terminal compatibility.
"""

import os
import sys
import subprocess
import time

def run_standard_tests():
    """Run the standard test suite."""
    print("Running standard test suite...")
    
    try:
        test_dir = os.path.join(os.path.dirname(__file__), '..', 'cohens_d_package')
        python_exec = sys.executable
        
        # Run pytest
        result = subprocess.run(
            [python_exec, '-m', 'pytest', 'tests/', '-v'],
            cwd=test_dir,
            capture_output=True,
            text=True,
            timeout=60
        )
        
        print("STANDARD TEST OUTPUT:")
        print(result.stdout)
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"Standard tests failed to run: {e}")
        return False

def run_manual_validation():
    """Run manual validation tests."""
    print("\nRunning intensive manual validation...")
    print("=" * 50)
    
    # Import and run tests manually to avoid Unicode issues
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'cohens_d_package'))
    
    try:
        from cohens_d import cohens_d
        import numpy as np
        
        print("1. Basic functionality test...")
        np.random.seed(42)
        x = np.random.normal(0, 1, 1000)
        y = np.random.normal(0.5, 1, 1000)
        
        result = cohens_d(x, y)
        assert not np.isnan(result)
        assert 0.3 < abs(result) < 0.7
        print("   PASSED - Basic functionality")
        
        print("2. Large array performance test...")
        x_large = np.random.normal(0, 1, 100000)
        y_large = np.random.normal(0.5, 1, 100000)
        
        start_time = time.time()
        result_large = cohens_d(x_large, y_large)
        elapsed = time.time() - start_time
        
        assert not np.isnan(result_large)
        assert elapsed < 1.0  # Should be fast
        print(f"   PASSED - Large array test ({elapsed:.4f}s)")
        
        print("3. Multidimensional test...")
        x_2d = np.random.normal(0, 1, (100, 10))
        y_2d = np.random.normal(0.3, 1, (100, 10))
        
        result_axis0 = cohens_d(x_2d, y_2d, axis=0)
        result_axis1 = cohens_d(x_2d, y_2d, axis=1)
        
        assert result_axis0.shape == (10,)
        assert result_axis1.shape == (100,)
        assert not np.any(np.isnan(result_axis0))
        assert not np.any(np.isnan(result_axis1))
        print("   PASSED - Multidimensional test")
        
        print("4. Paired samples test...")
        before = np.random.normal(100, 15, 50)
        after = before + np.random.normal(2, 5, 50)
        
        result_paired = cohens_d(before, after, paired=True)
        assert not np.isnan(result_paired)
        print("   PASSED - Paired samples test")
        
        print("5. Bias correction test...")
        result_biased = cohens_d(x, y, bias_correction=False)
        result_unbiased = cohens_d(x, y, bias_correction=True)
        
        assert not np.isnan(result_biased)
        assert not np.isnan(result_unbiased)
        assert abs(result_biased) > abs(result_unbiased)  # Hedges' g should be smaller
        print("   PASSED - Bias correction test")
        
        print("6. NaN handling test...")
        x_nan = np.array([1, 2, np.nan, 4, 5])
        y_nan = np.array([2, 3, 4, np.nan, 6])
        
        result_omit = cohens_d(x_nan, y_nan, nan_policy='omit')
        result_prop = cohens_d(x_nan, y_nan, nan_policy='propagate')
        
        assert not np.isnan(result_omit)
        assert np.isnan(result_prop)
        print("   PASSED - NaN handling test")
        
        print("7. Edge cases test...")
        # Empty arrays should return NaN
        empty_result = cohens_d(np.array([]), np.array([]))
        assert np.isnan(empty_result)
        
        # Identical arrays should return 0
        identical = np.array([1, 2, 3, 4, 5])
        zero_result = cohens_d(identical, identical)
        assert abs(zero_result) < 1e-10
        
        # Single values should return NaN (zero variance)
        single_result = cohens_d(np.array([1]), np.array([2]))
        assert np.isnan(single_result)
        
        print("   PASSED - Edge cases test")
        
        print("\nAll validation tests PASSED!")
        return True
        
    except Exception as e:
        print(f"Validation test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run comprehensive validation."""
    print("=" * 60)
    print("COHEN'S D COMPREHENSIVE VALIDATION")
    print("=" * 60)
    print("ASCII-compatible validation for Windows terminal")
    print()
    
    # Run standard tests first
    standard_passed = run_standard_tests()
    
    # Run manual validation
    validation_passed = run_manual_validation()
    
    print("\n" + "=" * 60)
    print("FINAL SUMMARY")
    print("=" * 60)
    
    if standard_passed and validation_passed:
        print("SUCCESS: All validation tests passed!")
        print()
        print("Your Cohen's d implementation is validated for:")
        print("  - Mathematical correctness")
        print("  - Edge case handling") 
        print("  - Performance with large datasets")
        print("  - Multidimensional operations")
        print("  - All parameter combinations")
        print("  - NaN handling policies")
        print("  - Paired and unpaired samples")
        print("  - Bias correction (Hedges' g)")
        print()
        print("READY FOR SCIPY PROPOSAL!")
        return 0
    else:
        print("FAILED: Some validation tests failed")
        print(f"Standard tests: {'PASSED' if standard_passed else 'FAILED'}")
        print(f"Manual validation: {'PASSED' if validation_passed else 'FAILED'}")
        return 1

if __name__ == "__main__":
    exit(main())