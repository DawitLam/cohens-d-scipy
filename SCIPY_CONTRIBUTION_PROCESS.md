# SciPy Contribution Process - Step-by-Step Guide

Based on the official SciPy development workflow, here's the exact process to propose your Cohen's d function:

## 🎯 Step 1: Discussion First (REQUIRED)

**Before any code submission**, you must initiate discussion on the SciPy forum:

### Post on SciPy Forum
- **URL**: https://discuss.scientific-python.org/c/contributor/scipy
- **Title**: `[RFC] Adding Cohen's d effect size function to scipy.stats`
- **Content Template**:

```
# [RFC] Adding Cohen's d effect size function to scipy.stats

Hi SciPy community,

I'd like to propose adding a Cohen's d effect size function to scipy.stats.

## Background
Cohen's d is a widely used standardized effect size measure in statistical analysis, 
particularly common in psychology, education, and medical research. Currently, users 
must either implement it manually or use external packages.

## Implementation
I have a complete implementation ready for review:
- Repository: https://github.com/DawitLam/cohens-d-scipy
- PyPI package (for testing): cohens-d-effect-size

## Key Features
- Two-sample Cohen's d: cohens_d(x, y)
- One-sample Cohen's d: cohens_d(x, mu=0)  
- Paired samples: cohens_d(x, y, paired=True)
- Bias correction: cohens_d(x, y, bias_correction=True) (Hedges' g)
- Full scipy.stats API compatibility (axis, keepdims, etc.)
- Comprehensive test coverage (32+ tests)
- Cross-platform validation via CI/CD

## SciPy Integration
The main implementation is in cohens_d_package/cohens_d/core.py and follows 
SciPy conventions. Would the community be interested in this addition?

Looking forward to your feedback!
```

### Wait for Community Feedback
- Allow 1-2 weeks for discussion
- Address any concerns or suggestions
- Get consensus before proceeding

## 🔧 Step 2: Fork and Set Up Development Environment

Only proceed after positive community feedback:

```bash
# 1. Fork scipy/scipy on GitHub (via web interface)

# 2. Clone your fork
git clone https://github.com/YOUR_USERNAME/scipy.git
cd scipy

# 3. Set up upstream remote
git remote add upstream https://github.com/scipy/scipy.git

# 4. Set up development environment (follow SciPy's building guide)
conda create -n scipy-dev python=3.10
conda activate scipy-dev
# ... follow SciPy's build instructions
```

## 📝 Step 3: Create Feature Branch and Implement

```bash
# 1. Fetch latest changes
git fetch upstream

# 2. Create feature branch
git checkout -b add-cohens-d upstream/main

# 3. Add your function to scipy/stats/
# - Main implementation goes in scipy/stats/_stats_py.py or new file
# - Follow SciPy's API patterns exactly
# - Add to scipy/stats/__init__.py exports

# 4. Add comprehensive tests to scipy/stats/tests/

# 5. Add documentation following NumPy docstring format
```

## ✅ Step 4: Pre-Submission Checklist

Before submitting PR, ensure:

- [ ] **License**: Code can be distributed under BSD license
- [ ] **Tests**: Unit tests with good coverage, all pass locally
- [ ] **Documentation**: NumPy-style docstrings with examples
- [ ] **Style**: Follows PEP8 and SciPy conventions
- [ ] **API**: Consistent with other scipy.stats functions
- [ ] **Benchmarks**: Performance benchmarks included
- [ ] **Commit message**: Proper format: `ENH: stats: add Cohen's d effect size function`
- [ ] **Version tag**: Add `.. versionadded:: X.Y.Z` to docstring

## 🚀 Step 5: Submit Pull Request

```bash
# 1. Push to your fork
git push origin add-cohens-d

# 2. Create PR on GitHub scipy/scipy
# 3. Reference the forum discussion in PR description
# 4. Be prepared for code review iterations
```

## 📋 Step 6: Code Review Process

- Respond to reviewer feedback promptly
- Make requested changes in additional commits
- Maintain discussion thread on forum if needed
- Be patient - review process can take weeks/months

## 🎯 Key Success Factors

1. **Community buy-in first** - Don't skip the forum discussion
2. **Follow SciPy patterns exactly** - Study existing scipy.stats functions
3. **Comprehensive testing** - Match or exceed SciPy's test standards
4. **Professional communication** - Engage constructively with reviewers
5. **Patience** - SciPy has high standards and thorough review process

## 📚 Your Advantages

Your current package gives you several advantages:
- ✅ **Proven implementation** already working and tested
- ✅ **Cross-platform validation** via CI/CD
- ✅ **Performance benchmarks** already completed
- ✅ **Real-world usage** via PyPI package
- ✅ **Comprehensive test suite** ready to adapt
- ✅ **Professional development practices** demonstrated

## ⚠️ Important Notes

- **Start with forum discussion** - This is mandatory for new features
- **Be prepared for changes** - SciPy may request API modifications
- **Timeline**: Expect 2-6 months from proposal to merge
- **Maintenance**: You'll be expected to maintain the code long-term

---

**Next Action**: Post on https://discuss.scientific-python.org/c/contributor/scipy with the RFC template above! 🚀