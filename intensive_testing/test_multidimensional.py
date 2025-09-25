#!/usr/bin/env python3
"""
Multidimensional and axis behavior tests for Cohen's d implementation.
These tests ensure correct behavior across different array dimensions and axes.
"""

import numpy as np
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'cohens_d_package'))

from cohens_d import cohens_d


def test_multidimensional_consistency():
 """Test that multidimensional operations are consistent with 1D equivalents."""
 print(">> Testing multidimensional consistency...")

 np.random.seed(42)

 # Create 2D arrays
 x_2d = np.random.normal(0, 1, (100, 5))
 y_2d = np.random.normal(0.5, 1, (100, 5))

 # Test axis=0 (along rows)
 result_axis0 = cohens_d(x_2d, y_2d, axis=0)

 # Compare with column-wise 1D calculations
 for col in range(5):
 expected = cohens_d(x_2d[:, col], y_2d[:, col])
 actual = result_axis0[col]
 assert abs(actual - expected) < 1e-10, f"Column {col}: expected {expected}, got {actual}"

 # Test axis=1 (along columns)
 result_axis1 = cohens_d(x_2d, y_2d, axis=1)

 # Compare with row-wise 1D calculations
 for row in range(100):
 expected = cohens_d(x_2d[row, :], y_2d[row, :])
 actual = result_axis1[row]
 assert abs(actual - expected) < 1e-10, f"Row {row}: expected {expected}, got {actual}"

 # Test axis=None (flattened)
 result_none = cohens_d(x_2d, y_2d, axis=None)
 expected_none = cohens_d(x_2d.flatten(), y_2d.flatten())
 assert abs(result_none - expected_none) < 1e-10

 print("[PASS] Multidimensional consistency test passed")


def test_keepdims_behavior():
 """Test keepdims parameter behavior."""
 print(">> Testing keepdims behavior...")

 np.random.seed(42)
 x_3d = np.random.normal(0, 1, (10, 20, 5))
 y_3d = np.random.normal(0.3, 1, (10, 20, 5))

 # Test keepdims=True for each axis
 for axis in [0, 1, 2]:
 result_keepdims = cohens_d(x_3d, y_3d, axis=axis, keepdims=True)
 result_no_keepdims = cohens_d(x_3d, y_3d, axis=axis, keepdims=False)

 # Check shapes
 expected_shape = list(x_3d.shape)
 expected_shape[axis] = 1
 assert result_keepdims.shape == tuple(expected_shape), \
 f"keepdims shape mismatch for axis {axis}"

 # Check that values are the same when squeezed
 assert np.allclose(result_keepdims.squeeze(), result_no_keepdims), \
 f"keepdims values mismatch for axis {axis}"

 # Test axis=None with keepdims
 result_none_keepdims = cohens_d(x_3d, y_3d, axis=None, keepdims=True)
 result_none_no_keepdims = cohens_d(x_3d, y_3d, axis=None, keepdims=False)

 assert result_none_keepdims.shape == (1, 1, 1)
 assert result_none_no_keepdims.shape == ()
 assert np.allclose(result_none_keepdims.squeeze(), result_none_no_keepdims)

 print("[PASS] keepdims behavior test passed")


def test_high_dimensional_arrays():
 """Test with high-dimensional arrays."""
 print(">> Testing high-dimensional arrays...")

 np.random.seed(42)

 # Create 4D arrays
 shape_4d = (5, 6, 7, 8)
 x_4d = np.random.normal(0, 1, shape_4d)
 y_4d = np.random.normal(0.2, 1, shape_4d)

 # Test different axes
 for axis in [0, 1, 2, 3, None]:
 result = cohens_d(x_4d, y_4d, axis=axis)

 # Basic sanity checks
 assert not np.any(np.isnan(result))
 assert not np.any(np.isinf(result))

 # Check expected shape
 if axis is None:
 assert result.shape == ()
 else:
 expected_shape = list(shape_4d)
 expected_shape.pop(axis)
 assert result.shape == tuple(expected_shape)

 print("[PASS] High-dimensional arrays test passed")


def test_negative_axis_indexing():
 """Test negative axis indexing."""
 print(">> Testing negative axis indexing...")

 np.random.seed(42)
 x_3d = np.random.normal(0, 1, (10, 20, 5))
 y_3d = np.random.normal(0.3, 1, (10, 20, 5))

 # Test that negative and positive axis indices give same results
 axis_pairs = [(0, -3), (1, -2), (2, -1)]

 for pos_axis, neg_axis in axis_pairs:
 result_pos = cohens_d(x_3d, y_3d, axis=pos_axis)
 result_neg = cohens_d(x_3d, y_3d, axis=neg_axis)

 assert np.allclose(result_pos, result_neg), \
 f"Axis {pos_axis} and {neg_axis} should give same results"

 print("[PASS] Negative axis indexing test passed")


def test_axis_with_paired_samples():
 """Test axis parameter with paired samples."""
 print(">> Testing axis parameter with paired samples...")

 np.random.seed(42)

 # Create paired data where each row is a pair
 n_pairs = 50
 n_features = 10

 # Before-after measurements
 before = np.random.normal(100, 15, (n_pairs, n_features))
 after = before + np.random.normal(5, 3, (n_pairs, n_features)) # Small improvement

 # Test paired calculation along different axes
 # axis=0: Effect size for each feature across pairs
 result_axis0 = cohens_d(before, after, axis=0, paired=True)
 assert result_axis0.shape == (n_features,)

 # Manual verification for first feature
 diff = before[:, 0] - after[:, 0]
 expected_0 = np.mean(diff) / np.std(diff, ddof=1)
 assert abs(result_axis0[0] - expected_0) < 1e-10

 # axis=1: Effect size for each pair across features
 result_axis1 = cohens_d(before, after, axis=1, paired=True)
 assert result_axis1.shape == (n_pairs,)

 # axis=None: Overall effect size
 result_none = cohens_d(before, after, axis=None, paired=True)
 assert result_none.shape == ()

 print("[PASS] Axis with paired samples test passed")


def test_complex_multidimensional_scenarios():
 """Test complex multidimensional scenarios."""
 print(">> Testing complex multidimensional scenarios...")

 np.random.seed(42)

 # Scenario 1: Time series data (subjects × timepoints × conditions)
 subjects = 20
 timepoints = 100

 control_data = np.random.normal(0, 1, (subjects, timepoints))
 treatment_data = np.random.normal(0.3, 1, (subjects, timepoints)) # Different means

 # Effect size across subjects for each timepoint
 effect_per_timepoint = cohens_d(control_data, treatment_data, axis=0)
 assert effect_per_timepoint.shape == (timepoints,)
 # Should be reasonable effect sizes
 assert np.all(np.abs(effect_per_timepoint) < 2) # Reasonable range

 # Effect size across timepoints for each subject
 effect_per_subject = cohens_d(control_data, treatment_data, axis=1)
 assert effect_per_subject.shape == (subjects,)

 # Overall effect size
 overall_effect = cohens_d(control_data, treatment_data, axis=None)
 assert np.isscalar(overall_effect) or (isinstance(overall_effect, np.ndarray) and overall_effect.ndim == 0)

 print("[PASS] Complex multidimensional scenarios test passed")


def test_edge_cases_multidimensional():
 """Test edge cases in multidimensional settings."""
 print(">> Testing multidimensional edge cases...")

 # Single-element arrays along axis
 x_single = np.array([[1], [2], [3]]) # 3×1
 y_single = np.array([[2], [3], [4]]) # 3×1

 # Test along axis=0 (3 elements)
 result_axis0 = cohens_d(x_single, y_single, axis=0)
 assert result_axis0.shape == (1,)
 assert not np.isnan(result_axis0[0])

 # Should return NaN along axis=1 (single elements)
 result_axis1 = cohens_d(x_single, y_single, axis=1)
 assert result_axis1.shape == (3,)
 assert np.all(np.isnan(result_axis1)) # Single elements have zero variance

 # Arrays with some dimensions having single elements
 x_mixed = np.random.normal(0, 1, (1, 10, 5))
 y_mixed = np.random.normal(0.3, 1, (1, 10, 5))

 # Test along axis with multiple elements
 result_axis1 = cohens_d(x_mixed, y_mixed, axis=1)
 assert result_axis1.shape == (1, 5)
 assert not np.any(np.isnan(result_axis1))

 result_axis2 = cohens_d(x_mixed, y_mixed, axis=2)
 assert result_axis2.shape == (1, 10)
 assert not np.any(np.isnan(result_axis2))

 # Should return NaN along axis with single element
 result_axis0 = cohens_d(x_mixed, y_mixed, axis=0)
 assert result_axis0.shape == (10, 5)
 assert np.all(np.isnan(result_axis0))

 print("[PASS] Multidimensional edge cases test passed")


def main():
 """Run all multidimensional tests."""
 print("Running multidimensional validation tests...")
 print("=" * 50)

 test_functions = [
 test_multidimensional_consistency,
 test_keepdims_behavior,
 test_high_dimensional_arrays,
 test_negative_axis_indexing,
 test_axis_with_paired_samples,
 test_complex_multidimensional_scenarios,
 test_edge_cases_multidimensional,
 ]

 passed = 0
 failed = 0

 for test_func in test_functions:
 try:
 test_func()
 passed += 1
 except Exception as e:
 print(f"[FAIL] {test_func.__name__} failed: {e}")
 import traceback
 traceback.print_exc()
 failed += 1

 print("=" * 50)
 print(f" Results: {passed} passed, {failed} failed, 0 errors")

 if failed == 0:
 print(" All multidimensional tests passed!")
 else:
 print("[WARN] Some multidimensional tests failed")
 return 1

 return 0


if __name__ == "__main__":
 exit(main())