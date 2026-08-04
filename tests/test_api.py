from orders import store
from orders.api import handle_refund
from orders.models import Order


def test_handle_refund_shipped_order():
    store.save(Order("T-3", "Test User", 10.0, "shipped"))
    result = handle_refund("T-3")
    assert result == {"ok": True, "order_id": "T-3", "status": "refunded"}


def test_handle_refund_unknown_order():
    result = handle_refund("does-not-exist")
    assert result == {"ok": False, "error": "'unknown order: does-not-exist'"}


def test_handle_refund_non_shipped_order():
    store.save(Order("T-4", "Test User", 10.0, "pending"))
    result = handle_refund("T-4")
    assert result == {"ok": False, "error": "cannot refund a pending order"}
