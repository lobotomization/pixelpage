from . import utils
from flask import Flask, render_template, send_file, jsonify, request
import redis
import random

#@app.route("/v0")
def v0():
    template  = "index.v0.html" 
    array = []
    for i in range(0, 9999, 4):
        array.append(random.randint(0, 255))
        array.append(random.randint(0, 255))
        array.append(random.randint(0, 255))
        array.append(255)
    sqr = {'data': array, 'height': 50, 'width': 50}
    return render_template(template, sqr=sqr)
