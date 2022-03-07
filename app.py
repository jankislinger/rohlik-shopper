import os

from flask import Flask, jsonify

from rohlik import Rohlik

if "ROHLIK_EMAIL" not in os.environ:
    from dotenv import load_dotenv
    load_dotenv()

app = Flask(__name__)

rohlik = Rohlik(
    email=os.environ["ROHLIK_EMAIL"],
    password=os.environ["ROHLIK_PASSWORD"],
)


@app.route("/")
def index():
    return jsonify({})


@app.route("/add_item/<string:item_slug>/<int:qty>/<string:alias>")
def add_item(item_slug, qty, alias):
    rohlik.add_item(item_slug, qty, alias)
    return jsonify({"text": "Successfully added item."})


@app.route("/set_item_qty/<string:item_slug>/<int:qty>/<string:alias>")
def set_item_qty(item_slug, qty, alias):
    rohlik.set_item_qty(item_slug, qty, alias)
    return jsonify({"text": "Successfully added set quantity."})


@app.route("/latest_update")
def latest_update():
    return jsonify(rohlik.get_latest_update())


@app.route("/cart")
def cart():
    cart_items = rohlik.get_cart()
    return jsonify({"cart_items": cart_items})


if __name__ == "__main__":
    app.run(port=5000)
