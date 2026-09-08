# Probability Distributions

> **Learning Path**: [Stage 05: Data Analytics & Scientific Libraries](file:///Users/sagarshingare/Documents/python-mastery-repo/LEARNING_PATH.md#stage-05-data-analytics--scientific-libraries) — **Step 5.3**

Theoretical continuous and discrete probability distributions, empirical coverage rules, and goodness-of-fit hypothesis testing using SciPy.

---

## Supported Distributions

1. **Gaussian / Normal ($N(\mu, \sigma^2)$)**: PDF, CDF, percent point function, and empirical $68.27\% - 95.45\% - 99.73\%$ rule validation.
2. **Binomial ($B(n, p)$)**: Discrete Bernoulli trials, PMF, and cumulative CDF success probabilities.
3. **Poisson ($\text{Pois}(\lambda)$)**: Discrete arrival rate modeling, memoryless dispersion ($E[X] = \text{Var}(X) = \lambda$).
4. **Exponential ($\text{Exp}(\lambda)$)**: Continuous wait-time modeling.
5. **Kolmogorov-Smirnov Test**: Non-parametric test comparing sample distributions against theoretical CDFs.

---

## Running Demonstrations

Run all Distribution demonstrations:
```bash
python3 -m statistics.distributions.run_examples --demo all
```

Or run individual distributions:
```bash
python3 -m statistics.distributions.run_examples --demo normal
python3 -m statistics.distributions.run_examples --demo binomial
python3 -m statistics.distributions.run_examples --demo poisson
python3 -m statistics.distributions.run_examples --demo exponential
python3 -m statistics.distributions.run_examples --demo fit
```
