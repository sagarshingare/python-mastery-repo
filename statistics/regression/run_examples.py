"""Demonstrations for Regression Analysis and Ordinary Least Squares."""

from __future__ import annotations

import argparse
import numpy as np

from .regression_analysis import (
    simple_linear_regression,
    multiple_linear_regression,
    predict_linear,
)


def demo_simple() -> None:
    print("--- 1. Simple Linear Regression (Advertising Spend vs Sales) ---")
    np.random.seed(42)
    ad_spend = np.linspace(10, 100, 30)
    sales = 25.0 + 1.8 * ad_spend + np.random.normal(0, 8, size=30)

    model = simple_linear_regression(ad_spend, sales)
    print(f"  Fitted Equation: Sales = {model['intercept']:.2f} + {model['slope']:.2f} * Spend")
    print(f"  R-Squared (R²):  {model['r_squared']:.4f} ({model['r_squared']*100:.1f}% variance explained)")
    print(f"  RMSE:            ${model['rmse']:.2f} | MAE: ${model['mae']:.2f}")
    print(f"  p-value:         {model['p_value']:.4e} (Slope Std Err: {model['std_err']:.4f})")


def demo_multiple() -> None:
    print("\n--- 2. Multiple Linear Regression (Housing Valuation) ---")
    np.random.seed(42)
    n = 100
    # Features: square_feet, bedrooms, age_years
    sqft = np.random.uniform(800, 3500, size=n)
    beds = np.random.randint(1, 5, size=n)
    age = np.random.uniform(0, 40, size=n)

    # Ground truth: Price = 50,000 + 150*sqft + 15,000*beds - 800*age + noise
    price = 50000.0 + 150.0 * sqft + 15000.0 * beds - 800.0 * age + np.random.normal(0, 15000, size=n)
    X = np.column_stack([sqft, beds, age])
    feature_names = ["sqft", "bedrooms", "age_years"]

    model = multiple_linear_regression(X, price, feature_names=feature_names)
    print(f"  Intercept (β0): ${model['intercept']:,.2f}")
    print("  Feature Coefficients:")
    for feat, beta in model["coefficients"].items():
        print(f"    - {feat:<10}: {beta:+10.2f}")
    print(f"  R²:             {model['r_squared']:.4f} | Adjusted R²: {model['adjusted_r_squared']:.4f}")
    print(f"  RMSE:           ${model['rmse']:,.2f}")
    print(f"  Residual Mean:  ${model['residual_mean']:.4f} (centered at 0)")

    # Out-of-sample prediction test
    new_home = np.array([[2400, 3, 5]])  # 2400 sqft, 3 beds, 5 years old
    predicted_price = predict_linear(new_home, model)[0]
    print(f"\n  Valuation for 2,400 sqft, 3-bed, 5-yr house: ${predicted_price:,.2f}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Regression Analysis Demonstrations")
    parser.add_argument(
        "--demo",
        choices=["all", "simple", "multiple"],
        default="all",
        help="Specific regression demo to run",
    )
    args = parser.parse_args()

    print("=== REGRESSION ANALYSIS DEMONSTRATIONS ===")
    if args.demo in ("all", "simple"):
        demo_simple()
    if args.demo in ("all", "multiple"):
        demo_multiple()


if __name__ == "__main__":
    main()
