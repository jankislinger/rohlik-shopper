from flask import Flask, jsonify

from rohlik_shopper.client import RohlikClient
from rohlik_shopper.credentials import RohlikCredentials
from rohlik_shopper.session import RohlikSession

app = Flask(__name__)

credentials = RohlikCredentials.from_environ(use_dotenv=True)
session = RohlikSession()
rohlik = RohlikClient(credentials, session)


@app.route("/")
def index():
    return jsonify({})


@app.route("/add_item/<string:item_slug>/<int:qty>/<string:alias>")
def add_item(item_slug, qty, alias=None):
    # alias is deprecated
    item_id = int(item_slug.split("-", 1)[0])
    rohlik.add_items(item_id, qty)
    return jsonify({"text": "Successfully added item."})


@app.route("/set_item_qty/<string:item_slug>/<int:qty>/<string:alias>")
def set_item_qty(item_slug, qty, alias=None):
    # alias is deprecated
    item_id = int(item_slug.split("-", 1)[0])
    rohlik.add_items(item_id, qty)
    return jsonify({"text": "Successfully added set quantity."})


@app.route("/latest_update")
def latest_update():
    # deprecated
    return jsonify({"updated": False})


@app.route("/cart")
def cart():
    cart_items = list(rohlik.cart.items.values())
    return jsonify({"cart_items": cart_items})


if __name__ == "__main__":
    app.run(port=5000)
