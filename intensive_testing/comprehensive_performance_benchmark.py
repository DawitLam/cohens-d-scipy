#!/usr/bin/env python3
"""
Comprehensive performance benchmark suite for Cohen's d implementation.
Compares against manual implementations, Pingouin (if available), and provides detailed metrics.
"""

import time
import numpy as np
import sys
import os
import tracemalloc
import gc
from typing import Dict, List, Tuple, Optional, Callable

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'cohens_d_package'))

try:
    from cohens_d import cohens_d
except ImportError:
    sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
    from cohens_d_package.cohens_d import cohens_d


# Manual implementations for comparison
def manual_cohens_d_basic(x: np.ndarray, y: np.ndarray) -> float:
    """Basic manual implementation of Cohen's d."""
    mean_x = np.mean(x)
    mean_y = np.mean(y)
    pooled_std = np.sqrt(((len(x) - 1) * np.var(x, ddof=1) + 
                         (len(y) - 1) * np.var(y, ddof=1)) / 
                        (len(x) + len(y) - 2))
    return (mean_x - mean_y) / pooled_std


def manual_cohens_d_vectorized(x: np.ndarray, y: np.ndarray) -> float:
    """Vectorized manual implementation."""
    diff_means = np.mean(x) - np.mean(y)
    pooled_var = ((len(x) - 1) * np.var(x, ddof=1) + 
                  (len(y) - 1) * np.var(y, ddof=1)) / (len(x) + len(y) - 2)
    return diff_means / np.sqrt(pooled_var)


def try_import_pingouin():
    """Try to import pingouin for comparison."""
    try:
        import pingouin as pg
        return pg
    except ImportError:
        return None


class BenchmarkResult:
    """Store benchmark results."""
    
    def __init__(self, name: str, time_taken: float, memory_peak: float, 
                 result: float, error: Optional[str] = None):
        self.name = name
        self.time_taken = time_taken
        self.memory_peak = memory_peak
        self.result = result
        self.error = error


def benchmark_function(func: Callable, *args, **kwargs) -> BenchmarkResult:
    """Benchmark a function with time and memory tracking."""
    gc.collect()  # Clean up before measurement
    tracemalloc.start()
    
    start_time = time.perf_counter()
    try:
        result = func(*args, **kwargs)
        error = None
    except Exception as e:
        result = np.nan
        error = str(e)
    
    end_time = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    time_taken = end_time - start_time
    memory_peak = peak / 1024 / 1024  # Convert to MB
    
    return BenchmarkResult(func.__name__, time_taken, memory_peak, result, error)


class PerformanceBenchmarkSuite:
    """Comprehensive performance benchmark suite."""
    
    def __init__(self):
        self.results: Dict[str, List[BenchmarkResult]] = {}
        self.pingouin = try_import_pingouin()
        
    def add_result(self, test_name: str, result: BenchmarkResult):
        """Add a benchmark result."""
        if test_name not in self.results:
            self.results[test_name] = []
        self.results[test_name].append(result)
    
    def benchmark_basic_implementations(self, x: np.ndarray, y: np.ndarray, test_name: str):
        """Benchmark different basic implementations."""
        print(f"  📊 Benchmarking basic implementations for {test_name}...")
        
        # Our implementation
        result = benchmark_function(cohens_d, x, y)
        self.add_result(test_name, result)
        
        # Manual basic
        result = benchmark_function(manual_cohens_d_basic, x, y)
        result.name = "manual_basic"
        self.add_result(test_name, result)
        
        # Manual vectorized
        result = benchmark_function(manual_cohens_d_vectorized, x, y)
        result.name = "manual_vectorized"
        self.add_result(test_name, result)
        
        # Pingouin if available
        if self.pingouin:
            def pg_cohen_d(x, y):
                return self.pingouin.compute_effsize(x, y, eftype='cohen')
            
            result = benchmark_function(pg_cohen_d, x, y)
            result.name = "pingouin"
            self.add_result(test_name, result)
    
    def test_scalability(self):
        """Test performance across different array sizes."""
        print("🔍 Testing scalability across array sizes...")
        
        sizes = [100, 1000, 10000, 100000, 1000000]
        
        for size in sizes:
            test_name = f"size_{size:,}"
            print(f"    Testing size {size:,}...")
            
            np.random.seed(42)
            x = np.random.normal(0, 1, size)
            y = np.random.normal(0.5, 1, size)
            
            self.benchmark_basic_implementations(x, y, test_name)
    
    def test_multidimensional_performance(self):
        """Test performance with multidimensional arrays."""
        print("🔍 Testing multidimensional array performance...")
        
        shapes_and_axes = [
            ((1000, 10), 0, "1000x10_axis0"),
            ((1000, 10), 1, "1000x10_axis1"),
            ((100, 100), 0, "100x100_axis0"),
            ((100, 100), 1, "100x100_axis1"),
            ((50, 50, 4), 0, "50x50x4_axis0"),
            ((50, 50, 4), 2, "50x50x4_axis2"),
        ]
        
        for shape, axis, test_name in shapes_and_axes:
            print(f"    Testing shape {shape}, axis={axis}...")
            
            np.random.seed(42)
            x = np.random.normal(0, 1, shape)
            y = np.random.normal(0.3, 1, shape)
            
            # Only test our implementation for multidimensional
            result = benchmark_function(cohens_d, x, y, axis=axis)
            self.add_result(f"multidim_{test_name}", result)
    
    def test_parameter_combinations(self):
        """Test performance with different parameter combinations."""
        print("🔍 Testing parameter combination performance...")
        
        np.random.seed(42)
        x = np.random.normal(0, 1, 10000)
        y = np.random.normal(0.5, 1, 10000)
        
        param_combinations = [
            ({'bias_correction': False}, "no_bias_correction"),
            ({'bias_correction': True}, "with_bias_correction"),
            ({'pooled': False}, "unpooled"),
            ({'pooled': True}, "pooled"),
            ({'nan_policy': 'propagate'}, "nan_propagate"),
            ({'nan_policy': 'omit'}, "nan_omit"),
            ({'paired': True}, "paired"),
        ]
        
        for params, test_name in param_combinations:
            print(f"    Testing {test_name}...")
            
            if test_name == "paired":
                # Ensure arrays are same shape for paired test
                result = benchmark_function(cohens_d, x, y, **params)
            else:
                result = benchmark_function(cohens_d, x, y, **params)
            
            self.add_result(f"params_{test_name}", result)
    
    def test_nan_performance(self):
        """Test performance with NaN values."""
        print("🔍 Testing NaN handling performance...")
        
        np.random.seed(42)
        base_x = np.random.normal(0, 1, 10000)
        base_y = np.random.normal(0.5, 1, 10000)
        
        nan_scenarios = [
            (0, "no_nans"),
            (0.01, "1%_nans"),
            (0.05, "5%_nans"),
            (0.1, "10%_nans"),
            (0.2, "20%_nans"),
        ]
        
        for nan_fraction, test_name in nan_scenarios:
            print(f"    Testing {test_name}...")
            
            x = base_x.copy()
            y = base_y.copy()
            
            if nan_fraction > 0:
                # Add NaNs randomly
                n_nans = int(len(x) * nan_fraction)
                nan_indices_x = np.random.choice(len(x), n_nans, replace=False)
                nan_indices_y = np.random.choice(len(y), n_nans, replace=False)
                x[nan_indices_x] = np.nan
                y[nan_indices_y] = np.nan
            
            # Test different nan policies
            for policy in ['propagate', 'omit']:
                result = benchmark_function(cohens_d, x, y, nan_policy=policy)
                result.name = f"cohens_d_{policy}"
                self.add_result(f"nan_{test_name}_{policy}", result)
    
    def test_extreme_values(self):
        """Test performance with extreme values."""
        print("🔍 Testing extreme value performance...")
        
        extreme_scenarios = [
            (0, 1, "normal"),
            (0, 1000, "high_variance"),
            (1e6, 1, "large_mean"),
            (1e-6, 1e-6, "tiny_values"),
        ]
        
        for mean_scale, std_scale, test_name in extreme_scenarios:
            print(f"    Testing {test_name}...")
            
            np.random.seed(42)
            x = np.random.normal(0, std_scale, 10000) + mean_scale
            y = np.random.normal(0.5, std_scale, 10000) + mean_scale
            
            result = benchmark_function(cohens_d, x, y)
            self.add_result(f"extreme_{test_name}", result)
    
    def print_detailed_results(self):
        """Print comprehensive benchmark results."""
        print("\n" + "="*80)
        print("📈 COMPREHENSIVE PERFORMANCE BENCHMARK RESULTS")
        print("="*80)
        
        # Scalability results
        if any('size_' in key for key in self.results.keys()):
            print("\n🚀 SCALABILITY RESULTS:")
            print("-" * 60)
            print(f"{'Size':<15} {'Implementation':<15} {'Time (s)':<12} {'Memory (MB)':<12} {'Result':<10}")
            print("-" * 60)
            
            for test_name in sorted(self.results.keys()):
                if test_name.startswith('size_'):
                    size = test_name.replace('size_', '')
                    for result in self.results[test_name]:
                        print(f"{size:<15} {result.name:<15} {result.time_taken:<12.6f} {result.memory_peak:<12.2f} {result.result:<10.4f}")
        
        # Parameter combination results  
        if any('params_' in key for key in self.results.keys()):
            print("\n⚙️ PARAMETER COMBINATION RESULTS:")
            print("-" * 60)
            print(f"{'Parameter':<20} {'Time (s)':<12} {'Memory (MB)':<12} {'Result':<10}")
            print("-" * 60)
            
            for test_name in sorted(self.results.keys()):
                if test_name.startswith('params_'):
                    param = test_name.replace('params_', '')
                    result = self.results[test_name][0]
                    print(f"{param:<20} {result.time_taken:<12.6f} {result.memory_peak:<12.2f} {result.result:<10.4f}")
        
        # NaN handling results
        if any('nan_' in key for key in self.results.keys()):
            print("\n🚫 NaN HANDLING PERFORMANCE:")
            print("-" * 60)
            print(f"{'Scenario':<20} {'Policy':<10} {'Time (s)':<12} {'Memory (MB)':<12}")
            print("-" * 60)
            
            for test_name in sorted(self.results.keys()):
                if test_name.startswith('nan_'):
                    parts = test_name.replace('nan_', '').split('_')
                    scenario = '_'.join(parts[:-1])
                    policy = parts[-1]
                    result = self.results[test_name][0]
                    print(f"{scenario:<20} {policy:<10} {result.time_taken:<12.6f} {result.memory_peak:<12.2f}")
        
        # Multidimensional results
        if any('multidim_' in key for key in self.results.keys()):
            print("\n📐 MULTIDIMENSIONAL PERFORMANCE:")
            print("-" * 60)
            print(f"{'Shape & Axis':<20} {'Time (s)':<12} {'Memory (MB)':<12}")
            print("-" * 60)
            
            for test_name in sorted(self.results.keys()):
                if test_name.startswith('multidim_'):
                    shape_axis = test_name.replace('multidim_', '')
                    result = self.results[test_name][0]
                    print(f"{shape_axis:<20} {result.time_taken:<12.6f} {result.memory_peak:<12.2f}")
    
    def generate_performance_summary(self) -> dict:
        """Generate a summary of key performance metrics."""
        summary = {
            'fastest_time': float('inf'),
            'slowest_time': 0,
            'lowest_memory': float('inf'),
            'highest_memory': 0,
            'total_tests': 0,
            'successful_tests': 0,
            'failed_tests': 0
        }
        
        for test_results in self.results.values():
            for result in test_results:
                summary['total_tests'] += 1
                if result.error:
                    summary['failed_tests'] += 1
                else:
                    summary['successful_tests'] += 1
                    summary['fastest_time'] = min(summary['fastest_time'], result.time_taken)
                    summary['slowest_time'] = max(summary['slowest_time'], result.time_taken)
                    summary['lowest_memory'] = min(summary['lowest_memory'], result.memory_peak)
                    summary['highest_memory'] = max(summary['highest_memory'], result.memory_peak)
        
        return summary


def main():
    """Run comprehensive performance benchmarks."""
    print("🏃‍♂️ Running Comprehensive Performance Benchmark Suite")
    print("="*80)
    
    # Check for optional dependencies
    pingouin = try_import_pingouin()
    if pingouin:
        print("✅ Pingouin available for comparison")
    else:
        print("ℹ️  Pingouin not available (install with: pip install pingouin)")
    
    suite = PerformanceBenchmarkSuite()
    
    # Run all benchmark tests
    try:
        suite.test_scalability()
        suite.test_multidimensional_performance()
        suite.test_parameter_combinations()
        suite.test_nan_performance()
        suite.test_extreme_values()
        
        # Print detailed results
        suite.print_detailed_results()
        
        # Print summary
        summary = suite.generate_performance_summary()
        print(f"\n📊 PERFORMANCE SUMMARY:")
        print("-" * 40)
        print(f"Total tests: {summary['total_tests']}")
        print(f"Successful: {summary['successful_tests']}")
        print(f"Failed: {summary['failed_tests']}")
        print(f"Fastest time: {summary['fastest_time']:.6f}s")
        print(f"Slowest time: {summary['slowest_time']:.6f}s")
        print(f"Lowest memory: {summary['lowest_memory']:.2f}MB")
        print(f"Highest memory: {summary['highest_memory']:.2f}MB")
        
        print(f"\n🎉 Comprehensive performance benchmarks completed!")
        return 0
        
    except Exception as e:
        print(f"❌ Benchmark suite failed: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())