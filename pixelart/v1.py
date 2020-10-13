from . import utils
from flask import Flask, render_template, send_file, jsonify, request
import redis
import random

r = redis.Redis(host='localhost', port=6379, db=0)
#@app.route("/v1")
def v1():
    template  = "index.v1.html" 
    array = []
    for i in range(0, 9999, 4):
        array.append(r.execute_command('bitfield test get u8 ' + str(8*i + 0))[0])
        array.append(r.execute_command('bitfield test get u8 ' + str(8*i + 8))[0])
        array.append(r.execute_command('bitfield test get u8 ' + str(8*i + 16))[0])
        array.append(r.execute_command('bitfield test get u8 ' + str(8*i + 24))[0])
    sqr = {'data': array, 'height': 50, 'width': 50}
    return render_template(template, sqr=sqr)
