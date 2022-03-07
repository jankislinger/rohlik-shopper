import datetime
import functools
import os

import requests

BASE_URL = "https://www.rohlik.cz"
FRONTEND_SERVICE = f"{BASE_URL}/services/frontend-service"
LOGIN_URL = f"{FRONTEND_SERVICE}/login"
URL_CART = f"{FRONTEND_SERVICE}/v2/cart"

LOGIN_TTL = datetime.timedelta(minutes=30)
CART_CACHE_TTL = datetime.timedelta(minutes=5)

SCREENSHOTS_URL = os.environ.get("SCREENSHOTS_URL", "screenshots")


class Rohlik:
    def __init__(self, email, password):
        self._email = email
        self._password = password
        self._last_login = None

        self._session = requests.Session()

        self._cart_items = None
        self._cart_items_last_update = None

        self._login()

    def add_item(self, slug, qty=None):
        item_id = int(slug.split("-")[0])
        self._update_cart(force=True)

        if item_id not in self._cart_items:
            self._add_item_to_cart(item_id, qty)
            return

        current_qty = self._cart_items[item_id]["quantity"]
        target_qty = current_qty + qty
        self._update_item_qty_in_cart(item_id, target_qty),

    def set_item_qty(self, item_slug: str, qty: int):
        item_id = int(item_slug.split("-", 1)[0])
        self._update_cart(force=True)

        if item_id not in self._cart_items:
            self._add_item_to_cart(item_id, qty)
            return

        current_qty = self._cart_items[item_id]["quantity"]
        if current_qty >= qty:
            return

        self._update_item_qty_in_cart(item_id, qty),

    def get_cart(self):
        # TODO: not force if used for periodical update
        self._update_cart(force=False)
        return list(self._cart_items.values())

    def _login(self):
        data = {"email": self._email, "password": self._password, "name": ""}
        response = self._session.post(LOGIN_URL, json=data)
        response.raise_for_status()
        # TODO: save number of express & unlimited orders
        self._last_login = datetime.datetime.now()

    def _ensure_logged_in(self):
        if timestamp_is_recent(self._last_login, LOGIN_TTL):
            # recently logged in
            return
        # TODO: checked if logged in via api
        self._login()

    def _update_cart(self, force):
        if not force and timestamp_is_recent(self._cart_items_last_update, CART_CACHE_TTL):
            print("Cart should be up-to-date")
            return

        self._ensure_logged_in()
        response = self._session.get(URL_CART)
        if response.status_code != 200:
            print(response.status_code)
            print(response.text)
        response.raise_for_status()
        self._update_cart_from_response(response.json())

    def _update_cart_from_response(self, response):
        cart_items = response["data"].get("items", {})
        self._cart_items = {int(k): v for k, v in cart_items.items()}
        self._cart_items_last_update = datetime.datetime.now()

    def _update_item_qty_in_cart(self, item_id, qty):
        # assumes updated cart & item in cart
        data = {
            "cartItemId": self._cart_items[item_id]["orderFieldId"],
            "quantity": qty,
        }
        response = self._session.put(URL_CART, json=data)
        response.raise_for_status()
        self._update_cart_from_response(response.json())

    def _add_item_to_cart(self, item_id, qty):
        # assumes updated cart
        data = {
            "productId": item_id,
            "quantity": qty,
            "source": f"true:ProductCategory:{get_product_category(item_id)}",
            "actionId": None,
            "recipeId": None
        }
        response = self._session.post(URL_CART, json=data)
        response.raise_for_status()
        self._update_cart_from_response(response.json())


def timestamp_is_recent(timestamp, max_delay):
    if timestamp is None:
        return False
    return timestamp + max_delay >= datetime.datetime.now()


@functools.lru_cache
def get_product_category(product_id):
    url = f"{FRONTEND_SERVICE}/product/{product_id}/full?preview=false"
    response = requests.get(url)
    if response.status_code != 200:
        print(response.text)
    response.raise_for_status()
    response = response.json()
    return response["data"]["product"]["categories"][-1]["id"]
