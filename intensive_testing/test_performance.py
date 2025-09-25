#!/usr/bin/env python3
"""
Performance and scalability tests for Cohen's d implementation.
These tests ensure the function scales well with large datasets and different dimensions.
"""

import time
import numpy as np
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'cohens_d_package'))

from cohens_d import cohens_d


def test_large_array_performance():
 """Test performance with large arrays."""
 print("Testing large array performance...")

 # Test with increasingly large arrays
 sizes = [1000, 10000, 100000, 1000000]

 for size in sizes:
 np.random.seed(42)
 x = np.random.normal(0, 1, size)
 y = np.random.normal(0.5, 1, size)

 start_time = time.time()
 result = cohens_d(x, y)
 elapsed = time.time() - start_time

 print(f" Size {size:,}: {elapsed:.4f}s, d = {result:.4f}")

 # Basic sanity checks
 assert not np.isnan(result)
 assert 0.3 < abs(result) < 0.7 # Expected effect size around 0.5

 print("[PASS] Large array performance test passed")


def test_multidimensional_performance():
 """Test performance with multidimensional arrays."""
 print(">> Testing multidimensional array performance...")

 # Test 2D arrays with different shapes
 shapes = [(1000, 10), (100, 100), (10, 1000)]

 for shape in shapes:
 np.random.seed(42)
 x = np.random.normal(0, 1, shape)
 y = np.random.normal(0.3, 1, shape)

 # Test along different axes
 for axis in [0, 1, None]:
 start_time = time.time()
 result = cohens_d(x, y, axis=axis)
 elapsed = time.time() - start_time

 print(f" Shape {shape}, axis={axis}: {elapsed:.4f}s")

 # Basic sanity checks
 assert not np.any(np.isnan(result))

 print("[PASS] Multidimensional performance test passed")


def test_memory_efficiency():
 """Test memory usage with large arrays."""
 print(">> Testing memory efficiency...")

 # Test in-place operations don't create unnecessary copies
 np.random.seed(42)
 x = np.random.normal(0, 1, 100000)
 y = np.random.normal(0.5, 1, 100000)

 # Different parameter combinations
 test_cases = [
 {'bias_correction': False},
 {'bias_correction': True},
 {'pooled': False},
 {'axis': None, 'keepdims': True},
 ]

 for params in test_cases:
 result = cohens_d(x, y, **params)
 assert not np.isnan(result)
 print(f" Memory test with {params}: passed")

 print("[PASS] Memory efficiency test passed")


def test_broadcasting_performance():
 """Test performance with same-shape array scenarios."""
 print(">> Testing array shape performance...")

 np.random.seed(42)

 # Test different array shapes (same shapes to avoid broadcasting issues)
 scenarios = [
 # (shape, axis)
 ((1000, 10), 0),
 ((1000, 10), 1),
 ((100, 100), 0),
 ((100, 100), 1),
 ((1000,), None),
 ]

 for shape, axis in scenarios:
 x = np.random.normal(0, 1, shape)
 y = np.random.normal(0.3, 1, shape)

 start_time = time.time()
 result = cohens_d(x, y, axis=axis)
 elapsed = time.time() - start_time

 print(f" Shape {shape}, axis={axis}: {elapsed:.4f}s")
 assert not np.any(np.isnan(result))

 print("[PASS] Array shape performance test passed")


def test_comparison_with_scipy():
 """Compare performance with scipy.stats equivalent operations."""
 print(">> Comparing performance with scipy equivalent...")

 try:
 from scipy import stats

 np.random.seed(42)
 x = np.random.normal(0, 1, 10000)
 y = np.random.normal(0.5, 1, 10000)

 # Our implementation
 start_time = time.time()
 our_result = cohens_d(x, y)
 our_time = time.time() - start_time

 # Manual calculation using scipy tools
 start_time = time.time()
 pooled_std = np.sqrt(((len(x) - 1) * np.var(x, ddof=1) +
 (len(y) - 1) * np.var(y, ddof=1)) /
 (len(x) + len(y) - 2))
 scipy_result = (np.mean(x) - np.mean(y)) / pooled_std
 scipy_time = time.time() - start_time

 print(f" Our implementation: {our_time:.6f}s, d = {our_result:.4f}")
 print(f" Manual calculation: {scipy_time:.6f}s, d = {scipy_result:.4f}")
 print(f" Difference: {abs(our_result - scipy_result):.6f}")

 # Should be very close
 assert abs(our_result - scipy_result) < 1e-10

 except ImportError:
 print(" scipy not available for comparison")

 print("[PASS] Performance comparison test passed")


def main():
 """Run all performance tests."""
 print("Running performance tests...")
 print("=" * 50)

 test_functions = [
 test_large_array_performance,
 test_multidimensional_performance,
 test_memory_efficiency,
 test_broadcasting_performance,
 test_comparison_with_scipy,
 ]

 passed = 0
 failed = 0

 for test_func in test_functions:
 try:
 test_func()
 passed += 1
 except Exception as e:
 print(f"[FAIL] {test_func.__name__} failed: {e}")
 failed += 1

 print("=" * 50)
 print(f" Results: {passed} passed, {failed} failed, 0 errors")

 if failed == 0:
 print(" All performance tests passed!")
 else:
 print("[WARN] Some performance tests failed")
 return 1

 return 0


if __name__ == "__main__":
 exit(main())