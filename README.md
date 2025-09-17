# Cohen's d Effect Size Implementation

A robust implementation of Cohen's d effect size calculation for inclusion in SciPy.

## Files

- `scipy/stats/_effect_size.py` - Main implementation
- `scipy/stats/tests/test_effect_size.py` - Test suite  
- `benchmarks/benchmarks/effect_size.py` - Performance benchmarks

## Features

- Two-sample and one-sample Cohen's d
- Pooled and unpooled standard deviation options
- Multidimensional array support
- Comprehensive NaN handling
- SciPy-compatible API

## Usage

```python
import numpy as np
from scipy.stats import cohens_d

# Two-sample Cohen's d
x = np.array([1, 2, 3, 4, 5])
y = np.array([2, 3, 4, 5, 6])
d = cohens_d(x, y)

# One-sample Cohen's d
d = cohens_d(x)
```

## Status

✅ Ready for SciPy integration  
✅ All tests passing  
✅ Performance optimized  
✅ API compliant  