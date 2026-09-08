# Statistical Analysis & Scientific Computing

> **Learning Path**: [Stage 04: SQL](file:///Users/sagarshingare/Documents/python-mastery-repo/sql) ➔ [Stage 05: Data Analytics](file:///Users/sagarshingare/Documents/python-mastery-repo/LEARNING_PATH.md#stage-05-data-analytics--scientific-libraries) ▸ **Step 5.3: Statistical Analysis**

Mathematical foundations of data analytics, probabilistic reasoning, experimentation inference, and linear modeling using NumPy, Pandas, and SciPy.

---

## Submodule Directory

| Submodule | Focus | Key Highlights |
|:---|:---|:---|
| [`descriptive/`](file:///Users/sagarshingare/Documents/python-mastery-repo/statistics/descriptive) | Univariate & Bivariate | Central tendency, dispersion, skewness/kurtosis, Tukey IQR outlier fencing, Pearson/Spearman correlation |
| [`distributions/`](file:///Users/sagarshingare/Documents/python-mastery-repo/statistics/distributions) | Probability Models | Normal (68-95-99.7 empirical rule), Binomial, Poisson, Exponential, and Kolmogorov-Smirnov goodness-of-fit |
| [`hypothesis_testing/`](file:///Users/sagarshingare/Documents/python-mastery-repo/statistics/hypothesis_testing) | Experimentation & A/B | One-sample t-test, Welch's two-sample t-test, paired t-test, One-Way ANOVA, Chi-Square independence, Mann-Whitney U |
| [`regression/`](file:///Users/sagarshingare/Documents/python-mastery-repo/statistics/regression) | Linear Modeling & OLS | Simple univariate regression, multiple OLS linear regression via Normal Equations, $R^2$, Adj-$R^2$, RMSE, out-of-sample prediction |

---

## Running Demonstrations

### 1. Unified Master Demonstration
Execute all Statistics submodules sequentially:
```bash
python3 -m statistics.run_examples --submodule all
# or
python3 -m statistics.examples
```

### 2. Direct Submodule Runners
```bash
# Descriptive summary, IQR outliers, and correlation
python3 -m statistics.descriptive.run_examples --demo all

# Continuous/discrete distributions and KS normality tests
python3 -m statistics.distributions.run_examples --demo all

# Statistical hypothesis testing and A/B experiment evaluation
python3 -m statistics.hypothesis_testing.run_examples --demo all

# Simple and multiple linear regression with OLS
python3 -m statistics.regression.run_examples --demo all
```
