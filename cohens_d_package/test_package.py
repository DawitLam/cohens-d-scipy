#!/usr/bin/env python3
"""
Simple test script to verify the cohens_d package installation and basic functionality.
"""

import sys
import numpy as np

def test_basic_functionality():
    """Test basic package functionality."""
    print("Testing Cohen's d package...")
    
    try:
        # Import the package
        from cohens_d import cohens_d, __version__
        print(f"✓ Package imported successfully (version {__version__})")
        
        # Test basic two-sample calculation
        x = np.array([1, 2, 3, 4, 5])
        y = np.array([2, 3, 4, 5, 6])
        
        d = cohens_d(x, y)
        # Calculate expected value manually
        mean_x = np.mean(x)
        mean_y = np.mean(y)
        var_x = np.var(x, ddof=1)
        var_y = np.var(y, ddof=1)
        n_x, n_y = len(x), len(y)
        pooled_var = ((n_x - 1) * var_x + (n_y - 1) * var_y) / (n_x + n_y - 2)
        expected = (mean_x - mean_y) / np.sqrt(pooled_var)
        
        if abs(d - expected) < 1e-10:
            print(f"✓ Two-sample Cohen's d calculation: {d:.6f}")
        else:
            print(f"✗ Two-sample calculation failed: got {d}, expected {expected}")
            return False
            
        # Test one-sample calculation
        x_one = np.array([1, 2, 3, 4, 5])
        d_one = cohens_d(x_one)
        expected_one = np.mean(x_one) / np.std(x_one, ddof=1)
        
        if abs(d_one - expected_one) < 1e-10:
            print(f"✓ One-sample Cohen's d calculation: {d_one:.6f}")
        else:
            print(f"✗ One-sample calculation failed: got {d_one}, expected {expected_one}")
            return False
            
        # Test with random data
        np.random.seed(42)
        x_rand = np.random.normal(0, 1, 100)
        y_rand = np.random.normal(0.5, 1, 100)
        d_rand = cohens_d(x_rand, y_rand)
        
        if np.isfinite(d_rand):
            print(f"✓ Random data calculation: {d_rand:.6f}")
        else:
            print(f"✗ Random data calculation failed: {d_rand}")
            return False
            
        # Test NaN handling
        x_nan = np.array([1, 2, np.nan, 4, 5])
        y_nan = np.array([2, 3, 4, np.nan, 6])
        d_nan = cohens_d(x_nan, y_nan, nan_policy='omit')
        
        if np.isfinite(d_nan):
            print(f"✓ NaN handling (omit): {d_nan:.6f}")
        else:
            print(f"✗ NaN handling failed: {d_nan}")
            return False
            
        print("\n✓ All basic tests passed!")
        return True
        
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        return False
    except Exception as e:
        print(f"✗ Test failed with error: {e}")
        return False

def test_parameter_validation():
    """Test parameter validation."""
    print("\nTesting parameter validation...")
    
    from cohens_d import cohens_d
    
    x = np.array([1, 2, 3, 4, 5])
    y = np.array([2, 3, 4, 5, 6])
    
    # Test invalid nan_policy
    try:
        cohens_d(x, y, nan_policy='invalid')
        print("✗ Invalid nan_policy should raise ValueError")
        return False
    except ValueError:
        print("✓ Invalid nan_policy correctly raises ValueError")
    
    # Test invalid alternative
    try:
        cohens_d(x, y, alternative='invalid')
        print("✗ Invalid alternative should raise ValueError")
        return False
    except ValueError:
        print("✓ Invalid alternative correctly raises ValueError")
    
    print("✓ Parameter validation tests passed!")
    return True

def main():
    """Run all tests."""
    print("Cohen's d Package Test Suite")
    print("=" * 40)
    
    success = True
    success &= test_basic_functionality()
    success &= test_parameter_validation()
    
    print("\n" + "=" * 40)
    if success:
        print("🎉 All tests passed! Package is working correctly.")
        return 0
    else:
        print("❌ Some tests failed. Please check the package installation.")
        return 1

if __name__ == "__main__":
    sys.exit(main())