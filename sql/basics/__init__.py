"""SQL Fundamentals package: DDL, DML, filtering, aggregation, and pagination."""

from .fundamentals import (
    batch_insert_employees,
    create_connection,
    delete_inactive_employees,
    filter_employees,
    get_department_metrics,
    init_fundamentals_db,
    insert_employee,
    paginate_employees,
    update_employee_salary,
)

__all__ = [
    "create_connection",
    "init_fundamentals_db",
    "insert_employee",
    "batch_insert_employees",
    "update_employee_salary",
    "delete_inactive_employees",
    "filter_employees",
    "get_department_metrics",
    "paginate_employees",
]
