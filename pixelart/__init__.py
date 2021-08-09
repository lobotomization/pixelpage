from . import v11
from . import v10
from . import misc

from . import utils
from flask import Flask, render_template, send_file, jsonify, request
import redis
import random

r = redis.Redis(host='localhost', port=6379, db=0)
app = Flask(__name__)


app.add_url_rule("/rando", view_func=misc.rando)
app.add_url_rule("/unrando", view_func=misc.unrando)
app.add_url_rule("/api/a", view_func=misc.image)
app.add_url_rule("/api/b", view_func=misc.square)
app.add_url_rule("/", view_func=v10.v10)
app.add_url_rule("/v10/api", view_func=v10.v10_api)
app.add_url_rule("/v10/click", view_func=v10.v10_click)
app.add_url_rule("/v10/colors", view_func=v10.v10_color)
app.add_url_rule("/dev", view_func=v11.v11)
app.add_url_rule("/v11/api", view_func=v11.v11_api)
app.add_url_rule("/v11/click", view_func=v11.v11_click)
app.add_url_rule("/v11/colors", view_func=v11.v11_color)



if __name__ == "__main__":
    app.run()
