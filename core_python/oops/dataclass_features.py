"""
Advanced Dataclass Patterns & Idioms
===================================
Covers modern Python dataclass mechanics:
- `frozen=True` (immutability and hashing)
- `order=True` (rich ordering comparisons)
- `field(default_factory=...)`, `field(repr=False)`, `field(compare=False)`
- `InitVar` and `__post_init__` for field validation and derivation
- Inheritance hierarchies with dataclasses
- Memory optimization: `__slots__` vs standard `__dict__`
- `asdict`, `astuple`, `replace` utilities
- Version differences (Python 3.10 `slots=True`, `kw_only=True`)
"""

from __future__ import annotations
import sys
from dataclasses import InitVar, asdict, astuple, dataclass, field, replace
from typing import Any, Dict, List, Optional


@dataclass(order=True)
class PriorityItem:
    """Demonstrates rich comparison ordering and field exclusion."""
    priority: int
    name: str = field(compare=False)
    payload: Dict[str, Any] = field(default_factory=dict, repr=False, compare=False)


@dataclass(frozen=True)
class ImmutableAuditRecord:
    """Demonstrates frozen immutability and hashability for sets/dicts."""
    record_id: str
    action: str
    timestamp: float
    actor_id: str

    def __post_init__(self) -> None:
        if not self.record_id:
            raise ValueError("record_id must be non-empty")


@dataclass
class Transaction:
    """Demonstrates InitVar and post-initialization validation/computation."""
    amount: float
    currency: str
    tax_rate: InitVar[float] = 0.0
    total: float = field(init=False)
    metadata: Dict[str, str] = field(default_factory=dict)

    def __post_init__(self, tax_rate: float) -> None:
        if self.amount < 0:
            raise ValueError("amount cannot be negative")
        self.total = round(self.amount * (1 + tax_rate), 2)


# Dataclass Inheritance
@dataclass
class BaseEntity:
    id: str
    created_at: float


@dataclass
class AuditEntity(BaseEntity):
    updated_at: float
    is_active: bool = True
    tags: List[str] = field(default_factory=list)


def create_optimized_dataclass() -> Any:
    """Conditionally applies slots=True and kw_only=True on Python 3.10+."""
    if sys.version_info >= (3, 10):
        # On Python 3.10+, slots=True reduces memory by replacing __dict__
        exec(
            """
@dataclass(slots=True, kw_only=True)
class ModernRecord:
    id: int
    name: str
    score: float = 0.0
""",
            globals(),
        )
        return globals()["ModernRecord"]
    else:
        # On Python 3.9, slots without class variable conflict
        @dataclass
        class ModernRecord:
            __slots__ = ("id", "name", "_score")
            id: int
            name: str
            _score: float

            def __init__(self, id: int, name: str, score: float = 0.0) -> None:
                self.id = id
                self.name = name
                self._score = score

            @property
            def score(self) -> float:
                return self._score

        return ModernRecord


def run_dataclass_demos() -> None:
    """Execute dataclass feature demonstrations."""
    print("=== Advanced Dataclass Demonstrations ===")

    # 1. Ordering and Comparison
    low = PriorityItem(priority=1, name="Process Low Batch")
    high = PriorityItem(priority=10, name="Critical Alert")
    print(f"Priority comparison (high > low): {high > low}")
    assert high > low

    # 2. Immutability and Hashing
    audit = ImmutableAuditRecord("rec-001", "LOGIN", 1700000000.0, "user-42")
    cache = {audit: "Valid session"}
    print(f"Audit record in dict key: {cache[audit]}")
    try:
        # Should raise FrozenInstanceError
        audit.action = "LOGOUT"  # type: ignore
    except Exception as err:
        print(f"Caught expected frozen error: {type(err).__name__}")

    # 3. InitVar & Post-Init
    txn = Transaction(amount=100.0, currency="USD", tax_rate=0.08)
    print(f"Transaction: amount={txn.amount}, total with 8% tax={txn.total}")
    assert txn.total == 108.0

    # 4. Utilities: asdict, astuple, replace
    txn_dict = asdict(txn)
    print(f"Serialized asdict keys: {list(txn_dict.keys())}")
    cloned_txn = replace(txn, amount=200.0)
    print(f"Cloned transaction amount: {cloned_txn.amount}")

    # 5. Inheritance
    record = AuditEntity(id="ent-1", created_at=100.0, updated_at=105.0, tags=["prod", "v2"])
    print(f"Inherited dataclass: {record}")

    # 6. Modern / Slotted Record
    ModernRecordClass = create_optimized_dataclass()
    modern_item = ModernRecordClass(id=1, name="Slotted Data", score=99.5)
    print(f"Modern/Slotted dataclass created: {modern_item}")

    print("Dataclass demonstrations completed successfully!\n")


if __name__ == "__main__":
    run_dataclass_demos()
