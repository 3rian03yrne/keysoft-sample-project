import pytest

from orders import store
from orders.models import Order
from orders.service import cancel_order, refund_order


def test_cancel_pending_order():
    store.save(Order("T-1", "Test User", 10.0, "pending"))
    result = cancel_order("T-1")
    assert result.status == "cancelled"


def test_cancel_unknown_order_raises():
    with pytest.raises(KeyError):
        cancel_order("does-not-exist")


def test_cannot_cancel_shipped_order():
    store.save(Order("T-2", "Test User", 10.0, "shipped"))
    with pytest.raises(ValueError):
        cancel_order("T-2")


def test_refund_shipped_order():
    store.save(Order("T-3", "Test User", 10.0, "shipped"))
    result = refund_order("T-3")
    assert result.status == "refunded"


def test_refund_unknown_order_raises():
    with pytest.raises(KeyError):
        refund_order("does-not-exist")


def test_cannot_refund_pending_order():
    store.save(Order("T-4", "Test User", 10.0, "pending"))
    with pytest.raises(ValueError):
        refund_order("T-4")
