"""Shared fixtures for the order test suite."""
from collections.abc import Iterator

import pytest

from orders import store


@pytest.fixture(autouse=True)
def reset_store() -> Iterator[None]:
    """Restore the in-memory store around every test.

    The store is a process-wide singleton, so without this each test would see
    the writes and in-place status changes left behind by the ones before it.
    """
    store.reset()
    yield
    store.reset()
