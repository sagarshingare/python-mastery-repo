# Pandas DataFrame Basics

> **Learning Path**: [Stage 05: Data Analytics & Scientific Libraries](file:///Users/sagarshingare/Documents/python-mastery-repo/LEARNING_PATH.md#stage-05-data-analytics--scientific-libraries) — **Step 5.2**

Core tabular structures in Pandas: Series, DataFrames, data ingestion, cleaning, missing value imputation, vectorized string transformations, and datetime feature extraction.

---

## Key Concepts

1. **Cleaning & Normalization**: Stripping whitespace, column renaming, robust type coercion (`pd.to_numeric`, `pd.to_datetime`).
2. **Missing Value Imputation**: Numeric fill strategies (mean, median, constant) and categorical sentinel defaults.
3. **Vectorized String Methods**: String parsing with regex (`str.extract`), character case conversion, and token length indexing.
4. **Datetime Engineering**: Timestamp decomposition into calendar components (year, month, quarter, day name, weekend indicator).

---

## Running Demonstrations

Run all Basics demonstrations:
```bash
python3 -m pandas_lib.basics.run_examples --demo all
```

Or target specific demonstrations:
```bash
python3 -m pandas_lib.basics.run_examples --demo cleaning
python3 -m pandas_lib.basics.run_examples --demo missing_data
python3 -m pandas_lib.basics.run_examples --demo datetime
```
