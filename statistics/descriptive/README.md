# Descriptive Statistics & Univariate Analytics

> **Learning Path**: [Stage 05: Data Analytics & Scientific Libraries](file:///Users/sagarshingare/Documents/python-mastery-repo/LEARNING_PATH.md#stage-05-data-analytics--scientific-libraries) — **Step 5.3**

Measures of central tendency, dispersion, shape (skewness, kurtosis), Tukey IQR outlier fencing, percentile extraction, and bivariate association metrics.

---

## Key Calculations

1. **Central Tendency & Spread**: Mean, median, sample variance ($s^2$), sample standard deviation ($s$), and interquartile range (IQR).
2. **Distribution Shape**: Skewness (asymmetry) and Fisher kurtosis (tailedness/peakedness).
3. **Outlier Detection**: Tukey's fences defining valid boundaries $[Q_1 - 1.5 \cdot IQR, Q_3 + 1.5 \cdot IQR]$.
4. **Bivariate Association**: Sample covariance, Pearson linear correlation ($r$), and Spearman rank-order correlation ($\rho$).

---

## Running Demonstrations

Run all Descriptive demonstrations:
```bash
python3 -m statistics.descriptive.run_examples --demo all
```

Or run targeted demonstrations:
```bash
python3 -m statistics.descriptive.run_examples --demo summary
python3 -m statistics.descriptive.run_examples --demo outliers
python3 -m statistics.descriptive.run_examples --demo bivariate
```
