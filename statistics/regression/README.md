# Linear Regression Analysis

> **Learning Path**: [Stage 05: Data Analytics & Scientific Libraries](file:///Users/sagarshingare/Documents/python-mastery-repo/LEARNING_PATH.md#stage-05-data-analytics--scientific-libraries) — **Step 5.3**

Ordinary Least Squares (OLS) linear modeling, multi-variable design matrix formulation, coefficient estimation, and model evaluation metrics (RMSE, MAE, $R^2$, Adjusted $R^2$).

---

## Key Methodologies

1. **Simple Linear Regression**: Univariate trend fitting ($y = \beta_0 + \beta_1 x + \epsilon$) via Wald tests and SciPy linregress.
2. **Multiple Linear Regression**: Closed-form Normal Equations $\hat{\beta} = (X^T X)^{-1} X^T y$ via `np.linalg.lstsq` with an augmented bias column.
3. **Model Evaluation Metrics**:
   - **$R^2$**: Coefficient of determination ($1 - SS_{\text{res}} / SS_{\text{tot}}$).
   - **Adjusted $R^2$**: Penalizes model complexity / degrees of freedom ($1 - (1 - R^2) \frac{n - 1}{n - p - 1}$).
   - **RMSE / MAE**: Standardized error scale in raw target units.
4. **Out-of-Sample Inference**: Applying learned parameters to unseen feature records.

---

## Running Demonstrations

Run all Regression demonstrations:
```bash
python3 -m statistics.regression.run_examples --demo all
```

Or run individual models:
```bash
python3 -m statistics.regression.run_examples --demo simple
python3 -m statistics.regression.run_examples --demo multiple
```
