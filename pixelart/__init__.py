from . import v10
from . import v9
from . import v8
from . import v7
from . import v6
from . import v5
from . import v4
from . import v3
from . import v2
from . import v1
from . import v0
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
app.add_url_rule("/v0", view_func=v0.v0)
app.add_url_rule("/v1", view_func=v1.v1)
app.add_url_rule("/v2", view_func=v2.v2)
app.add_url_rule("/v3", view_func=v3.v3)
app.add_url_rule("/v4", view_func=v4.v4)
app.add_url_rule("/v4/api", view_func=v4.v4_api)
app.add_url_rule("/v5", view_func=v5.v5)
app.add_url_rule("/v5/api", view_func=v5.v5_api)
app.add_url_rule("/v5/click", view_func=v5.v5_click)
app.add_url_rule("/v6", view_func=v6.v6)
app.add_url_rule("/v6/api", view_func=v6.v6_api)
app.add_url_rule("/v6/click", view_func=v6.v6_click)
app.add_url_rule("/v7", view_func=v7.v7)
app.add_url_rule("/v7/api", view_func=v7.v7_api)
app.add_url_rule("/v7/click", view_func=v7.v7_click)
app.add_url_rule("/v8", view_func=v8.v8)
app.add_url_rule("/v8/api", view_func=v8.v8_api)
app.add_url_rule("/v8/click", view_func=v8.v8_click)
app.add_url_rule("/v8/colors", view_func=v8.v8_color)
app.add_url_rule("/v9", view_func=v9.v9)
app.add_url_rule("/v9/api", view_func=v9.v9_api)
app.add_url_rule("/v9/click", view_func=v9.v9_click)
app.add_url_rule("/v9/colors", view_func=v9.v9_color)
app.add_url_rule("/v10", view_func=v10.v10)
app.add_url_rule("/v10/api", view_func=v10.v10_api)
app.add_url_rule("/v10/click", view_func=v10.v10_click)
app.add_url_rule("/v10/colors", view_func=v10.v10_color)



if __name__ == "__main__":
    app.run()
