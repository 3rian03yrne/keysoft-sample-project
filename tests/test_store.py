"""Tests for the in-memory order store."""
from orders import store
from orders.models import Order


def test_fetch_seeded_order() -> None:
    """fetch returns the seeded order for a known id.

    Guards the seed data the other test modules rely on.
    """
    assert store.fetch("A-10422") == Order("A-10422", "Ada Lovelace", 89.0, "shipped")


def test_fetch_unknown_order_returns_none() -> None:
    """fetch returns None rather than raising for an unknown id.

    Callers such as service.cancel_order branch on this None.
    """
    assert store.fetch("does-not-exist") is None


def test_put_inserts_new_order() -> None:
    """put makes a new order retrievable by its id.

    Covers the insert half of put's documented behaviour.
    """
    order = Order("T-100", "Test User", 10.0, "pending")
    store.put(order)
    assert store.fetch("T-100") is order


def test_put_overwrites_existing_order() -> None:
    """put replaces an existing entry with the same id.

    Covers the overwrite half of put's documented behaviour.
    """
    store.put(Order("T-101", "Test User", 10.0, "pending"))
    store.put(Order("T-101", "Test User", 25.0, "shipped"))
    assert store.fetch("T-101") == Order("T-101", "Test User", 25.0, "shipped")


def test_reset_discards_added_orders() -> None:
    """reset removes orders written since the last reset.

    This is what keeps one test's writes from leaking into the next.
    """
    store.put(Order("T-102", "Test User", 10.0, "pending"))
    store.reset()
    assert store.fetch("T-102") is None


def test_reset_undoes_mutations_to_seeded_orders() -> None:
    """reset rebuilds seed orders that were mutated in place.

    Services mutate the Order objects they fetch, so restoring the dict alone
    would not be enough.
    """
    seeded = store.fetch("A-10423")
    assert seeded is not None
    seeded.status = "cancelled"
    store.reset()
    restored = store.fetch("A-10423")
    assert restored is not None
    assert restored.status == "pending"
