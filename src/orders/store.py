"""In-memory order store. Stands in for a real database."""
from dataclasses import replace

from orders.models import Order

_SEED_ORDERS: tuple[Order, ...] = (
    Order("A-10422", "Ada Lovelace", 89.0, "shipped"),
    Order("A-10423", "Alan Turing", 42.5, "pending"),
)

_ORDERS: dict[str, Order] = {}


def fetch(order_id: str) -> Order | None:
    """Look up an order by id.

    Returns the stored Order, or None if no order has that id.
    """
    return _ORDERS.get(order_id)


def put(order: Order) -> None:
    """Insert or overwrite an order, keyed by its order_id.

    Existing entries with the same id are replaced.
    """
    _ORDERS[order.order_id] = order


def reset() -> None:
    """Discard all stored orders and restore the initial seed contents.

    Each seed order is rebuilt as a fresh copy, so in-place mutations made by
    earlier callers (a status change, say) do not survive the reset.
    """
    _ORDERS.clear()
    for order in _SEED_ORDERS:
        _ORDERS[order.order_id] = replace(order)


reset()
