"""Tests for the order request handlers."""
from orders import store
from orders.api import handle_cancel_order, handle_get_order, handle_refund
from orders.models import Order


def test_handle_get_order_known_order() -> None:
    """handle_get_order returns the order as a plain dict.

    Only the fields the handler documents are exposed.
    """
    store.put(Order("T-10", "Test User", 10.0, "shipped"))
    result = handle_get_order("T-10")
    assert result == {"order_id": "T-10", "status": "shipped", "total_usd": 10.0}


def test_handle_get_order_unknown_order() -> None:
    """handle_get_order returns an empty dict for an unknown order.

    Documented behaviour of the handler's None branch.
    """
    result = handle_get_order("does-not-exist")
    assert result == {}


def test_handle_cancel_order_pending_order() -> None:
    """handle_cancel_order reports a successful cancellation.

    Happy path through the cancel handler.
    """
    store.put(Order("T-11", "Test User", 10.0, "pending"))
    result = handle_cancel_order("T-11")
    assert result == {"ok": True, "order_id": "T-11", "status": "cancelled"}


def test_handle_cancel_order_unknown_order() -> None:
    """handle_cancel_order reports an unquoted error for an unknown order.

    The KeyError raised by the service must not leak its repr quotes.
    """
    result = handle_cancel_order("does-not-exist")
    assert result == {"ok": False, "error": "unknown order: does-not-exist"}


def test_handle_cancel_order_shipped_order() -> None:
    """handle_cancel_order reports an error for a non-pending order.

    Covers the ValueError branch of the cancel handler.
    """
    store.put(Order("T-12", "Test User", 10.0, "shipped"))
    result = handle_cancel_order("T-12")
    assert result == {"ok": False, "error": "cannot cancel a shipped order"}


def test_handle_refund_shipped_order() -> None:
    """handle_refund reports a successful refund.

    Happy path through the refund handler.
    """
    store.put(Order("T-13", "Test User", 10.0, "shipped"))
    result = handle_refund("T-13")
    assert result == {"ok": True, "order_id": "T-13", "status": "refunded"}


def test_handle_refund_unknown_order() -> None:
    """handle_refund reports an unquoted error for an unknown order.

    The KeyError raised by the service must not leak its repr quotes.
    """
    result = handle_refund("does-not-exist")
    assert result == {"ok": False, "error": "unknown order: does-not-exist"}


def test_handle_refund_non_shipped_order() -> None:
    """handle_refund reports an error for a non-shipped order.

    Covers the ValueError branch of the refund handler.
    """
    store.put(Order("T-14", "Test User", 10.0, "pending"))
    result = handle_refund("T-14")
    assert result == {"ok": False, "error": "cannot refund a pending order"}
