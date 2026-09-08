"""Regression analysis: Ordinary Least Squares (OLS), multiple regression, and evaluation metrics."""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Sequence, Tuple

import numpy as np
from scipy import stats

logger = logging.getLogger(__name__)


def simple_linear_regression(
    x: Sequence[float],
    y: Sequence[float],
) -> Dict[str, Any]:
    """Fit a simple univariate linear model y = slope * x + intercept."""
    x_arr = np.asarray(x, dtype=float)
    y_arr = np.asarray(y, dtype=float)

    res = stats.linregress(x_arr, y_arr)
    y_pred = res.intercept + res.slope * x_arr
    residuals = y_arr - y_pred

    rmse = float(np.sqrt(np.mean(residuals**2)))
    mae = float(np.mean(np.abs(residuals)))
    r_squared = float(res.rvalue**2)

    return {
        "slope": float(res.slope),
        "intercept": float(res.intercept),
        "r_value": float(res.rvalue),
        "r_squared": r_squared,
        "p_value": float(res.pvalue),
        "std_err": float(res.stderr),
        "rmse": rmse,
        "mae": mae,
    }


def multiple_linear_regression(
    X: np.ndarray,
    y: np.ndarray,
    feature_names: Sequence[str] | None = None,
) -> Dict[str, Any]:
    """Fit multiple linear regression model using closed-form Ordinary Least Squares (OLS).
    
    y = X * beta + intercept
    """
    X_mat = np.asarray(X, dtype=float)
    y_vec = np.asarray(y, dtype=float)
    n_samples, n_features = X_mat.shape

    # Augment design matrix with bias column for intercept
    X_design = np.hstack([np.ones((n_samples, 1)), X_mat])

    # Solve normal equations: beta = (X^T X)^(-1) X^T y using robust lstsq
    beta, residuals, rank, s = np.linalg.lstsq(X_design, y_vec, rcond=None)

    intercept = float(beta[0])
    coefficients = [float(b) for b in beta[1:]]

    # Model predictions and residual calculations
    y_pred = X_design @ beta
    res_vec = y_vec - y_pred

    ss_res = float(np.sum(res_vec**2))
    ss_tot = float(np.sum((y_vec - np.mean(y_vec)) ** 2))
    r_squared = 1.0 - (ss_res / ss_tot) if ss_tot > 0 else 0.0

    # Adjusted R-squared: 1 - (1 - R^2) * (n - 1) / (n - p - 1)
    dof_adj = (n_samples - 1) / max(n_samples - n_features - 1, 1)
    adj_r_squared = 1.0 - (1.0 - r_squared) * dof_adj

    mse = float(np.mean(res_vec**2))
    rmse = float(np.sqrt(mse))
    mae = float(np.mean(np.abs(res_vec)))

    names = list(feature_names) if feature_names else [f"x{i+1}" for i in range(n_features)]
    coef_dict = {name: coef for name, coef in zip(names, coefficients)}

    return {
        "n_samples": n_samples,
        "n_features": n_features,
        "intercept": intercept,
        "coefficients": coef_dict,
        "r_squared": float(r_squared),
        "adjusted_r_squared": float(adj_r_squared),
        "mse": mse,
        "rmse": rmse,
        "mae": mae,
        "residual_mean": float(np.mean(res_vec)),
        "residual_std": float(np.std(res_vec, ddof=1)),
    }


def predict_linear(
    X: np.ndarray,
    model: Dict[str, Any],
) -> np.ndarray:
    """Predict targets using fitted multiple regression coefficients."""
    X_mat = np.asarray(X, dtype=float)
    intercept = model["intercept"]
    coefs = np.array(list(model["coefficients"].values()), dtype=float)
    return intercept + X_mat @ coefs
