"""Unit tests for newly added DSA and API development modules."""

from __future__ import annotations

import pytest
from starlette.testclient import TestClient
from fastapi import FastAPI

from api_development.authentication.auth_utils import (
    Role,
    generate_api_key,
    has_sufficient_permission,
    hash_password,
    verify_api_key,
    verify_password,
)
from api_development.fastapi.crud_api import router as item_router
from api_development.jwt.jwt_handler import (
    InvalidSignatureError,
    TokenExpiredError,
    decode_jwt,
    encode_jwt,
)
from api_development.rate_limiting.rate_limiter import SlidingWindowRateLimiter, TokenBucket
from dsa.dynamic_programming import edit_distance, fibonacci_memo, knapsack_01
from dsa.graphs import Graph
from dsa.heaps import MinHeap, top_k_elements
from dsa.linked_list import SinglyLinkedList
from dsa.queue import CircularQueue, Queue
from dsa.sliding_window import max_sum_subarray
from dsa.stack import MinStack, Stack, is_balanced
from dsa.strings import are_anagrams, is_palindrome, kmp_search
from dsa.system_design import BloomFilter, LRUCache
from dsa.trees import BinarySearchTree, inorder


# ---------------------------------------------------------------------------
# DSA Tests
# ---------------------------------------------------------------------------


def test_singly_linked_list() -> None:
    sll = SinglyLinkedList()
    sll.append(10)
    sll.append(20)
    sll.prepend(5)
    assert list(sll) == [5, 10, 20]
    assert sll.delete_value(10) is True
    assert list(sll) == [5, 20]
    sll.reverse()
    assert list(sll) == [20, 5]


def test_stack_and_balanced_parentheses() -> None:
    stack = Stack()
    stack.push(1)
    stack.push(2)
    assert stack.pop() == 2
    assert is_balanced("({[]})") is True
    assert is_balanced("({[})") is False

    min_stack = MinStack()
    min_stack.push(5)
    min_stack.push(2)
    min_stack.push(8)
    assert min_stack.get_min() == 2
    min_stack.pop()
    assert min_stack.get_min() == 2
    min_stack.pop()
    assert min_stack.get_min() == 5


def test_queue_and_circular_queue() -> None:
    q = Queue()
    q.enqueue("a")
    q.enqueue("b")
    assert q.dequeue() == "a"

    cq = CircularQueue(capacity=3)
    cq.enqueue(1)
    cq.enqueue(2)
    cq.enqueue(3)
    assert cq.is_full is True
    assert cq.dequeue() == 1
    cq.enqueue(4)
    assert len(cq) == 3


def test_binary_search_tree() -> None:
    bst = BinarySearchTree()
    for val in [50, 30, 70, 20, 40, 60, 80]:
        bst.insert(val)
    assert inorder(bst.root) == [20, 30, 40, 50, 60, 70, 80]
    assert bst.search(40) is True
    assert bst.search(99) is False


def test_graph_traversals() -> None:
    g = Graph(directed=True)
    g.add_edge("A", "B")
    g.add_edge("A", "C")
    g.add_edge("B", "D")
    assert g.bfs("A") == ["A", "B", "C", "D"]
    assert "D" in g.dfs("A")


def test_min_heap() -> None:
    heap = MinHeap()
    for val in [40, 10, 30, 5, 20]:
        heap.push(val)
    assert heap.pop() == 5
    assert heap.pop() == 10
    assert top_k_elements([10, 5, 20, 8, 15], 2) == [20, 15]


def test_string_algorithms() -> None:
    assert is_palindrome("A man, a plan, a canal: Panama") is True
    assert is_palindrome("race a car") is False
    assert are_anagrams("anagram", "nagaram") is True
    assert are_anagrams("rat", "car") is False
    assert kmp_search("ABABDABACDABABCABAB", "ABABCABAB") == [10]


def test_dynamic_programming() -> None:
    assert fibonacci_memo(10) == 55
    assert knapsack_01([10, 20, 30], [60, 100, 120], 50) == 220
    assert edit_distance("kitten", "sitting") == 3


def test_sliding_window() -> None:
    assert max_sum_subarray([2, 1, 5, 1, 3, 2], 3) == 9


def test_system_design_structures() -> None:
    # LRU Cache
    cache = LRUCache(capacity=2)
    cache.put("a", 1)
    cache.put("b", 2)
    assert cache.get("a") == 1
    cache.put("c", 3)  # evicts 'b'
    assert cache.get("b") is None
    assert cache.get("c") == 3

    # Bloom filter
    bf = BloomFilter(expected_items=100, fp_rate=0.01)
    bf.add("hello")
    bf.add("world")
    assert "hello" in bf
    assert "python" not in bf


# ---------------------------------------------------------------------------
# API Development Tests
# ---------------------------------------------------------------------------


def test_auth_and_rbac() -> None:
    pw = "SuperSecret#2026"
    hashed = hash_password(pw)
    assert verify_password(pw, hashed) is True
    assert verify_password("wrong", hashed) is False

    key = generate_api_key()
    assert verify_api_key(key, key) is True
    assert verify_api_key(key, "fake_key") is False

    assert has_sufficient_permission(Role.ADMIN, Role.USER) is True
    assert has_sufficient_permission(Role.USER, Role.ADMIN) is False


def test_jwt_lifecycle() -> None:
    secret = "jwt-test-secret"
    token = encode_jwt({"sub": "user_10"}, secret, expires_in_seconds=60)
    decoded = decode_jwt(token, secret)
    assert decoded["sub"] == "user_10"

    with pytest.raises(InvalidSignatureError):
        decode_jwt(token, "wrong-secret")

    expired = encode_jwt({"sub": "user_10"}, secret, expires_in_seconds=-5)
    with pytest.raises(TokenExpiredError):
        decode_jwt(expired, secret)


def test_rate_limiter() -> None:
    bucket = TokenBucket(capacity=2, refill_rate=1.0)
    assert bucket.consume() is True
    assert bucket.consume() is True
    assert bucket.consume() is False

    limiter = SlidingWindowRateLimiter(max_requests=2, window_seconds=10.0)
    assert limiter.is_allowed("client_1") is True
    assert limiter.is_allowed("client_1") is True
    assert limiter.is_allowed("client_1") is False
    assert limiter.is_allowed("client_2") is True


def test_fastapi_crud_endpoints() -> None:
    app = FastAPI()
    app.include_router(item_router)
    client = TestClient(app)

    # 1. Create
    resp = client.post("/items/", json={"title": "Mouse", "price": 29.99, "category": "tech"})
    assert resp.status_code == 201
    item_id = resp.json()["id"]

    # 2. Get by ID
    get_resp = client.get(f"/items/{item_id}")
    assert get_resp.status_code == 200
    assert get_resp.json()["title"] == "Mouse"

    # 3. List
    list_resp = client.get("/items/?category=tech")
    assert list_resp.status_code == 200
    assert list_resp.json()["total"] >= 1

    # 4. Update
    put_resp = client.put(f"/items/{item_id}", json={"price": 34.99})
    assert put_resp.status_code == 200
    assert put_resp.json()["price"] == 34.99

    # 5. Delete
    del_resp = client.delete(f"/items/{item_id}")
    assert del_resp.status_code == 204

    # 6. Verify 404
    assert client.get(f"/items/{item_id}").status_code == 404
