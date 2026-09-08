"""
Unit tests for advanced Core Python primitives:
- Descriptors, Dataclasses, Structured Concurrency
- Decorators (dual-use, stateful, singleton)
- Context Managers (transactions, suppression, ExitStack)
- Generators (flatten, coroutines, pipeline)
- Iterators (DatasetCollection, sentinel, traversal)
- Metaclasses & __init_subclass__
- Memory Management (cyclic gc, weakref, slots)
- Exception Handling (chaining, AppError)
- Packaging (pyproject.toml generation, entrypoints)
"""

from __future__ import annotations
import asyncio
from pathlib import Path
import tempfile
import pytest

# OOPS & Concurrency
from core_python.oops.descriptors import (
    BoundedString,
    EmailField,
    PositiveNumber,
    ReadOnlyDescriptor,
    Typed,
    UserAccount,
)
from core_python.oops.dataclass_features import (
    AuditEntity,
    ImmutableAuditRecord,
    PriorityItem,
    Transaction,
    create_optimized_dataclass,
)
from core_python.async_programming.structured_concurrency import (
    TaskGroupCompat,
    simulate_faulty_worker,
    simulate_fetch,
)

# Decorators
from core_python.decorators.decorators import (
    CallCounter,
    audit_log,
    memoize,
    repeat,
    retry,
    singleton_class,
)

# Context Managers
from core_python.context_managers.resource_contexts import (
    ManagedTransaction,
    SuppressExceptions,
    open_multiple_files,
)

# Generators & Iterators
from core_python.generators.generator_examples import (
    flatten_nested,
    run_pipeline,
    running_average,
)
from core_python.iterators.iterator_utils import (
    DatasetCollection,
    group_consecutive,
    read_until_sentinel,
    take,
)

# Metaclasses & Memory
from core_python.metaclasses.metaclass_examples import (
    BaseTrackedModel,
    PluginRegistryBase,
    SingletonMeta,
)
from core_python.memory_management.memory_utils import (
    ExpensivePayload,
    WeakCache,
    compare_slots_vs_dict,
    create_circular_reference_and_collect,
    get_reference_count,
)

# Exception Handling & Packaging
from core_python.exception_handling.custom_exceptions import AppError, DatabaseError, ValidationError
from core_python.exception_handling.handling_strategies import (
    execute_with_chaining,
    execute_with_suppressed_cause,
)
from core_python.packaging.packaging_guide import (
    ConsoleScript,
    PackageMetadata,
    render_pyproject_toml,
)


# === Descriptors Tests ===

def test_descriptors_validation_success():
    user = UserAccount("alice", "alice@example.com", 150.0)
    assert user.username == "alice"
    assert user.email == "alice@example.com"
    assert user.balance == 150.0


def test_descriptors_validation_failures():
    with pytest.raises(ValueError, match="positive"):
        UserAccount("alice", "alice@example.com", -20.0)

    with pytest.raises(ValueError, match="valid email"):
        UserAccount("alice", "invalid-email", 100.0)

    with pytest.raises(ValueError, match="between 3 and 30"):
        UserAccount("al", "alice@example.com", 100.0)


def test_descriptors_lazy_cached():
    user = UserAccount("bob", "bob@example.com", 50.0)
    assert "expensive_hash" not in user.__dict__

    val1 = user.expensive_hash
    assert "expensive_hash" in user.__dict__
    val2 = user.expensive_hash
    assert val1 == val2


# === Dataclass Tests ===

def test_dataclass_ordering():
    item1 = PriorityItem(priority=1, name="Low")
    item2 = PriorityItem(priority=5, name="High")
    assert item2 > item1
    assert item1 < item2


def test_dataclass_frozen_immutability():
    audit = ImmutableAuditRecord("rec_1", "CREATE", 123456.0, "usr_1")
    mapping = {audit: True}
    assert mapping[audit] is True

    with pytest.raises(Exception):
        audit.action = "DELETE"  # type: ignore


def test_dataclass_initvar_and_postinit():
    txn = Transaction(amount=200.0, currency="USD", tax_rate=0.10)
    assert txn.total == 220.0

    with pytest.raises(ValueError, match="negative"):
        Transaction(amount=-10.0, currency="USD")


def test_dataclass_inheritance_and_slotted():
    entity = AuditEntity(id="ent-99", created_at=100.0, updated_at=120.0, tags=["test"])
    assert entity.id == "ent-99"
    assert entity.is_active is True

    ModernCls = create_optimized_dataclass()
    modern_obj = ModernCls(id=1, name="Modern")
    assert modern_obj.id == 1
    assert modern_obj.name == "Modern"


# === Structured Concurrency Tests ===

def test_structured_concurrency_success():
    async def _runner():
        async with TaskGroupCompat() as tg:
            t1 = tg.create_task(simulate_fetch(1, 0.01))
            t2 = tg.create_task(simulate_fetch(2, 0.01))

        assert t1.result()["data"] == "payload_1"
        assert t2.result()["data"] == "payload_2"

    asyncio.run(_runner())


def test_structured_concurrency_failure_propagation():
    async def _runner():
        with pytest.raises(Exception):
            async with TaskGroupCompat() as tg:
                tg.create_task(simulate_fetch(1, 0.1))
                tg.create_task(simulate_faulty_worker(2))

    asyncio.run(_runner())


# === Decorators Tests ===

def test_stateful_call_counter_and_dual_use():
    @CallCounter
    def add(a: int, b: int) -> int:
        return a + b

    assert add(2, 3) == 5
    assert add(10, 20) == 30
    assert add.call_count == 2
    add.reset()
    assert add.call_count == 0

    # Dual-use
    @audit_log
    def f1():
        return 1

    @audit_log(action="CUSTOM")
    def f2():
        return 2

    assert f1() == 1
    assert f2() == 2


def test_singleton_class_decorator():
    @singleton_class
    class Service:
        pass

    s1 = Service()
    s2 = Service()
    assert s1 is s2


# === Context Managers Tests ===

def test_managed_transaction_commit_and_rollback():
    store = {"x": 10}
    with ManagedTransaction(store) as tx:
        tx["x"] = 20
    assert store["x"] == 20

    # Rollback
    with pytest.raises(ValueError):
        with ManagedTransaction(store) as tx:
            tx["x"] = 50
            raise ValueError("abort")
    assert store["x"] == 20


def test_suppress_exceptions_context():
    with SuppressExceptions(KeyError, ZeroDivisionError):
        _ = 1 / 0
    # Must not raise


def test_exitstack_multiple_files():
    with tempfile.TemporaryDirectory() as tmpdir:
        p1 = Path(tmpdir) / "a.txt"
        p2 = Path(tmpdir) / "b.txt"
        p1.write_text("alpha")
        p2.write_text("beta")
        assert open_multiple_files([p1, p2]) == ["alpha", "beta"]


# === Generators & Iterators Tests ===

def test_flatten_nested_yield_from():
    nested = [1, [2, [3, 4]], 5]
    assert list(flatten_nested(nested)) == [1, 2, 3, 4, 5]


def test_running_average_coroutine():
    avg = running_average()
    next(avg)
    assert avg.send(10) == 10.0
    assert avg.send(20) == 15.0
    assert avg.send(30) == 20.0
    avg.close()


def test_dataset_collection_multi_pass_and_sentinel():
    ds = DatasetCollection([10, 20, 30])
    assert list(ds) == [10, 20, 30]
    assert list(ds) == [10, 20, 30]  # Not exhausted!
    assert list(reversed(ds)) == [30, 20, 10]

    # Sentinel
    q = [1, 2, -1, 3]
    assert read_until_sentinel(lambda: q.pop(0), -1) == [1, 2]


# === Metaclasses & Memory Tests ===

def test_metaclass_and_init_subclass():
    class Model(BaseTrackedModel):
        field_a = 1
        field_b = 2

    assert "field_a" in Model._tracked_attributes
    assert "field_b" in Model._tracked_attributes

    # init_subclass
    class DummyPlugin(PluginRegistryBase, plugin_name="test_plugin"):
        pass

    assert "test_plugin" in PluginRegistryBase.list_plugins()


def test_cyclic_gc_and_weakref():
    collected = create_circular_reference_and_collect()
    assert collected >= 0

    cache = WeakCache()
    item = ExpensivePayload("k1")
    cache.set("k1", item)
    assert cache.size() == 1
    del item
    assert cache.size() == 0


def test_slots_vs_dict_benchmark():
    res = compare_slots_vs_dict(500)
    assert res["count"] == 500
    assert res["slotted_peak_bytes"] < res["regular_peak_bytes"]


# === Exception Handling & Packaging Tests ===

def test_exception_chaining_and_suppressed_cause():
    with pytest.raises(DatabaseError) as exc_info:
        execute_with_chaining("syntax_error")
    assert isinstance(exc_info.value.__cause__, ConnectionRefusedError)

    with pytest.raises(ValidationError) as exc_info2:
        execute_with_suppressed_cause("bad_token")
    assert exc_info2.value.__cause__ is None


def test_packaging_metadata_and_console_script():
    meta = PackageMetadata(name="test-pkg", version="0.1.0")
    toml = render_pyproject_toml(meta)
    assert 'name = "test-pkg"' in toml

    script = ConsoleScript("run-test", "pkg.cli", "start")
    assert script.to_toml_entry() == 'run-test = "pkg.cli:start"'
