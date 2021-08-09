from . import utils
from flask import Flask, render_template, send_file, jsonify, request
import redis
import random
import colorsys

r = redis.Redis(host='localhost', port=6379, db=0)

max_height = 100
max_width = 100

#@app.route("/stable", methods=['GET'])
def stable():
    template  = "index.stable.html" 
    board = 'test'
    scale = 16
    width = 50
    height = 50
    if 'board' in request.args:
        board = str(request.args['board'])
    if not board.isalpha():
        return "Error: Board name is not alphabetical"
    if 'zoom' in request.args:
        scale = int(request.args['zoom'])
    if 'width' in request.args:
        width = int(request.args['width'])
        if width > max_width:
            width = max_width
    if 'height' in request.args:
        height = int(request.args['height'])
        if height > max_height:
            height = max_height

    size = {'width':width*scale, 'height':height*scale}
    return render_template(template, board=board, size=size, scale=scale, width=width, height=height)

#@app.route("/stable/api", methods=['GET'])
def stable_api():
    if 'ox' and 'oy' and 'board' and 'width' and 'height' in request.args:
        ox     = int(request.args['ox'])
        oy     = int(request.args['oy'])
        board  = str(request.args['board'])
        height = int(request.args['height'])
        width  = int(request.args['width'])
    elif not board.isalpha():
        return "Error: Board name is not alphabetical"
    else:
        return "Error: Missing a field. Please specify all variables."

    if width > max_width:
        width = max_width

    if height > max_height:
        height = max_height

    array = []
    for y in range(oy, oy + height):
        for x in range(ox, ox + width):
            if x > 0 and y >= 0:
                quadrant = '1'
            elif x <= 0 and y > 0:
                quadrant = '2'
            elif x < 0 and y <= 0:
                quadrant = '3'
            elif x >= 0 and y < 0:
                quadrant = '4'
            else:
                quadrant = '1'

            i = 32*utils.diagpixelpos(x, y) #32 bits per pixel

            array.append(r.execute_command('bitfield ' + quadrant + board + ' get u8 ' + str(i + 0))[0])
            array.append(r.execute_command('bitfield ' + quadrant + board + ' get u8 ' + str(i + 8))[0])
            array.append(r.execute_command('bitfield ' + quadrant + board + ' get u8 ' + str(i + 16))[0])
            array.append(255)
    sqr = {'data': array, 'height': height, 'width': width}
    return jsonify(sqr)

#@app.route("/stable/click", methods=['GET'])
def stable_click():
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
    red = int(request.args['r'])
    green = int(request.args['g'])
    blue = int(request.args['b'])
    opacity = 255
    array = [red, green, blue, opacity]
    if ox + clickx > 0 and oy + clicky >= 0:
        quadrant = '1'
    elif ox + clickx <= 0 and oy + clicky > 0:
        quadrant = '2'
    elif ox + clickx < 0 and oy + clicky <= 0:
        quadrant = '3'
    elif ox + clickx >= 0 and oy + clicky < 0:
        quadrant = '4'
    else:
        quadrant = '1'
    i = 32*utils.diagpixelpos(ox + clickx, oy + clicky) #32 bits per pixel
    r.execute_command('bitfield ' + quadrant + board + ' set u8 ' + str(i + 0 ) + ' ' + str(red))
    r.execute_command('bitfield ' + quadrant + board + ' set u8 ' + str(i + 8 ) + ' ' + str(green))
    r.execute_command('bitfield ' + quadrant + board + ' set u8 ' + str(i + 16) + ' ' + str(blue))
    r.execute_command('bitfield ' + quadrant + board + ' set u8 ' + str(i + 24) + ' ' + str(opacity))
    sqr = {'data': array, 'height': 1, 'width': 1}
    return jsonify(sqr)

#@app.route("/stable/colors", methods=['GET'])
def stable_color():
    gridsize = 100
    values = [0, 51, 102, 153, 204, 255]
    colors = []
    for a in range(0, gridsize):
        for b in range(0, gridsize):
            col = colorsys.hls_to_rgb(a/gridsize, b/gridsize, 1)
            colors.append(int(255*col[0]))
            colors.append(int(255*col[1]))
            colors.append(int(255*col[2]))
            colors.append(255)
    #colors = [140,30,44,255,220,68,60,255,255,140,102,255,199,91,56,255,214,111,36,255,228,186,50,255,33,145,59,255,131,181,53,255,235,213,189,255,102,195,217,255,56,124,238,255,53,57,162,255,153,141,162,255,89,78,111,255,43,26,75,255,8,5,14,255]
    if 'clickx' and 'clicky' in request.args:
        clickx = int(request.args['clickx'])
        clicky = int(request.args['clicky'])
    else:
        return jsonify({'data': colors, 'height': gridsize, 'width': gridsize})
    if 'rclick' in request.args:
        rclick = 1
    else:
        rclick = 0
    pos = 4*utils.pixelpos(clickx, clicky, gridsize, gridsize) # Four entries per pixel
    return jsonify({'data': colors[pos:pos+4], 'height': 1, 'width': 1, 'rclick': rclick})
