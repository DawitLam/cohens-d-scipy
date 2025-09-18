# PyPI Upload Guide for cohens-d-effect-size Package

## 🎉 SUCCESS! Package Published to PyPI!

Your Cohen's d package has been successfully uploaded to PyPI and is now available worldwide!

**Package URL**: https://pypi.org/project/cohens-d-effect-size/  
**Installation**: `pip install cohens-d-effect-size`

## Built Files
- `dist/cohens_d_effect_size-0.1.0-py3-none-any.whl` - Wheel distribution
- `dist/cohens_d_effect_size-0.1.0.tar.gz` - Source distribution

## PyPI Upload Steps

### 1. Create PyPI Account
1. Go to https://pypi.org/account/register/
2. Create your account with your email: dawit.lambebo@gmail.com
3. Verify your email address

### 2. Create API Token (Recommended)
1. Go to https://pypi.org/manage/account/
2. Scroll to "API tokens" section
3. Click "Add API token"
4. Give it a name like "cohens-d-package"
5. Choose scope: "Entire account" (for first upload)
6. Save the token securely - you'll only see it once!

### 3. Upload to TestPyPI First (Recommended)

**First, you also need a TestPyPI account and token:**
1. Register at: https://test.pypi.org/account/register/
2. Get API token at: https://test.pypi.org/manage/account/

**Then upload to TestPyPI:**
```bash
# Upload to TestPyPI first to test
python -m twine upload --repository testpypi dist/*
```

### 4. Upload to Production PyPI
```bash
# Upload to real PyPI
twine upload dist/*
```

When prompted:
- Username: `__token__`
- Password: Your API token (including the `pypi-` prefix)

## Alternative: Upload with Username/Password
If you prefer not to use API tokens:
```bash
twine upload dist/* --username dawit.lambebo@gmail.com
```

## Installation Test ✅ COMPLETED
Your package is now live! Anyone can install it with:
```bash
pip install cohens-d-effect-size
```

## Usage Example for Users
```python
import numpy as np
from cohens_d import cohens_d

# Two-sample Cohen's d
control = np.array([1, 2, 3, 4, 5])
treatment = np.array([3, 4, 5, 6, 7])
effect_size = cohens_d(control, treatment)
print(f"Cohen's d: {effect_size:.3f}")

# One-sample Cohen's d
sample = np.array([0.5, 1.0, 1.5, 2.0])
effect_size = cohens_d(sample)
print(f"One-sample Cohen's d: {effect_size:.3f}")
```

## Package Information
- **Name**: cohens-d-effect-size ✅
- **Version**: 0.1.0 ✅
- **Author**: Dawit L. Gulta
- **Email**: dawit.lambebo@gmail.com
- **License**: BSD 3-Clause
- **Python**: >=3.8
- **Dependencies**: numpy>=1.19.0
- **PyPI URL**: https://pypi.org/project/cohens-d-effect-size/

## Features
✅ One-sample and two-sample Cohen's d  
✅ Multi-dimensional array support  
✅ Missing data handling (NaN policies)  
✅ Pooled vs unpooled variance options  
✅ Full NumPy compatibility  
✅ Comprehensive test suite (23 tests)  
✅ Modern packaging standards  

## PyPI Page URL ✅ LIVE
Your package is available at:
https://pypi.org/project/cohens-d-effect-size/

## Troubleshooting
- If package name is taken, consider: `cohens-d-stats`, `cohens-d-effect-size`, etc.
- Make sure your PyPI account is verified
- Check that your API token has the right permissions
- For 2FA accounts, you must use API tokens

## Next Steps After PyPI Upload
1. Update GitHub repository with PyPI badge
2. Create GitHub release matching the version
3. Consider submitting to SciPy for integration
4. Share with the scientific Python community

## Maintenance
To upload future versions:
1. Update version in `cohens_d/__version__.py`
2. Run tests: `pytest tests/`
3. Build: `python -m build`
4. Upload: `twine upload dist/*`