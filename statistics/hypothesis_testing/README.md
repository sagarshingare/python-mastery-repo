# Statistical Hypothesis Testing & A/B Experimentation

> **Learning Path**: [Stage 05: Data Analytics & Scientific Libraries](file:///Users/sagarshingare/Documents/python-mastery-repo/LEARNING_PATH.md#stage-05-data-analytics--scientific-libraries) — **Step 5.3**

Parametric and non-parametric hypothesis tests for product experimentation, conversion optimization, and scientific validation using SciPy.

---

## Supported Statistical Tests

1. **One-Sample t-test**: Compare a sample mean against a target SLA or known historical benchmark.
2. **Two-Sample Welch's t-test**: Evaluate A/B experiment treatments with unequal sample sizes and variances.
3. **Paired t-test**: Measure paired pre/post treatment shifts on the same subjects.
4. **One-Way ANOVA**: Test whether any mean among 3+ design variants differs significantly without compounding Type-I error.
5. **Chi-Square Test of Independence**: Test dependence between categorical factors (e.g., Device Platform vs Conversion).
6. **Mann-Whitney U Test**: Non-parametric rank-sum test when normality assumptions fail.

---

## Running Demonstrations

Run all Hypothesis Testing demonstrations:
```bash
python3 -m statistics.hypothesis_testing.run_examples --demo all
```

Or run individual tests:
```bash
python3 -m statistics.hypothesis_testing.run_examples --demo one_sample
python3 -m statistics.hypothesis_testing.run_examples --demo two_sample
python3 -m statistics.hypothesis_testing.run_examples --demo paired
python3 -m statistics.hypothesis_testing.run_examples --demo anova
python3 -m statistics.hypothesis_testing.run_examples --demo chi_square
```
