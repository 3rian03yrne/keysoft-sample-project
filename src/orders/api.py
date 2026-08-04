"""HTTP-style request handlers for the order service."""
import logging

from orders import store
from orders.service import cancel_order, refund_order

logger = logging.getLogger(__name__)


def handle_get_order(order_id: str) -> dict:
    """Look up an order and return it as a plain dict.

    Returns an empty dict if the order is unknown.
    """
    order = store.get(order_id)
    if order is None:
        return {}
    return {"order_id": order.order_id, "status": order.status, "total_usd": order.total_usd}


def handle_cancel_order(order_id: str) -> dict:
    """Cancel an order and return a structured result dict.

    Returns {"ok": False, "error": ...} if the order is unknown or can't be cancelled.
    """
    try:
        order = cancel_order(order_id)
    except (KeyError, ValueError) as e:
        logger.error("cancel failed: %s", e)
        return {"ok": False, "error": str(e)}
    return {"ok": True, "order_id": order.order_id, "status": order.status}


def handle_refund(order_id: str) -> dict:
    """Refund an order and return a structured result dict.

    Returns {"ok": False, "error": ...} if the order is unknown or can't be refunded.
    """
    try:
        order = refund_order(order_id)
    except (KeyError, ValueError) as e:
        logger.error("refund failed: %s", e)
        return {"ok": False, "error": str(e)}
    return {"ok": True, "order_id": order.order_id, "status": order.status}
