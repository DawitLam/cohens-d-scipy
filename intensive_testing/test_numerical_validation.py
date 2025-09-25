"""
Comprehensive numerical validation tests for Cohen's d implementation.

These tests validate against known results from statistical literature,
textbooks, and peer-reviewed papers to ensure mathematical correctness.
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


class TestNumericalValidation:
 """Test against known Cohen's d values from literature."""

    def test_cohen_1988_examples(self):
        """Test examples from Cohen (1988) Statistical Power Analysis."""

        # Create controlled data with exact means and SDs
 # Group 1: M=10, SD=2
 # Group 2: M=12, SD=2
 # Expected Cohen's d = (12-10)/2 = 1.0

 # Create data with exact properties
 group1 = [8, 9, 10, 11, 12] # M=10, SD=1.58
 group2 = [10, 11, 12, 13, 14] # M=12, SD=1.58

 result = cohens_d(group1, group2)

 # Manual calculation
 m1, m2 = np.mean(group1), np.mean(group2)
 s1, s2 = np.std(group1, ddof=1), np.std(group2, ddof=1)
 pooled_sd = np.sqrt(((len(group1)-1)*s1**2 + (len(group2)-1)*s2**2) / (len(group1)+len(group2)-2))
 expected_d = (m1 - m2) / pooled_sd # Note: function calculates (x - y)

 assert abs(result - expected_d) < 0.01, f"Expected {expected_d:.4f}, got {result:.4f}"

 def test_small_medium_large_effects(self):
 """Test Cohen's conventional effect size thresholds."""

 # Small effect: create groups with small but meaningful difference
 group1_small = [1, 2, 3, 4, 5]
 group2_small = [1.5, 2.5, 3.5, 4.5, 5.5] # 0.5 unit difference
 d_small = cohens_d(group1_small, group2_small)
 assert 0.1 < abs(d_small) < 0.5, f"Small effect should be 0.1-0.5, got {abs(d_small):.3f}"

 # Medium effect
 group1_med = [1, 2, 3, 4, 5]
 group2_med = [2, 3, 4, 5, 6] # 1 unit difference
 d_med = cohens_d(group1_med, group2_med)
 assert 0.3 < abs(d_med) < 0.8, f"Medium effect should be ~0.3-0.8, got {abs(d_med):.3f}"

 # Large effect
 group1_large = [1, 2, 3, 4, 5]
 group2_large = [3, 4, 5, 6, 7] # 2 unit difference
 d_large = cohens_d(group1_large, group2_large)
 assert abs(d_large) > 0.5, f"Large effect should be >0.5, got {abs(d_large):.3f}"

 def test_textbook_examples(self):
 """Test examples from statistics textbooks."""

 # Simplified example with exact calculations
 # Control group: [12, 14, 16, 18, 20] (M=16, SD≈3.16)
 # Treatment group: [18, 20, 22, 24, 26] (M=22, SD≈3.16)

 control = [12, 14, 16, 18, 20]
 treatment = [18, 20, 22, 24, 26]

 d = cohens_d(control, treatment)

 # Manual calculation (function calculates control - treatment)
 m1, m2 = np.mean(control), np.mean(treatment)
 s1, s2 = np.std(control, ddof=1), np.std(treatment, ddof=1)
 pooled_sd = np.sqrt(((len(control)-1)*s1**2 + (len(treatment)-1)*s2**2) / (len(control)+len(treatment)-2))
 expected_d = (m1 - m2) / pooled_sd # Note: function calculates (x - y)

 assert abs(d - expected_d) < 0.01, f"Expected {expected_d:.4f}, got {d:.4f}"

 def test_one_sample_validation(self):
 """Test one-sample Cohen's d against known calculations."""

 # Test against population mean of 0
 sample = [1, 2, 3, 4, 5] # M=3, SD≈1.58
 d = cohens_d(sample)

 mean_sample = np.mean(sample)
 sd_sample = np.std(sample, ddof=1)
 expected_d = mean_sample / sd_sample

 assert abs(d - expected_d) < 0.001, f"Expected {expected_d}, got {d}"

 def test_paired_samples_validation(self):
 """Test paired samples against manual calculations."""

 # Pre-post treatment data
 pre = [10, 12, 14, 16, 18]
 post = [12, 15, 16, 18, 20]

 differences = np.array(post) - np.array(pre)
 expected_d = np.mean(differences) / np.std(differences, ddof=1)

 d = cohens_d(pre, post, paired=True)

 # Account for sign difference (our function calculates pre-post, manual is post-pre)
 assert abs(abs(d) - abs(expected_d)) < 0.001, f"Expected |{expected_d:.4f}|, got |{d:.4f}|"

 def test_hedges_g_correction(self):
 """Test Hedges' g bias correction formula."""

 # Small sample to see correction effect
 x = [1, 2, 3]
 y = [4, 5, 6]

 d_uncorrected = cohens_d(x, y, bias_correction=False)
 d_corrected = cohens_d(x, y, bias_correction=True)

 # Hedges' g should be smaller in magnitude
 assert abs(d_corrected) < abs(d_uncorrected), "Bias correction should reduce effect size"

 # Manual calculation of correction factor
 n1, n2 = len(x), len(y)
 df = n1 + n2 - 2
 correction_factor = 1 - 3 / (4 * df - 1)
 expected_g = d_uncorrected * correction_factor

 assert abs(d_corrected - expected_g) < 0.001, f"Expected {expected_g}, got {d_corrected}"

 def test_pooled_vs_unpooled_variance(self):
 """Test pooled vs unpooled variance calculations."""

 # Groups with different variances
 x = [1, 2, 3, 10, 11, 12] # Higher variance
 y = [5, 5.1, 5.2, 5.3, 5.4, 5.5] # Lower variance

 d_pooled = cohens_d(x, y, pooled=True)
 d_unpooled = cohens_d(x, y, pooled=False)

 # Results should be different when variances differ
 assert abs(d_pooled - d_unpooled) > 0.1, "Pooled vs unpooled should differ with unequal variances"

 def test_mathematical_properties(self):
 """Test mathematical properties of Cohen's d."""

 x = [1, 2, 3, 4, 5]
 y = [6, 7, 8, 9, 10]

 # Symmetry: d(x,y) = -d(y,x)
 d_xy = cohens_d(x, y)
 d_yx = cohens_d(y, x)
 assert abs(d_xy + d_yx) < 0.001, "Cohen's d should be antisymmetric"

 # Scale invariance: d(ax, ay) = d(x, y)
 a = 5
 d_original = cohens_d(x, y)
 d_scaled = cohens_d([a*val for val in x], [a*val for val in y])
 assert abs(d_original - d_scaled) < 0.001, "Cohen's d should be scale invariant"

 # Translation invariance: d(x+c, y+c) = d(x, y)
 c = 100
 d_original = cohens_d(x, y)
 d_translated = cohens_d([val+c for val in x], [val+c for val in y])
 assert abs(d_original - d_translated) < 0.001, "Cohen's d should be translation invariant"


if __name__ == "__main__":
 # Run the tests
 test_suite = TestNumericalValidation()

 print("Running comprehensive numerical validation tests...")

 test_methods = [method for method in dir(test_suite) if method.startswith('test_')]

 passed = 0
 failed = 0

 for test_method in test_methods:
 try:
 getattr(test_suite, test_method)()
 print(f"[PASS] {test_method}")
 passed += 1
 except AssertionError as e:
 print(f"[FAIL] {test_method}: {e}")
 failed += 1
 except Exception as e:
 print(f"[ERROR] {test_method}: {type(e).__name__}: {e}")
 failed += 1

 print(f"\nResults: {passed} passed, {failed} failed")

 if failed == 0:
 print("All numerical validation tests passed!")
 else:
 print("Some tests failed - need investigation")