from . import dev
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
app.add_url_rule("/dev", view_func=dev.dev)
app.add_url_rule("/dev/api", view_func=dev.dev_api)
app.add_url_rule("/dev/click", view_func=dev.dev_click)
app.add_url_rule("/dev/colors", view_func=dev.dev_color)
app.add_url_rule("/dev/subscription/", view_func=dev.subscription, methods=['GET','POST'])


@app.route("/push_v1/",methods=['POST'])
def push_v1():
    message = "Push Test v1"
    #print("is_json",request.is_json)

    if not request.json or not request.json.get('sub_token'):
        return jsonify({'failed':1})

    #print("request.json",request.json)

    token = request.json.get('sub_token')
    try:
        token = json.loads(token)
        send_web_push(token, message)
        return jsonify({'success':1})
    except Exception as e:
        print("error",e)
        return jsonify({'failed':str(e)})


if __name__ == "__main__":
    app.run()
