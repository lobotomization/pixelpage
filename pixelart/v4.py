from . import utils
from flask import Flask, render_template, send_file, jsonify, request
import redis
import random

r = redis.Redis(host='localhost', port=6379, db=0)
#@app.route("/v4")
def v4():
    template  = "index.v4.html" 
    array = []
    for i in range(0, 9999, 4):
        array.append(r.execute_command('bitfield test get u8 ' + str(8*i + 0))[0])
        array.append(r.execute_command('bitfield test get u8 ' + str(8*i + 8))[0])
        array.append(r.execute_command('bitfield test get u8 ' + str(8*i + 16))[0])
        array.append(255)
    sqr = {'data': array, 'height': 50, 'width': 50}
    return render_template(template, sqr=sqr)

#@app.route("/v4/api", methods=['GET'])
def v4_api():
    if 'ox' and 'oy' in request.args:
        ox = int(request.args['ox'])
        oy = int(request.args['oy'])
    else:
        return "Error: Missing 'ox' or 'oy' field. Please specify both ox and oy."

    array = []
    for y in range(oy, oy + 50):
        for x in range(ox, ox + 50):
            i = 32*utils.pixelpos(x, y, 50, 50) #32 bits per pixel
            array.append(r.execute_command('bitfield test get u8 ' + str(i + 0))[0])
            array.append(r.execute_command('bitfield test get u8 ' + str(i + 8))[0])
            array.append(r.execute_command('bitfield test get u8 ' + str(i + 16))[0])
            array.append(255)
    sqr = {'data': array, 'height': 50, 'width': 50}
    return jsonify(sqr)

