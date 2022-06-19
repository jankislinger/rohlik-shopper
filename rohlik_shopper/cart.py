import datetime
from typing import Dict, Optional, Tuple


class RohlikCart:
    """Class to represent items in a cart."""

    _items: Dict[int, dict]
    _last_update_time: Optional[datetime.datetime]

    def __init__(self):
        self._items = {}
        self._last_update_time = None

    def set_items(self, items) -> None:
        """Set items to specified value."""
        self._items = items
        self._last_update_time = datetime.datetime.now()

    def update_from_response(self, cart_data: dict) -> None:
        """Update items from a API response."""
        items = cart_data["data"].get("items", {})
        items = {int(k): v for k, v in items.items()}
        self.set_items(items)

    def get_product_status(self, product_id: int) -> Tuple[int, int]:
        """Get `item_order_id` and `quantity` of a product."""
        item = self._items[product_id]
        item_cart_id = item["orderFieldId"]
        quantity = item["quantity"]
        return item_cart_id, quantity

    @property
    def items(self) -> Dict[int, dict]:
        """Get items."""
        return self._items

    def is_valid(self, max_age_seconds: int) -> bool:
        """Check if cart is recent."""
        if self._last_update_time is None:
            return False
        max_age = datetime.timedelta(seconds=max_age_seconds)
        valid_until = self._last_update_time + max_age
        return datetime.datetime.now() <= valid_until
