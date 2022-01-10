import os

from dotenv import load_dotenv
from flask import Flask, jsonify

from rohlik import Rohlik

load_dotenv()

app = Flask(
    __name__,
)

rohlik = Rohlik(
    email=os.environ["ROHLIK_EMAIL"],
    password=os.environ["ROHLIK_PASSWORD"],
    headless=True,
)


@app.route("/")
def index():
    return jsonify({})


@app.route("/add_item/<string:item>/", defaults={'amount': 1})
@app.route("/add_item/<string:item>/<int:amount>")
def add_item(item, amount):
    rohlik.add_item(item, amount)
    return jsonify({"text": f"Successfully added {amount} {item}(s)."})


if __name__ == "__main__":
    try:
        app.run(port=5000)
    finally:
        rohlik.close()
