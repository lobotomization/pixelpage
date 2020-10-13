from . import utils
from flask import Flask, render_template, send_file, jsonify, request
import redis
import random

r = redis.Redis(host='localhost', port=6379, db=0)
#@app.route("/v7", methods=['GET'])
def v7():
    template  = "index.v7.html" 
    if 'board' not in request.args:
        board = 'test';
    else:
        board = str(request.args['board'])
    if not board.isalpha():
        return "Error: Board name is not alphabetical"
    return render_template(template, board=board)

#@app.route("/v7/api", methods=['GET'])
def v7_api():
    if 'ox' and 'oy' and 'board' in request.args:
        ox    = int(request.args['ox'])
        oy    = int(request.args['oy'])
        board = str(request.args['board'])
    elif not board.isalpha():
        return "Error: Board name is not alphabetical"
    else:
        return "Error: Missing 'ox', 'oy' or 'board' field. Please specify all variables."

    array = []
    for y in range(oy, oy + 50):
        for x in range(ox, ox + 50):
            i = 32*utils.pixelpos(x, y, 50, 50) #32 bits per pixel

            array.append(r.execute_command('bitfield ' + board + ' get u8 ' + str(i + 0))[0])
            array.append(r.execute_command('bitfield ' + board + ' get u8 ' + str(i + 8))[0])
            array.append(r.execute_command('bitfield ' + board + ' get u8 ' + str(i + 16))[0])
            array.append(255)
    sqr = {'data': array, 'height': 50, 'width': 50}
    return jsonify(sqr)

#@app.route("/v7/click", methods=['GET'])
def v7_click():
    if 'ox' and 'oy' and 'board' and 'clickx' and 'clicky' in request.args:
        ox = int(request.args['ox'])
        oy = int(request.args['oy'])
        board = str(request.args['board'])
        clickx = int(request.args['clickx'])
        clicky = int(request.args['clicky'])
    elif not board.isalpha():
        return "Error: Board name is not alphabetical"
    else:
        return "Error: Missing 'ox', 'oy', 'board', 'clickx' or 'clicky' field. Please specify all four variables."
    if 'rclick' in request.args:
        color = ' 0'
    else:
        color = ' 255'
    opacity = ' 255'
    array = []
    i = 32*utils.pixelpos(ox + clickx, oy + clicky, 50, 50) #32 bits per pixel
    r.execute_command('bitfield ' + board + ' set u8 ' + str(i + 0 ) + color)
    r.execute_command('bitfield ' + board + ' set u8 ' + str(i + 8 ) + color)
    r.execute_command('bitfield ' + board + ' set u8 ' + str(i + 16) + color)
    r.execute_command('bitfield ' + board + ' set u8 ' + str(i + 24) + opacity)
    array.append(r.execute_command('bitfield ' + board + ' get u8 ' + str(i + 0))[0])
    array.append(r.execute_command('bitfield ' + board + ' get u8 ' + str(i + 8))[0])
    array.append(r.execute_command('bitfield ' + board + ' get u8 ' + str(i + 16))[0])
    array.append(255)
    sqr = {'data': array, 'height': 1, 'width': 1}
    return jsonify(sqr)
