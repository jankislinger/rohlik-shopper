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


@app.route("/add_item/<string:item>", defaults={'amount': 1})
@app.route("/add_item/<string:item>/<int:amount>")
def add_item(item, amount):
    rohlik.add_item(item, add_amt=amount)
    return jsonify({"text": f"Successfully added {amount} {item}(s)."})


@app.route("/cart")
def cart():
    cart_items = rohlik.get_cart()
    return jsonify({"cart_items": cart_items})


if __name__ == "__main__":
    app.run(port=5000)
