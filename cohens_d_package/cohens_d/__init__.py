"""
Cohen's d Effect Size Calculator

A Python package for calculating Cohen's d effect size for one-sample and 
two-sample comparisons. Provides comprehensive options for handling missing data,
different axes, and pooled vs unpooled standard deviations.

This package provides a clean, NumPy-compatible interface for effect size
calculations commonly needed in statistical analysis and research.
"""

from .__version__ import __version__, __author__, __email__, __description__
from .core import cohens_d

__all__ = ['cohens_d', '__version__']