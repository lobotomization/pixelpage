from . import stable
from . import misc

from . import utils
from flask import Flask, Response, render_template, send_file, jsonify, request
from pywebpush import webpush, WebPushException
import json, os, logging
import redis
import random
import sqlite3
import ast

r = redis.Redis(host='localhost', port=6379, db=0)
app = Flask(__name__)


app.add_url_rule("/rando", view_func=misc.rando)
app.add_url_rule("/unrando", view_func=misc.unrando)
app.add_url_rule("/api/a", view_func=misc.image)
app.add_url_rule("/api/b", view_func=misc.square)
app.add_url_rule("/", view_func=stable.stable)
app.add_url_rule("/stable/api", view_func=stable.stable_api)
app.add_url_rule("/stable/click", view_func=stable.stable_click)
app.add_url_rule("/stable/colors", view_func=stable.stable_color)

if __name__ == "__main__":
    app.run()
