import datetime

from rohlik_shopper.cart import RohlikCart
from rohlik_shopper.credentials import RohlikCredentials
from rohlik_shopper.session import RohlikSession


class RohlikClient:
    """Class with abstraction of manipulation with items."""

    def __init__(self, credentials: RohlikCredentials, session: RohlikSession):
        self._credentials = credentials
        self._session = session
        self._last_login = None
        self._product_cache = {}
        self._cart = RohlikCart()

    def login(self):
        """Log into a server."""
        self._session.post("login", self._credentials.to_dict())
        self._last_login = datetime.datetime.now()

    def add_items(self, product_id: int, quantity: int):
        """Add items to a cart.

        Adds specified quantity of a product regardless current state of the cart.
        """
        self._update_cart()

        if product_id not in self._cart.items:
            self._add_new_items_to_cart(product_id, quantity)
            return

        item_cart_id, current_quantity = self._cart.get_product_status(product_id)
        self._update_item_quantity_in_cart(item_cart_id, quantity + current_quantity)

    def set_quantity(self, product_id: int, quantity: int, increase_only: bool = False) -> int:
        """Set quantity in a cart.

        Adds or removes items from the cart to match required quantity. If
        `increase_only` is set to `True` items are not removed.
        """
        self._update_cart()

        if product_id not in self._cart.items:
            self._add_new_items_to_cart(product_id, quantity)
            return quantity

        item_cart_id, current_quantity = self._cart.get_product_status(product_id)
        if current_quantity == quantity or (increase_only and current_quantity > quantity):
            return 0
        self._update_item_quantity_in_cart(item_cart_id, quantity)
        return quantity - current_quantity

    def search(self, query: str):
        params = {
            "search": query,
            "referer": "whisperer",
            "companyId":1,
        }
        return self._session.get("autocomplete", params)

    @property
    def cart(self):
        """Get cart object."""
        if not self._cart.is_valid(max_age_seconds=5):
            self._update_cart()
        return self._cart

    def _add_new_items_to_cart(self, product_id: int, quantity: int):
        category = self._product_category(product_id)
        data = {
            "productId": product_id,
            "quantity": quantity,
            "source": f"true:ProductCategory:{category}",
            "actionId": None,
            "recipeId": None,
        }
        response = self._session.post("v2/cart", json=data)
        self._cart.update_from_response(response)

    def _update_item_quantity_in_cart(self, cart_item_id: int, quantity: int):
        data = {"cartItemId": cart_item_id, "quantity": quantity}
        response = self._session.put("v2/cart", json=data)
        self._cart.update_from_response(response)

    def _update_cart(self):
        cart_data = self._session.get("v2/cart")
        self._cart.update_from_response(cart_data)

    def _product_category(self, product_id: int) -> str:
        detail = self._product_detail(product_id)
        return detail["product"]["categories"][-1]["id"]

    def _product_detail(self, product_id: int) -> dict:
        if product_id not in self._product_cache:
            response = self._session.get(f"product/{product_id}/full?preview=false")
            self._product_cache[product_id] = response["data"]
        return self._product_cache[product_id]
