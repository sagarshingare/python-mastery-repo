"""PySpark actions - collect, count, save, and write operations.

This module demonstrates PySpark action concepts including:
- Collect - retrieve data to driver
- Count - count rows in DataFrame
- First/Take - get limited rows
- Foreach - apply function to each row
- Save/Write - persist DataFrames to storage
- Show - display formatted output

Python version: 3.9+
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

try:
    from pyspark.sql import SparkSession
    HAS_PYSPARK = True
except ImportError:
    HAS_PYSPARK = False


def collect_data(df: Any) -> List[tuple]:
    """Collect all DataFrame rows to driver memory.
    
    Args:
        df: DataFrame to collect.
        
    Returns:
        List of Row objects as tuples.
    """
    if df is None or not HAS_PYSPARK:
        return []
    
    try:
        rows = df.collect()
        return [tuple(row) for row in rows]
    except Exception as e:
        print(f"Error collecting data: {e}")
        return []


def count_rows(df: Any) -> int:
    """Count total rows in DataFrame.
    
    Args:
        df: DataFrame to count.
        
    Returns:
        Number of rows.
    """
    if df is None or not HAS_PYSPARK:
        return 0
    
    try:
        return df.count()
    except Exception as e:
        print(f"Error counting rows: {e}")
        return 0


def get_first_row(df: Any) -> Optional[tuple]:
    """Get first row from DataFrame.
    
    Args:
        df: DataFrame to get first row from.
        
    Returns:
        First row as tuple or None.
    """
    if df is None or not HAS_PYSPARK:
        return None
    
    try:
        first = df.first()
        return tuple(first) if first else None
    except Exception as e:
        print(f"Error getting first row: {e}")
        return None


def take_rows(df: Any, n: int = 5) -> List[tuple]:
    """Take first n rows from DataFrame.
    
    Args:
        df: DataFrame to take rows from.
        n: Number of rows to take.
        
    Returns:
        List of rows as tuples.
    """
    if df is None or not HAS_PYSPARK:
        return []
    
    try:
        rows = df.take(n)
        return [tuple(row) for row in rows]
    except Exception as e:
        print(f"Error taking rows: {e}")
        return []


def show_data(df: Any, num_rows: int = 5, truncate: bool = True) -> None:
    """Display DataFrame in formatted table.
    
    Args:
        df: DataFrame to display.
        num_rows: Number of rows to show.
        truncate: Whether to truncate long values.
    """
    if df is None or not HAS_PYSPARK:
        print("DataFrame is None or PySpark not available")
        return
    
    try:
        df.show(num_rows, truncate=truncate)
    except Exception as e:
        print(f"Error displaying DataFrame: {e}")


def foreach_row(df: Any, func: Any) -> int:
    """Apply function to each row (for side effects).
    
    Args:
        df: DataFrame to iterate.
        func: Function to apply to each row.
        
    Returns:
        Count of rows processed.
    """
    if df is None or not HAS_PYSPARK:
        return 0
    
    try:
        count = 0
        for row in df.collect():
            func(row)
            count += 1
        return count
    except Exception as e:
        print(f"Error in foreach: {e}")
        return 0


def write_parquet(df: Any, path: str, mode: str = "overwrite") -> bool:
    """Write DataFrame to Parquet format.
    
    Args:
        df: DataFrame to write.
        path: Output path.
        mode: Write mode ('overwrite', 'append', 'ignore', 'error').
        
    Returns:
        True if successful, False otherwise.
    """
    if df is None or not HAS_PYSPARK:
        return False
    
    try:
        df.write.mode(mode).parquet(path)
        return True
    except Exception as e:
        print(f"Error writing Parquet: {e}")
        return False


def write_csv(df: Any, path: str, mode: str = "overwrite", header: bool = True) -> bool:
    """Write DataFrame to CSV format.
    
    Args:
        df: DataFrame to write.
        path: Output path.
        mode: Write mode.
        header: Whether to write header row.
        
    Returns:
        True if successful, False otherwise.
    """
    if df is None or not HAS_PYSPARK:
        return False
    
    try:
        df.write.mode(mode).option("header", header).csv(path)
        return True
    except Exception as e:
        print(f"Error writing CSV: {e}")
        return False


def write_json(df: Any, path: str, mode: str = "overwrite") -> bool:
    """Write DataFrame to JSON format.
    
    Args:
        df: DataFrame to write.
        path: Output path.
        mode: Write mode.
        
    Returns:
        True if successful, False otherwise.
    """
    if df is None or not HAS_PYSPARK:
        return False
    
    try:
        df.write.mode(mode).json(path)
        return True
    except Exception as e:
        print(f"Error writing JSON: {e}")
        return False


def write_sql_table(df: Any, table_name: str, mode: str = "overwrite") -> bool:
    """Write DataFrame as SQL table.
    
    Args:
        df: DataFrame to write.
        table_name: Table name.
        mode: Write mode.
        
    Returns:
        True if successful, False otherwise.
    """
    if df is None or not HAS_PYSPARK:
        return False
    
    try:
        df.write.mode(mode).saveAsTable(table_name)
        return True
    except Exception as e:
        print(f"Error writing table: {e}")
        return False


def get_statistics(df: Any) -> Dict[str, Any]:
    """Get basic statistics about DataFrame.
    
    Args:
        df: DataFrame to analyze.
        
    Returns:
        Dictionary with row count, column count, columns, and dtypes.
    """
    if df is None or not HAS_PYSPARK:
        return {}
    
    try:
        return {
            "row_count": df.count(),
            "column_count": len(df.columns),
            "columns": df.columns,
            "dtypes": df.dtypes,
        }
    except Exception as e:
        print(f"Error getting statistics: {e}")
        return {}