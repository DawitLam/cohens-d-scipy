"""
Benchmarks for Cohen's d effect size calculation.

This module provides performance benchmarks for the cohens_d function
to monitor performance regressions and compare against alternative
implementations.
"""

import numpy as np
from scipy.stats import cohens_d
import time
from collections import defaultdict

class Benchmark:
    """Benchmark suite for Cohen's d function."""
    def __init__(self):
        """Initialize benchmark suite."""
        self.sizes = [100, 1000, 10000, 100000]
        self.n_repeats = 10
        self.results = defaultdict(list)

    def setup_data(self, size, seed=42):
        np.random.seed(seed)
        x = np.random.normal(0, 1, size)
        y = np.random.normal(0.2, 1, size)
        return x, y

    def time_function(self, func, *args, **kwargs):
        times = []
        for _ in range(self.n_repeats):
            start = time.perf_counter()
            result = func(*args, **kwargs)
            end = time.perf_counter()
            times.append(end - start)
        return np.mean(times), np.std(times), result

    def bench_basic_two_sample(self):
        print("Benchmarking basic two-sample Cohen's d:")
        print("-" * 50)
        for size in self.sizes:
            x, y = self.setup_data(size)
            mean_time, std_time, _ = self.time_function(cohens_d, x, y)
            self.results['basic_two_sample'].append({
                'size': size,
                'mean_time': mean_time,
                'std_time': std_time
            })
            print(f"Size {size:6d}: {mean_time:.4f}  {std_time:.4f} seconds")

    def bench_one_sample(self):
        print("\nBenchmarking one-sample Cohen's d:")
        print("-" * 40)
        for size in self.sizes:
            x, _ = self.setup_data(size)
            mean_time, std_time, _ = self.time_function(cohens_d, x)
            self.results['one_sample'].append({
                'size': size,
                'mean_time': mean_time,
                'std_time': std_time
            })
            print(f"Size {size:6d}: {mean_time:.4f}  {std_time:.4f} seconds")

    def bench_nan_handling(self):
        print("\nBenchmarking NaN handling:")
        print("-" * 35)
        for size in self.sizes:
            x, y = self.setup_data(size)
            x[::100] = np.nan
            y[::150] = np.nan
            for policy in ['propagate', 'omit']:
                mean_time, std_time, _ = self.time_function(cohens_d, x, y, nan_policy=policy)
                self.results[f'nan_{policy}'].append({
                    'size': size,
                    'mean_time': mean_time,
                    'std_time': std_time
                })
                print(f"Size {size:6d}, {policy:9s}: "
                      f"{mean_time:.4f}  {std_time:.4f} seconds")

    def bench_multidimensional(self):
        print("\nBenchmarking multidimensional arrays:")
        print("-" * 45)
        shapes = [(100, 100), (1000, 10), (10, 1000), (100, 10, 10)]
        for shape in shapes:
            np.random.seed(42)
            x = np.random.normal(0, 1, shape)
            y = np.random.normal(0.2, 1, shape)
            for axis in [0, 1, None]:
                if axis is not None and axis >= len(shape):
                    continue
                mean_time, std_time, _ = self.time_function(cohens_d, x, y, axis=axis)
                axis_str = str(axis) if axis is not None else 'None'
                print(f"Shape {str(shape):15s}, axis={axis_str:4s}: "
                      f"{mean_time:.4f}  {std_time:.4f} seconds")

    def bench_pooled_vs_unpooled(self):
        print("\nBenchmarking pooled vs unpooled:")
        print("-" * 40)
        for size in self.sizes:
            x, y = self.setup_data(size)
            mean_time_pool, std_time_pool, _ = self.time_function(cohens_d, x, y, pooled=True)
            mean_time_unpool, std_time_unpool, _ = self.time_function(cohens_d, x, y, pooled=False)
            print(f"Size {size:6d}:")
            print(f"  Pooled  : {mean_time_pool:.4f}  {std_time_pool:.4f} s")
            print(f"  Unpooled: {mean_time_unpool:.4f}  {std_time_unpool:.4f} s")

    def bench_alternative_implementations(self):
        print("\nBenchmarking vs alternative implementations:")
        print("-" * 55)
        def manual_cohens_d(x, y):
            mean_x, mean_y = np.mean(x), np.mean(y)
            var_x, var_y = np.var(x, ddof=1), np.var(y, ddof=1)
            n_x, n_y = len(x), len(y)
            pooled_var = ((n_x - 1) * var_x + (n_y - 1) * var_y) / (n_x + n_y - 2)
            return (mean_x - mean_y) / np.sqrt(pooled_var)
        def vectorized_cohens_d(x, y):
            diff = x.mean() - y.mean()
            n1, n2 = len(x), len(y)
            pooled_std = np.sqrt(((n1 - 1) * x.var(ddof=1) + (n2 - 1) * y.var(ddof=1)) / (n1 + n2 - 2))
            return diff / pooled_std
        for size in [1000, 10000]:
            x, y = self.setup_data(size)
            implementations = [
                ("SciPy cohens_d", lambda: cohens_d(x, y)),
                ("Manual impl", lambda: manual_cohens_d(x, y)),
                ("Vectorized impl", lambda: vectorized_cohens_d(x, y))
            ]
            print(f"\nSize {size}:")
            for name, func in implementations:
                mean_time, std_time, _ = self.time_function(func)
                print(f"  {name:15s}: {mean_time:.4f}  {std_time:.4f} s")

    def memory_benchmark(self):
        print("\nMemory usage benchmark:")
        print("-" * 30)
        import psutil
        import os
        def get_memory_usage():
            process = psutil.Process(os.getpid())
            return process.memory_info().rss / 1024 / 1024
        for size in [10000, 100000, 1000000]:
            baseline_memory = get_memory_usage()
            x, y = self.setup_data(size)
            after_creation = get_memory_usage()
            result = cohens_d(x, y)
            after_calculation = get_memory_usage()
            del x, y, result
            memory_for_arrays = after_creation - baseline_memory
            memory_for_calc = after_calculation - after_creation
            print(f"Size {size:7d}: Arrays: {memory_for_arrays:.1f} MB, Calculation: {memory_for_calc:.1f} MB")

    def run_all_benchmarks(self):
        print("Cohen's d Performance Benchmarks")
        print("=" * 50)
        self.bench_basic_two_sample()
        self.bench_one_sample()
        self.bench_nan_handling()
        self.bench_multidimensional()
        self.bench_pooled_vs_unpooled()
        self.bench_alternative_implementations()
        try:
            self.memory_benchmark()
        except ImportError:
            print("\nSkipping memory benchmark (psutil not available)")
        print("\n" + "=" * 50)
        print("Benchmark completed!")

    def save_results(self, filename="cohens_d_benchmark_results.json"):
        import json
        serializable_results = {}
        for key, value in self.results.items():
            serializable_results[key] = []
            for item in value:
                serializable_item = {}
                for k, v in item.items():
                    if isinstance(v, np.floating):
                        serializable_item[k] = float(v)
                    elif isinstance(v, np.integer):
                        serializable_item[k] = int(v)
                    else:
                        serializable_item[k] = v
                serializable_results[key].append(serializable_item)
        with open(filename, 'w') as f:
            json.dump(serializable_results, f, indent=2)
        print(f"Results saved to {filename}")

def main():
    benchmark = Benchmark()
    benchmark.run_all_benchmarks()
    benchmark.save_results()

if __name__ == "__main__":
    main()
