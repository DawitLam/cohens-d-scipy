"""
Comprehensive edge case testing for Cohen's d implementation.

Tests boundary conditions, extreme values, and unusual input scenarios
that could cause numerical instability or unexpected behavior.
"""

import numpy as np
import pytest
import sys
import os

# Add the package directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), 'cohens_d_package'))

try:
    from cohens_d import cohens_d
except ImportError:
    # Fallback for different directory structures
    sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
    from cohens_d_package.cohens_d import cohens_d


class TestEdgeCases:
    """Test edge cases and boundary conditions."""
    
    def test_empty_arrays(self):
        """Test behavior with empty arrays."""
        
        # Empty arrays should return NaN
        result = cohens_d([], [])
        assert np.isnan(result), f"Empty arrays should return NaN, got {result}"
        
        # One empty, one non-empty
        result = cohens_d([1, 2, 3], [])
        assert np.isnan(result), f"One empty array should return NaN, got {result}"
    
    def test_single_value_arrays(self):
        """Test with single-value arrays."""
        
        # Single values - should return NaN due to zero variance
        result = cohens_d([5], [7])
        assert np.isnan(result), f"Single values should return NaN, got {result}"
        
        # Single identical values
        result = cohens_d([5], [5])
        assert np.isnan(result), f"Identical single values should return NaN, got {result}"
    
    def test_identical_arrays(self):
        """Test with identical arrays."""
        
        # Completely identical arrays
        x = [1, 2, 3, 4, 5]
        result = cohens_d(x, x)
        assert abs(result) < 1e-10, f"Identical arrays should give d≈0, got {result}"
        
        # Arrays with identical means and SDs
        x = [1, 3, 5]
        y = [2, 4, 6]  # Same pattern, shifted
        result = cohens_d(x, y)
        # Should be non-zero but finite
        assert np.isfinite(result), f"Similar patterns should give finite result, got {result}"
    
    def test_zero_variance_cases(self):
        """Test cases where variance is zero."""
        
        # All identical values in both groups (zero pooled variance)
        x = [5, 5, 5, 5, 5]
        y = [3, 3, 3, 3, 3]
        result = cohens_d(x, y)
        assert np.isnan(result), f"Zero pooled variance should return NaN, got {result}"
        
        # One group with zero variance, other with non-zero (valid case)
        x = [5, 5, 5, 5, 5]
        y = [1, 2, 3, 4, 5]
        result = cohens_d(x, y)
        assert np.isfinite(result), f"One zero variance should be finite, got {result}"
        
        # Test with unpooled variance when one group has zero variance
        result_unpooled = cohens_d(x, y, pooled=False)
        assert np.isnan(result_unpooled), f"Unpooled with zero variance should return NaN, got {result_unpooled}"
    
    def test_extreme_values(self):
        """Test with extreme numerical values."""
        
        # Very large values
        x = [1e10, 1e10 + 1, 1e10 + 2]
        y = [2e10, 2e10 + 1, 2e10 + 2]
        result = cohens_d(x, y)
        assert np.isfinite(result), f"Large values should give finite result, got {result}"
        
        # Very small values
        x = [1e-10, 2e-10, 3e-10]
        y = [4e-10, 5e-10, 6e-10]
        result = cohens_d(x, y)
        assert np.isfinite(result), f"Small values should give finite result, got {result}"
        
        # Mixed extreme values
        x = [-1e6, 0, 1e6]
        y = [-2e6, 0, 2e6]
        result = cohens_d(x, y)
        assert np.isfinite(result), f"Mixed extreme values should give finite result, got {result}"
    
    def test_infinite_values(self):
        """Test behavior with infinite values."""
        
        # Arrays containing infinity
        x = [1, 2, np.inf]
        y = [4, 5, 6]
        result = cohens_d(x, y)
        assert np.isnan(result), f"Infinite values should return NaN, got {result}"
        
        # Both arrays with infinity
        x = [1, np.inf, 3]
        y = [4, np.inf, 6]
        result = cohens_d(x, y)
        assert np.isnan(result), f"Both infinite should return NaN, got {result}"
        
        # Negative infinity
        x = [1, 2, -np.inf]
        y = [4, 5, 6]
        result = cohens_d(x, y)
        assert np.isnan(result), f"Negative infinity should return NaN, got {result}"
    
    def test_nan_values_propagate(self):
        """Test NaN handling with propagate policy."""
        
        # Default behavior should propagate NaN
        x = [1, 2, np.nan]
        y = [4, 5, 6]
        result = cohens_d(x, y, nan_policy='propagate')
        assert np.isnan(result), f"NaN propagate should return NaN, got {result}"
        
        # Both arrays with NaN
        x = [1, np.nan, 3]
        y = [4, np.nan, 6]
        result = cohens_d(x, y, nan_policy='propagate')
        assert np.isnan(result), f"Both NaN propagate should return NaN, got {result}"
    
    def test_nan_values_omit(self):
        """Test NaN handling with omit policy."""
        
        # Should ignore NaN values
        x = [1, 2, np.nan, 4, 5]
        y = [6, 7, 8, np.nan, 10]
        result = cohens_d(x, y, nan_policy='omit')
        assert np.isfinite(result), f"NaN omit should give finite result, got {result}"
        
        # All NaN should return NaN
        x = [np.nan, np.nan, np.nan]
        y = [1, 2, 3]
        result = cohens_d(x, y, nan_policy='omit')
        assert np.isnan(result), f"All NaN should return NaN, got {result}"
    
    def test_nan_values_raise(self):
        """Test NaN handling with raise policy."""
        
        # Should raise an error
        x = [1, 2, np.nan]
        y = [4, 5, 6]
        
        with pytest.raises(ValueError, match="Input x contains NaN values"):
            cohens_d(x, y, nan_policy='raise')
        
        # NaN in second array
        x = [1, 2, 3]
        y = [4, np.nan, 6]
        
        with pytest.raises(ValueError, match="Input y contains NaN values"):
            cohens_d(x, y, nan_policy='raise')
    
    def test_mismatched_array_lengths(self):
        """Test arrays with different lengths."""
        
        # Different length arrays should work fine for independent samples
        x = [1, 2, 3]
        y = [4, 5, 6, 7, 8]
        result = cohens_d(x, y)
        assert np.isfinite(result), f"Different lengths should work, got {result}"
        
        # But should fail for paired samples
        with pytest.raises(ValueError):
            cohens_d(x, y, paired=True)
    
    def test_single_element_after_nan_removal(self):
        """Test cases where NaN removal leaves too few elements."""
        
        # Array with mostly NaN values
        x = [1, np.nan, np.nan, np.nan]
        y = [np.nan, 2, np.nan, np.nan]
        result = cohens_d(x, y, nan_policy='omit')
        # Should handle gracefully (might return NaN for insufficient data)
        assert np.isnan(result), f"Insufficient data after NaN removal should return NaN, got {result}"
    
    def test_very_unequal_variances(self):
        """Test with extremely unequal variances."""
        
        # One group with very high variance
        x = [0, 0.01, 0.02]  # Low variance
        y = [-100, 0, 100]   # High variance
        
        result_pooled = cohens_d(x, y, pooled=True)
        result_unpooled = cohens_d(x, y, pooled=False)
        
        assert np.isfinite(result_pooled), f"Pooled with unequal variance should be finite, got {result_pooled}"
        assert np.isfinite(result_unpooled), f"Unpooled with unequal variance should be finite, got {result_unpooled}"
        
        # Results should be quite different
        assert abs(result_pooled - result_unpooled) > 0.1, "Pooled vs unpooled should differ significantly with unequal variances"
    
    def test_numerical_precision_limits(self):
        """Test numerical precision at machine limits."""
        
        # Values very close to machine epsilon
        eps = np.finfo(float).eps
        x = [eps, 2*eps, 3*eps]
        y = [4*eps, 5*eps, 6*eps]
        
        result = cohens_d(x, y)
        # Should either be finite or NaN, not crash
        assert np.isfinite(result) or np.isnan(result), f"Machine precision test failed: {result}"
    
    def test_integer_vs_float_consistency(self):
        """Test that integer and float inputs give same results."""
        
        # Integer inputs
        x_int = [1, 2, 3, 4, 5]
        y_int = [6, 7, 8, 9, 10]
        result_int = cohens_d(x_int, y_int)
        
        # Float inputs  
        x_float = [1.0, 2.0, 3.0, 4.0, 5.0]
        y_float = [6.0, 7.0, 8.0, 9.0, 10.0]
        result_float = cohens_d(x_float, y_float)
        
        assert abs(result_int - result_float) < 1e-10, f"Integer vs float inconsistency: {result_int} vs {result_float}"


if __name__ == "__main__":
    # Run the tests
    test_suite = TestEdgeCases()
    
    print("Running comprehensive edge case tests...")
    
    test_methods = [method for method in dir(test_suite) if method.startswith('test_')]
    
    passed = 0
    failed = 0
    errors = 0
    
    for test_method in test_methods:
        try:
            getattr(test_suite, test_method)()
            print(f"✅ {test_method}")
            passed += 1
        except AssertionError as e:
            print(f"❌ {test_method}: {e}")
            failed += 1
        except Exception as e:
            print(f"💥 {test_method}: {type(e).__name__}: {e}")
            errors += 1
    
    print(f"\n📊 Results: {passed} passed, {failed} failed, {errors} errors")
    
    if failed == 0 and errors == 0:
        print("🎉 All edge case tests passed!")
    else:
        print("⚠️  Some tests failed - need investigation")