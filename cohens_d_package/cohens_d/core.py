"""
Core Cohen's d implementation for effect size calculation.

This module provides functions for calculating Cohen's d effect size
for both one-sample and two-sample comparisons.
"""

import numpy as np
import warnings


def cohens_d(x, y=None, *, paired=False, bias_correction=False, axis=None, 
             nan_policy='propagate', ddof=1, keepdims=False, 
             alternative='two-sided', pooled=True):
    """
    Calculate Cohen's d effect size.
    
    Cohen's d is a standardized measure of effect size that quantifies 
    the difference between two groups or between a sample and a population. 
    For two independent samples, it represents the difference between group 
    means in terms of the pooled standard deviation.
    
    Parameters
    ----------
    x : array_like
        First sample or the sample to compare against zero (one-sample case).
    y : array_like, optional
        Second sample. If not provided, calculates one-sample Cohen's d 
        comparing `x` against zero.
    paired : bool, optional
        If True, calculate paired-samples Cohen's d using the standard 
        deviation of the differences (d-average formula). Only valid 
        when both x and y are provided. Default is False.
    bias_correction : bool, optional
        If True, apply Hedges' g small-sample bias correction factor.
        Default is False.
    axis : int or None, optional
        Axis along which to compute the effect size. If None, compute over 
        the flattened array. Default is None.
    nan_policy : {'propagate', 'raise', 'omit'}, optional
        Defines how to handle when input arrays contain nan.
        - 'propagate': returns nan
        - 'raise': throws an error  
        - 'omit': performs calculations ignoring nan values
        For paired samples, NaN handling is applied row-wise.
        Default is 'propagate'.
    ddof : int, optional
        Delta degrees of freedom used in the calculation of the standard
        deviation. Default is 1.
    keepdims : bool, optional
        If this is set to True, the axes which are reduced are left in the
        result as dimensions with size one. Default is False.
    alternative : {'two-sided', 'less', 'greater'}, optional
        Defines the alternative hypothesis. Currently only affects 
        documentation and validation. Default is 'two-sided'.
    pooled : bool, optional
        If True (default), use pooled standard deviation for two-sample 
        case. If False, use the standard deviation of the first sample.
        Ignored when paired=True.
        
    Returns
    -------
    d : float or ndarray
        Cohen's d effect size. If bias_correction=True, returns Hedges' g 
        instead. For paired samples, uses the d-average formula with the 
        standard deviation of differences.
        
    Notes
    -----
    Cohen's d is calculated as:
    
    - One-sample: d = mean(x) / std(x)
    - Two-sample independent: d = (mean(x) - mean(y)) / pooled_std
    - Two-sample paired: d = mean(x - y) / std(x - y)
    
    Where pooled_std for independent samples is:
    pooled_std = sqrt(((n1-1)*var1 + (n2-1)*var2) / (n1+n2-2))
    
    Hedges' g applies a small-sample bias correction:
    g = d * (1 - 3/(4*df - 1))
    where df = n - 1 for one-sample or n1 + n2 - 2 for two-sample independent,
    or n - 1 for paired samples.
    
    Interpretation guidelines for Cohen's d:
    - Small effect: d ≈ 0.2
    - Medium effect: d ≈ 0.5  
    - Large effect: d ≈ 0.8
    
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
    >>> from cohens_d import cohens_d
    >>> np.random.seed(12345678)
    >>> x = np.random.normal(0, 1, 100)
    >>> y = np.random.normal(0.5, 1, 100)  
    >>> d = cohens_d(x, y)
    >>> abs(d) > 0.4  # Should show moderate effect size
    True
    
    Calculate one-sample Cohen's d:
    
    >>> x = np.random.normal(0.3, 1, 100)
    >>> d = cohens_d(x)
    >>> abs(d) > 0  # Effect size should be positive
    True
    
    Calculate paired-samples Cohen's d:
    
    >>> pre = np.array([10, 12, 14, 16, 18])
    >>> post = np.array([12, 15, 16, 18, 20])
    >>> d_paired = cohens_d(pre, post, paired=True)
    >>> d_paired < 0  # Post > Pre, so negative effect
    True
    
    Apply Hedges' g bias correction:
    
    >>> x_small = np.array([1, 2, 3, 4, 5])
    >>> y_small = np.array([3, 4, 5, 6, 7])
    >>> d_raw = cohens_d(x_small, y_small, bias_correction=False)
    >>> g_corrected = cohens_d(x_small, y_small, bias_correction=True)
    >>> abs(g_corrected) < abs(d_raw)  # Bias correction reduces magnitude
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
    # Convert inputs to numpy arrays
    x = np.asarray(x)
    if y is not None:
        y = np.asarray(y)
        
    # Validate paired parameter
    if paired and y is None:
        raise ValueError("paired=True requires both x and y to be provided")
        
    # Validate nan_policy parameter
    if nan_policy not in ['propagate', 'raise', 'omit']:
        raise ValueError("nan_policy must be 'propagate', 'raise', or 'omit'")
        
    if nan_policy == 'raise':
        if np.any(np.isnan(x)):
            raise ValueError("Input x contains NaN values")
        if y is not None and np.any(np.isnan(y)):
            raise ValueError("Input y contains NaN values")
    
    # Validate alternative parameter
    if alternative not in ['two-sided', 'less', 'greater']:
        raise ValueError("alternative must be 'two-sided', 'less', "
                        "or 'greater'")
    
    # Process axis parameter
    if axis is not None:
        # Normalize axis index
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
        # Two-sample Cohen's d
        if paired:
            # Paired samples: use differences
            try:
                np.broadcast_arrays(x, y)
            except ValueError as e:
                raise ValueError("x and y arrays are not compatible for "
                                "broadcasting in paired design") from e
            
            # Calculate differences
            differences = x - y
            
            # Handle NaN values row-wise for paired samples
            if nan_policy == 'omit':
                # For paired samples, omit pairs where either value is NaN
                valid_mask = ~(np.isnan(x) | np.isnan(y))
                if axis is not None:
                    # Apply mask along the specified axis
                    differences = np.where(valid_mask, differences, np.nan)
                    mean_diff = np.nanmean(differences, axis=axis, keepdims=keepdims)
                    std_diff = np.nanstd(differences, axis=axis, ddof=ddof, keepdims=keepdims)
                else:
                    # Flatten and apply mask
                    differences_flat = differences.ravel()
                    valid_flat = valid_mask.ravel()
                    valid_diff = differences_flat[valid_flat]
                    if len(valid_diff) == 0:
                        mean_diff = np.nan
                        std_diff = np.nan
                    else:
                        mean_diff = np.mean(valid_diff)
                        std_diff = np.std(valid_diff, ddof=ddof)
            else:
                mean_diff = np.mean(differences, axis=axis, keepdims=keepdims)
                std_diff = np.std(differences, axis=axis, ddof=ddof, keepdims=keepdims)
            
            # Calculate Cohen's d for paired samples
            with np.errstate(divide='ignore', invalid='ignore'):
                d = mean_diff / std_diff
                
            d = np.where(std_diff == 0, np.nan, d)
            
        else:
            # Independent samples - check dimension compatibility
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
            
            # Calculate Cohen's d for independent samples
            with np.errstate(divide='ignore', invalid='ignore'):
                d = (mean_x - mean_y) / std_pooled
                
            d = np.where(std_pooled == 0, np.nan, d)
    
    # Apply bias correction (Hedges' g) if requested
    if bias_correction:
        # Calculate degrees of freedom for bias correction
        if y is None:
            # One-sample case
            if nan_policy == 'omit':
                n = np.sum(~np.isnan(x), axis=axis, keepdims=keepdims)
            else:
                n = x.shape[axis] if axis is not None else x.size
                if axis is not None and keepdims:
                    n = np.full(d.shape, n)
            df = n - 1
        elif paired:
            # Paired samples case
            if nan_policy == 'omit':
                valid_mask = ~(np.isnan(x) | np.isnan(y))
                n = np.sum(valid_mask, axis=axis, keepdims=keepdims)
            else:
                n = x.shape[axis] if axis is not None else x.size
                if axis is not None and keepdims:
                    n = np.full(d.shape, n)
            df = n - 1
        else:
            # Independent samples case
            if nan_policy == 'omit':
                n_x = np.sum(~np.isnan(x), axis=axis, keepdims=keepdims)
                n_y = np.sum(~np.isnan(y), axis=axis, keepdims=keepdims)
            else:
                n_x = x.shape[axis] if axis is not None else x.size
                n_y = y.shape[axis] if axis is not None else y.size
                if axis is not None and keepdims:
                    n_x = np.full(d.shape, n_x)
                    n_y = np.full(d.shape, n_y)
            df = n_x + n_y - 2
        
        # Apply Hedges' g correction factor: g = d * (1 - 3/(4*df - 1))
        with np.errstate(divide='ignore', invalid='ignore'):
            correction_factor = 1 - 3 / (4 * df - 1)
            d = d * correction_factor
            # Handle cases where df is too small
            d = np.where(df <= 1, np.nan, d)
    
    return d