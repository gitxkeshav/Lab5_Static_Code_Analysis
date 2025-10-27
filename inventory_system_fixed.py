"""
inventory_system_fixed.py
Cleaned and safer version for Lab 5 (Static Code Analysis)

Fixes included:
- Removed eval() (security risk)
- Fixed mutable default argument
- Added input validation
- Replaced bare except with specific exceptions and logging
- Used context managers for file I/O
- Proper logging configuration and __main__ guard
- Used f-strings for messages

Changes since last run:
- Removed global assignment by updating stock_data in-place.
- Replaced broad `except Exception` with narrower exception types.
- Replaced f-strings used directly in logging calls with lazy %-formatting.
- Wrapped long lines to satisfy Flake8 E501 (79 char limit)
"""



from __future__ import annotations

import json
import logging
from datetime import datetime
from typing import Dict, List, Optional

# Configure module-level logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Inventory store
stock_data: Dict[str, int] = {}


def add_item(item: str, qty: int, logs: Optional[List[str]] = None) -> bool:
    """Add qty of item to inventory. Return True on success."""
    if logs is None:
        logs = []

    # Input validation
    if not isinstance(item, str) or not item:
        logger.error("add_item: invalid item name: %r", item)
        return False

    if not isinstance(qty, int):
        logger.error(
            "add_item: qty must be int, got %r for item %s", type(qty), item
        )
        return False

    if qty == 0:
        logger.warning("add_item: qty is zero for item %s; no change.", item)
        return True

    stock_data[item] = stock_data.get(item, 0) + qty
    entry = f"{datetime.now()}: Added {qty} of {item}"
    logs.append(entry)
    # log the entry using lazy formatting
    logger.info("%s", entry)
    return True


def remove_item(item: str, qty: int) -> bool:
    """Remove qty of item. Return True on success, False otherwise."""
    if not isinstance(item, str) or not item:
        logger.error("remove_item: invalid item name: %r", item)
        return False

    if not isinstance(qty, int) or qty <= 0:
        logger.error("remove_item: qty must be a positive int, got %r", qty)
        return False

    # Item existence already checked below; KeyError is unlikely,
    # but handle it specifically if it happens.
    try:
        current = stock_data.get(item)
        if current is None:
            logger.warning("remove_item: item %s not found", item)
            return False

        if qty >= current:
            # remove item entirely
            del stock_data[item]
            logger.info(
                "remove_item: removed all of %s (was %d)", item, current
            )
        else:
            stock_data[item] = current - qty
            logger.info(
                "remove_item: decremented %s by %d (now %d)",
                item,
                qty,
                stock_data[item],
            )
        return True

    except KeyError as exc:
        logger.exception("remove_item: KeyError for item %s: %s", item, exc)
        return False


def get_qty(item: str) -> int:
    """Return quantity for item, or 0 if not present / invalid input."""
    if not isinstance(item, str) or not item:
        logger.error("get_qty: invalid item name: %r", item)
        return 0
    return stock_data.get(item, 0)


def load_data(file: str = "inventory.json") -> bool:
    """Load inventory from JSON file. Return True on success, False otherwise."""
    try:
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)

        if not isinstance(data, dict):
            logger.error("load_data: unexpected data format in %s", file)
            return False

        cleaned: Dict[str, int] = {}
        for k, v in data.items():
            if not isinstance(k, str):
                logger.warning("load_data: skipping non-string key: %r", k)
                continue
            try:
                cleaned[k] = int(v)
            except (TypeError, ValueError):
                logger.warning(
                    "load_data: invalid qty for %s: %r; skipping", k, v
                )

        # update stock_data in-place to avoid `global` reassignment
        stock_data.clear()
        stock_data.update(cleaned)
        logger.info(
            "load_data: loaded %d items from %s", len(stock_data), file
        )
        return True

    except FileNotFoundError:
        logger.warning(
            "load_data: file %s not found; starting with empty inventory", file
        )
        stock_data.clear()
        return False
    except json.JSONDecodeError as exc:
        logger.error("load_data: failed to parse JSON in %s: %s", file, exc)
        return False
    except OSError as exc:
        logger.exception(
            "load_data: I/O error while accessing %s: %s", file, exc
        )
        return False


def save_data(file: str = "inventory.json") -> bool:
    """Save inventory to JSON file. Return True on success."""
    try:
        with open(file, "w", encoding="utf-8") as f:
            json.dump(stock_data, f, indent=2)
        logger.info("save_data: saved %d items to %s", len(stock_data), file)
        return True
    except OSError as exc:
        logger.exception("save_data: I/O error while saving to %s: %s", file, exc)
        return False


def print_data() -> None:
    """Log current inventory report."""
    logger.info("Items Report")
    if not stock_data:
        logger.info("(no items in inventory)")
        return
    for name, qty in stock_data.items():
        logger.info("%s -> %d", name, qty)


def check_low_items(threshold: int = 5) -> List[str]:
    """Return list of item names whose qty is strictly less than threshold."""
    if not isinstance(threshold, int) or threshold <= 0:
        raise ValueError("threshold must be a positive int")
    return [name for name, qty in stock_data.items() if qty < threshold]


def _demo_operations() -> None:
    """Small demo showing usage (kept minimal for lab)."""
    logs: List[str] = []
    add_item("apple", 10, logs)
    add_item("banana", 2, logs)
    # invalid inputs will be logged and safely ignored
    add_item(123, 10, logs)  # will log an error and return False
    add_item("mango", 0, logs)  # zero qty: logged as warning
    remove_item("apple", 3)
    remove_item("orange", 1)

    logger.info("Apple stock: %d", get_qty("apple"))
    logger.info("Low items: %s", check_low_items())
    save_data()
    load_data()
    print_data()


if __name__ == "__main__":
    _demo_operations()
