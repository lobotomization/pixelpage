from . import utils
from flask import Flask, render_template, send_file, jsonify, request
import redis
import random

#@app.route("/rando")
def rando():
    for i in range(0, 10000):
        r.execute_command('bitfield test set u8 ' + str(8*i) + ' ' + str(random.randint(0,255)))
    return "atchoo"

#@app.route("/unrando")
def unrando():
    for i in range(0, 10000):
        r.execute_command('bitfield test set u8 ' + str(8*i) + ' ' + str(i%256))
    return "atchoo"

#@app.route('/api/a')
def image():
    return send_file('/var/www/pixelart/pixelart/static/football.png',  mimetype='image/png')

#@app.route('/api/b')
def square():
    array = []
    for i in range(0, 9999, 4):
        array.append(random.randint(0, 255))
        array.append(random.randint(0, 255))
        array.append(random.randint(0, 255))
        array.append(255)
    return {'data': array, 'height': 50, 'width': 50}
