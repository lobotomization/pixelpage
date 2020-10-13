from . import utils
from flask import Flask, render_template, send_file, jsonify, request
import redis
import random

r = redis.Redis(host='localhost', port=6379, db=0)
#@app.route("/v5")
def v5():
    template  = "index.v5.html" 
    return render_template(template)

#@app.route("/v5/api", methods=['GET'])
def v5_api():
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

#@app.route("/v5/click", methods=['GET'])
def v5_click():
    if 'ox' and 'oy' and 'clickx' and 'clicky' in request.args:
        ox = int(request.args['ox'])
        oy = int(request.args['oy'])
        clickx = int(request.args['clickx'])
        clicky = int(request.args['clicky'])
    else:
        return "Error: Missing 'ox', 'oy', 'clickx' or 'clicky' field. Please specify all four variables."

    array = []
    i = 32*utils.pixelpos(ox + clickx, oy + clicky, 50, 50) #32 bits per pixel
    array.append(r.execute_command('bitfield test get u8 ' + str(i + 0))[0])
    array.append(r.execute_command('bitfield test get u8 ' + str(i + 8))[0])
    array.append(r.execute_command('bitfield test get u8 ' + str(i + 16))[0])
    array.append(255)
    sqr = {'data': array, 'height': 1, 'width': 1}
    return jsonify(sqr)
