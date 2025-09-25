# Cohen's d Effect Size Implementation for SciPy

[![GitHub](https://img.shields.io/github/license/DawitLam/cohens-d-scipy)](https://github.com/DawitLam/cohens-d-scipy/blob/master/LICENSE)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)
[![NumPy](https://img.shields.io/badge/numpy-1.19%2B-orange)](https://numpy.org/)

A robust, production-ready implementation of Cohen's d effect size calculation designed for integration into SciPy's statistics module. This implementation fills a gap in SciPy's current offerings by providing comprehensive Cohen's d functionality with full support for paired samples, bias correction, and multidimensional arrays.

## Features

- **One-sample and two-sample Cohen's d**: Compare sample means against population means or between groups
- **Paired sample support**: Calculate Cohen's d for repeated measures using difference scores
- **Bias correction**: Hedges' g correction for small sample sizes
- **Multidimensional arrays**: Compute along specified axes with broadcasting support
- **NaN handling**: Configurable policies for missing data (propagate/omit/raise)
- **SciPy-compatible API**: Consistent parameter naming and behavior patterns

## Repository Structure

```
cohens_d_package/
├── cohens_d/
│ ├── __init__.py
│ ├── __version__.py
│ └── core.py # Main implementation
├── tests/
│ └── test_cohens_d.py # Comprehensive test suite
├── pyproject.toml # Package configuration
└── README.md # Package documentation
```

## Usage Examples

```python
import numpy as np
from cohens_d import cohens_d

# Two-sample Cohen's d (independent groups)
group1 = np.array([1.2, 2.1, 3.0, 4.2, 5.1])
group2 = np.array([2.3, 3.4, 4.1, 5.2, 6.0])
d = cohens_d(group1, group2)
print(f"Cohen's d: {d:.3f}")

# Paired samples Cohen's d
before = np.array([10, 12, 8, 15, 11])
after = np.array([12, 14, 9, 18, 13])
d_paired = cohens_d(before, after, paired=True)
print(f"Paired Cohen's d: {d_paired:.3f}")

# With bias correction (Hedges' g)
d_corrected = cohens_d(group1, group2, bias_correction=True)
print(f"Hedges' g: {d_corrected:.3f}")

# One-sample Cohen's d
sample = np.array([1.5, 2.2, 3.1, 4.0, 4.8])
d_one = cohens_d(sample) # Compare against zero
print(f"One-sample Cohen's d: {d_one:.3f}")

# Multidimensional arrays
data1 = np.random.randn(50, 3)
data2 = np.random.randn(60, 3)
d_multi = cohens_d(data1, data2, axis=0) # Cohen's d for each column
print(f"Effect sizes: {d_multi}")

# Handle missing data
x_nan = np.array([1, 2, np.nan, 4, 5])
y_nan = np.array([2, 3, 4, np.nan, 6])
d_omit = cohens_d(x_nan, y_nan, nan_policy='omit')
print(f"With NaN handling: {d_omit:.3f}")
```

## Installation

```bash
pip install cohens-d-effect-size
```

## Testing

Run the test suite:

```bash
cd cohens_d_package
python -m pytest tests/ -v
```

## API Reference

```python
cohens_d(x, y=None, *, paired=False, bias_correction=False, axis=None,
 nan_policy='propagate', ddof=1, keepdims=False,
 alternative='two-sided', pooled=True)
```

**Parameters:**
- `x, y`: array_like - Input samples
- `paired`: bool - Whether to calculate paired-samples Cohen's d
- `bias_correction`: bool - Apply Hedges' g small-sample correction
- `axis`: int or None - Axis along which to compute the statistic
- `nan_policy`: {'propagate', 'raise', 'omit'} - How to handle NaN values
- `ddof`: int - Delta degrees of freedom for standard deviation
- `keepdims`: bool - Whether to keep reduced dimensions
- `alternative`: {'two-sided', 'less', 'greater'} - Alternative hypothesis
- `pooled`: bool - Whether to use pooled standard deviation

**Returns:**
- Cohen's d effect size(s)

## Development Status

- **API Complete**: All planned features implemented
- **Tests Passing**: 32 comprehensive tests with edge case coverage
- **SciPy Compatible**: Follows scipy.stats conventions
- **Documentation**: Complete API documentation and examples

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Add tests for any new functionality
4. Ensure all tests pass (`python -m pytest`)
5. Submit a pull request

## License

This project is licensed under the BSD 3-Clause License - see the [LICENSE](LICENSE) file for details.