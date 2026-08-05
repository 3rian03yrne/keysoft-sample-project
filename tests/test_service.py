"""Tests for the order business logic."""
import pytest

from orders import store
from orders.models import Order
from orders.service import cancel_order, refund_order


def test_cancel_pending_order() -> None:
    """cancel_order moves a pending order to cancelled.

    Happy path for cancellation.
    """
    store.put(Order("T-1", "Test User", 10.0, "pending"))
    result = cancel_order("T-1")
    assert result.status == "cancelled"


def test_cancel_persists_new_status() -> None:
    """cancel_order writes the new status back to the store.

    A returned-but-unsaved order would leave the store stale.
    """
    store.put(Order("T-5", "Test User", 10.0, "pending"))
    cancel_order("T-5")
    stored = store.fetch("T-5")
    assert stored is not None
    assert stored.status == "cancelled"


def test_cancel_unknown_order_raises() -> None:
    """cancel_order raises KeyError for an unknown order.

    Unknown ids must not resolve to a silent no-op.
    """
    with pytest.raises(KeyError):
        cancel_order("does-not-exist")


def test_cannot_cancel_shipped_order() -> None:
    """cancel_order raises ValueError for a shipped order.

    Only pending orders are cancellable.
    """
    store.put(Order("T-2", "Test User", 10.0, "shipped"))
    with pytest.raises(ValueError):
        cancel_order("T-2")


def test_refund_shipped_order() -> None:
    """refund_order moves a shipped order to refunded.

    Happy path for refunds.
    """
    store.put(Order("T-3", "Test User", 10.0, "shipped"))
    result = refund_order("T-3")
    assert result.status == "refunded"


def test_refund_persists_new_status() -> None:
    """refund_order writes the new status back to the store.

    A returned-but-unsaved order would leave the store stale.
    """
    store.put(Order("T-6", "Test User", 10.0, "shipped"))
    refund_order("T-6")
    stored = store.fetch("T-6")
    assert stored is not None
    assert stored.status == "refunded"


def test_refund_unknown_order_raises() -> None:
    """refund_order raises KeyError for an unknown order.

    Unknown ids must not resolve to a silent no-op.
    """
    with pytest.raises(KeyError):
        refund_order("does-not-exist")


def test_cannot_refund_pending_order() -> None:
    """refund_order raises ValueError for a pending order.

    Only shipped orders are refundable.
    """
    store.put(Order("T-4", "Test User", 10.0, "pending"))
    with pytest.raises(ValueError):
        refund_order("T-4")
