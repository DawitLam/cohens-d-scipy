# Cohen's d Effect Size Calculator

[![PyPI version](https://badge.fury.io/py/cohens-d-effect-size.svg)](https://badge.fury.io/py/cohens-d-effect-size)
[![Python versions](https://img.shields.io/pypi/pyversions/cohens-d-effect-size.svg)](https://pypi.org/project/cohens-d-effect-size/)
[![License: BSD-3-Clause](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)
[![Tests](https://github.com/DawitLam/cohens-d-scipy/workflows/Tests/badge.svg)](https://github.com/DawitLam/cohens-d-scipy/actions)

A Python package for calculating Cohen's d effect size with comprehensive options for handling missing data, different axes, and pooled vs unpooled standard deviations.

## Features

- **One-sample and two-sample Cohen's d**: Calculate effect sizes for single samples against zero or between two independent groups
- **Flexible data handling**: Support for 1D and multi-dimensional arrays with axis specification
- **Missing data policies**: Choose how to handle NaN values (propagate, raise, or omit)
- **Pooled and unpooled variance**: Option to use pooled standard deviation or first sample's standard deviation
- **NumPy compatibility**: Full integration with NumPy arrays and broadcasting rules
- **Comprehensive testing**: Extensive test suite ensuring numerical accuracy and edge case handling

## Installation

Install from PyPI:

```bash
pip install cohens-d-effect-size
```

Install from source:

```bash
git clone https://github.com/DawitLam/cohens-d-scipy.git
cd cohens-d
pip install -e .
```

## Quick Start

```python
import numpy as np
from cohens_d import cohens_d

# Two-sample Cohen's d
group1 = np.array([1, 2, 3, 4, 5])
group2 = np.array([2, 3, 4, 5, 6])
effect_size = cohens_d(group1, group2)
print(f"Cohen's d: {effect_size:.3f}")

# One-sample Cohen's d (against zero)
sample = np.array([0.5, 1.0, 1.5, 2.0, 2.5])
effect_size = cohens_d(sample)
print(f"One-sample Cohen's d: {effect_size:.3f}")
```

## Parameters

- `x`: First sample or the sample to compare against zero
- `y`: Second sample (optional). If not provided, calculates one-sample Cohen's d
- `axis`: Axis along which to compute the effect size (default: None)
- `nan_policy`: How to handle NaN values ('propagate', 'raise', 'omit')
- `ddof`: Delta degrees of freedom for standard deviation calculation (default: 1)
- `keepdims`: Whether to keep reduced dimensions as size 1 (default: False)
- `alternative`: Alternative hypothesis ('two-sided', 'less', 'greater')
- `pooled`: Whether to use pooled standard deviation for two-sample case (default: True)

## Examples

### Basic Usage

```python
import numpy as np
from cohens_d import cohens_d

# Create sample data
np.random.seed(42)
control = np.random.normal(0, 1, 100)
treatment = np.random.normal(0.5, 1, 100)

# Calculate Cohen's d
d = cohens_d(control, treatment)
print(f"Effect size: {d:.3f}")
```

### Multi-dimensional Arrays

```python
# 2D arrays - calculate along different axes
data_2d = np.random.normal(0, 1, (10, 5))
treatment_2d = np.random.normal(0.3, 1, (10, 5))

# Along rows (axis=0)
d_rows = cohens_d(data_2d, treatment_2d, axis=0)
print(f"Effect sizes along axis 0: {d_rows}")

# Along columns (axis=1)  
d_cols = cohens_d(data_2d, treatment_2d, axis=1)
print(f"Effect sizes along axis 1: {d_cols}")
```

### Handling Missing Data

```python
# Data with missing values
data_with_nan = np.array([1, 2, np.nan, 4, 5])
control_with_nan = np.array([2, 3, 4, np.nan, 6])

# Omit missing values
d_omit = cohens_d(data_with_nan, control_with_nan, nan_policy='omit')
print(f"Effect size (omit NaN): {d_omit:.3f}")

# Raise error on missing values
try:
    d_raise = cohens_d(data_with_nan, control_with_nan, nan_policy='raise')
except ValueError as e:
    print(f"Error: {e}")
```

### Pooled vs Unpooled Standard Deviation

```python
# Using pooled standard deviation (default)
d_pooled = cohens_d(group1, group2, pooled=True)

# Using first sample's standard deviation only
d_unpooled = cohens_d(group1, group2, pooled=False)

print(f"Pooled: {d_pooled:.3f}, Unpooled: {d_unpooled:.3f}")
```

## Interpretation

Cohen's d effect size interpretation:

- **Small effect**: d ≈ 0.2
- **Medium effect**: d ≈ 0.5  
- **Large effect**: d ≈ 0.8

```python
def interpret_cohens_d(d):
    \"\"\"Interpret Cohen's d effect size.\"\"\"
    abs_d = abs(d)
    if abs_d < 0.2:
        return "negligible"
    elif abs_d < 0.5:
        return "small"
    elif abs_d < 0.8:
        return "medium"
    else:
        return "large"

d = cohens_d(control, treatment)
interpretation = interpret_cohens_d(d)
print(f"Effect size: {d:.3f} ({interpretation})")
```

## Requirements

- Python ≥ 3.8
- NumPy ≥ 1.19.0

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Development Setup

```bash
git clone https://github.com/DawitLam/cohens-d.git
cd cohens-d
pip install -e ".[dev]"
```

### Running Tests

```bash
pytest tests/
```

### Code Formatting

```bash
black cohens_d/ tests/
flake8 cohens_d/ tests/
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## References

1. Cohen, J. (1988). Statistical power analysis for the behavioral sciences (2nd ed.). Hillsdale, NJ: Lawrence Erlbaum Associates.
2. Lakens, D. (2013). Calculating and reporting effect sizes to facilitate cumulative science: a practical primer for t-tests and ANOVAs. Frontiers in Psychology, 4, 863.

## Changelog

### 0.1.0 (2024-01-XX)
- Initial release
- Support for one-sample and two-sample Cohen's d
- Comprehensive parameter options
- Full NumPy compatibility
- Extensive test coverage