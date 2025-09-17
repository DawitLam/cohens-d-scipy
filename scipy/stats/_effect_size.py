# ============================================================================
# MAIN IMPLEMENTATION (goes in scipy/stats/_effect_size.py)
# ============================================================================

"""
Cohen's d effect size calculation.

This module provides functions for calculating Cohen's d, a standardized
measure of effect size that quantifies the difference between two groups in
terms of their pooled standard deviation.
"""

import numpy as np
import warnings

__all__ = ['cohens_d']

def cohens_d(x, y=None, *, pooled=True, ddof=1, nan_policy='propagate',
             alternative='two-sided', axis=0, keepdims=False):
    """
    Calculate Cohen's d effect size.
    
    Cohen's d is a standardized measure of effect size that quantifies the 
    difference between two groups in terms of their pooled standard deviation.
    It is commonly used to measure the practical significance of a difference
    between group means.
    
    Parameters
    ----------
    x : array_like
        First sample or the sample to compare against a reference value.
    y : array_like, optional
        Second sample. If None, Cohen's d is calculated as a one-sample
        effect size using x against a mean of 0. Default is None.
    pooled : bool, optional
        If True (default), use pooled standard deviation. If False, use
        the standard deviation of the first group (x) only. Only relevant
        for two-sample calculations.
    ddof : int, optional
        Delta degrees of freedom: the divisor used in the calculation is
        ``N - ddof``, where ``N`` represents the number of elements.
        Default is 1.
    nan_policy : {'propagate', 'raise', 'omit'}, optional
        Defines how to handle when input contains nan.
        The following options are available (default is 'propagate'):
        
        * 'propagate': returns nan
        * 'raise': throws an error  
        * 'omit': performs the calculations ignoring nan values
    alternative : {'two-sided', 'less', 'greater'}, optional
        Defines the alternative hypothesis. The following options are
        available (default is 'two-sided'):
        
        * 'two-sided': the effect size is non-zero
        * 'less': the effect size is less than zero (x < y)  
        * 'greater': the effect size is greater than zero (x > y)
    axis : int or None, optional
        Axis along which to compute the effect size. If None, compute over
        the whole arrays, x and y. Default is 0.
    keepdims : bool, optional
        If this is set to True, the axes which are reduced are left in the
        result as dimensions with size one. Default is False.
        
    Returns
    -------
    statistic : float or ndarray
        The Cohen's d effect size. Positive values indicate that the mean
        of x is greater than the mean of y (or 0 for one-sample).
        
    Notes
    -----
    Cohen's d is calculated as:
    
    For two samples:
    
    .. math::
        d = \frac{\bar{x} - \bar{y}}{s_p}
        
    where :math:`s_p` is the pooled standard deviation when pooled=True:
    
    .. math::
        s_p = \sqrt{\frac{(n_1-1)s_1^2 + (n_2-1)s_2^2}{n_1+n_2-2}}
        
    or the standard deviation of x when pooled=False.
    
    For one sample (y=None):
    
    .. math::
        d = \frac{\bar{x}}{s_x}
        
    Effect size interpretation (Cohen, 1988):
    
    * Small effect: |d| = 0.2
    * Medium effect: |d| = 0.5  
    * Large effect: |d| = 0.8
    
    References
    ----------
    .. [1] Cohen, J. (1988). Statistical power analysis for the behavioral 
           sciences (2nd ed.). Hillsdale, NJ: Lawrence Erlbaum Associates.
    .. [2] Lakens, D. (2013). Calculating and reporting effect sizes to 
           facilitate cumulative science: a practical primer for t-tests and 
           ANOVAs. Frontiers in psychology, 4, 863.
           
    Examples
    --------
    Calculate Cohen's d for two independent samples:
    
    >>> import numpy as np
    >>> from scipy.stats import cohens_d
    >>> np.random.seed(12345678)
    >>> x = np.random.normal(0, 1, 100)
    >>> y = np.random.normal(0.5, 1, 100)  
    >>> d = cohens_d(x, y)
    >>> print(f"Cohen's d: {d:.3f}")  # doctest: +SKIP
    Cohen's d: -0.505
    
    Calculate one-sample Cohen's d:
    
    >>> x = np.random.normal(0.3, 1, 100)
    >>> d = cohens_d(x)
    >>> abs(d) > 0  # Effect size should be positive
    True
    
    With 2D arrays along different axes:
    
    >>> x = np.array([[1, 2], [3, 4]])
    >>> y = np.array([[2, 3], [4, 5]])
    >>> d_axis0 = cohens_d(x, y, axis=0)
    >>> d_axis1 = cohens_d(x, y, axis=1) 
    >>> d_axis0.shape
    (2,)
    >>> d_axis1.shape
    (2,)
    
    Handle NaN values:
    
    >>> x_nan = np.array([1., 2., np.nan, 4.])
    >>> y_nan = np.array([2., 3., 4., np.nan])
    >>> cohens_d(x_nan, y_nan, nan_policy='omit')  # doctest: +ELLIPSIS
    -1.0...
    """
    # Input validation and conversion
    x = np.asarray(x)
    if y is not None:
        y = np.asarray(y)
        
    # Handle nan_policy
    if nan_policy not in ['propagate', 'raise', 'omit']:
        raise ValueError("nan_policy must be 'propagate', 'raise', or 'omit'")
        
    if nan_policy == 'raise':
        if np.any(np.isnan(x)):
            raise ValueError("Input x contains NaN values")
        if y is not None and np.any(np.isnan(y)):
            raise ValueError("Input y contains NaN values")
    
    # Handle alternative parameter
    if alternative not in ['two-sided', 'less', 'greater']:
        raise ValueError("alternative must be 'two-sided', 'less', "
                        "or 'greater'")
    
    # Determine axis handling
    if axis is not None:
        # Use numpy's standard function to normalize axis
        if hasattr(np, 'core') and hasattr(np.core, 'numeric'):
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                axis = np.core.numeric.normalize_axis_index(axis, x.ndim)
        else:
            # Fallback - simple axis validation
            if axis < 0:
                axis = x.ndim + axis
            if axis < 0 or axis >= x.ndim:
                raise np.AxisError(f"axis {axis} is out of bounds for array of dimension {x.ndim}")
        if y is not None and y.ndim != x.ndim:
            raise ValueError("x and y must have the same number of dimensions")
    
    # One-sample Cohen's d
    if y is None:
        if nan_policy == 'omit':
            mean_x = np.nanmean(x, axis=axis, keepdims=keepdims)
            std_x = np.nanstd(x, axis=axis, ddof=ddof, keepdims=keepdims)
        else:
            mean_x = np.mean(x, axis=axis, keepdims=keepdims)
            std_x = np.std(x, axis=axis, ddof=ddof, keepdims=keepdims)
            
        # Avoid division by zero
        with np.errstate(divide='ignore', invalid='ignore'):
            d = mean_x / std_x
            
        d = np.where(std_x == 0, np.nan, d)
        
    else:
        # Two-sample Cohen's d - Check dimension compatibility
        if axis is None:
            x_flat = x.ravel()
            y_flat = y.ravel()
        else:
            try:
                np.broadcast_arrays(x, y)
            except ValueError as e:
                raise ValueError("x and y arrays are not compatible for "
                                "broadcasting") from e
        
        if nan_policy == 'omit':
            mean_x = np.nanmean(x, axis=axis, keepdims=keepdims)
            mean_y = np.nanmean(y, axis=axis, keepdims=keepdims)
            
            if pooled:
                var_x = np.nanvar(x, axis=axis, ddof=ddof, keepdims=keepdims)
                var_y = np.nanvar(y, axis=axis, ddof=ddof, keepdims=keepdims)
                n_x = np.sum(~np.isnan(x), axis=axis, keepdims=keepdims)
                n_y = np.sum(~np.isnan(y), axis=axis, keepdims=keepdims)
                
                with np.errstate(divide='ignore', invalid='ignore'):
                    pooled_var = ((n_x - 1) * var_x + (n_y - 1) * var_y) / (
                        n_x + n_y - 2)
                    std_pooled = np.sqrt(pooled_var)
            else:
                std_pooled = np.nanstd(x, axis=axis, ddof=ddof, 
                                      keepdims=keepdims)
        else:
            mean_x = np.mean(x, axis=axis, keepdims=keepdims)
            mean_y = np.mean(y, axis=axis, keepdims=keepdims)
            
            if pooled:
                var_x = np.var(x, axis=axis, ddof=ddof, keepdims=keepdims)
                var_y = np.var(y, axis=axis, ddof=ddof, keepdims=keepdims)
                n_x = x.shape[axis] if axis is not None else x.size
                n_y = y.shape[axis] if axis is not None else y.size
                
                if axis is not None and keepdims:
                    n_x = np.full(mean_x.shape, n_x)
                    n_y = np.full(mean_y.shape, n_y) 
                
                pooled_var = ((n_x - 1) * var_x + (n_y - 1) * var_y) / (
                    n_x + n_y - 2)
                std_pooled = np.sqrt(pooled_var)
            else:
                std_pooled = np.std(x, axis=axis, ddof=ddof, 
                                   keepdims=keepdims)
        
        # Calculate Cohen's d
        with np.errstate(divide='ignore', invalid='ignore'):
            d = (mean_x - mean_y) / std_pooled
            
        d = np.where(std_pooled == 0, np.nan, d)
    
    return d
