from . import utils
from flask import Flask, Response, render_template, send_file, jsonify, request
import redis
import random
import colorsys
import ast
import json

r = redis.Redis(host='localhost', port=6379, db=0)
db = '/tmp/db.db'
max_height = 500
max_width = 500

con = utils.connect_db(db)

#@app.route("/dev", methods=['GET'])
def dev():
    utils.create_table(con)
    template  = "index.dev.html" 
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

#@app.route("/dev/api", methods=['GET'])
def dev_api():
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

    opixels = []
    for y in range(oy, oy + height):
        line    = []
        i = 4*utils.pixelpos(ox, y, 1000, 1000)
        line_o_pixels = r.execute_command('getrange ' + board + ' ' + str(i) + ' ' + str(i + 4*width - 1))
        #ba = bytearray(line_o_pixels)
        line.extend(line_o_pixels)
        while len(line) < 4*width:
            line.extend([255, 255, 255, 255])
        opixels.extend(line)
    sqr = {'data': opixels, 'height': height, 'width': width}
    return jsonify(sqr)

'''
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
            secox, secoy   = utils.sector(ox, oy, 1000, 1000)
            secoxw, secoyh = utils.sector(ox + width, oy + height, 1000, 1000)
            if secoxw - secox == 0 and secoyh - secoy == 0:
                utils.pixelpos(ox, oy, 1000, 1000)
                for y in range(oy, oy + height):

            if secoxw - secox == 0 and secoyh - secoy == 1:
                    
            if secoxw - secox == 1 and secoyh - secoy == 0:

            if secoxw - secox == 1 and secoyh - secoy == 1:


            i      = str(32*utils.diagpixelpos(x, y)) #32 bits per pixel
            start  = str(32*utils.diagpixelpos(ox, oy)) #32 bits per pixel
            end    = str(32*utils.diagpixelpos(ox + width-1, oy + height-1)) #32 bits per pixel 
            pixels = r.execute_command('getrange ' + quadrant + board + ' ' + start + ' '  + end)
            #rgb = r.execute_command('bitfield ' + quadrant + board + ' get u24 ' + i)[0]
            #blue = rgb%256
            #green = (rgb>>8)%256
            #red = (rgb>>16)%256
            array.extend([red, green, blue, 255])
'''


#@app.route("/dev/click", methods=['GET'])
def dev_click():
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
    i = 32*utils.pixelpos(ox + clickx, oy + clicky, 1000, 1000) #32 bits per pixel
    r.execute_command('bitfield ' + board + ' set u8 ' + str(i + 0 ) + ' ' + str(red))
    r.execute_command('bitfield ' + board + ' set u8 ' + str(i + 8 ) + ' ' + str(green))
    r.execute_command('bitfield ' + board + ' set u8 ' + str(i + 16) + ' ' + str(blue))
    r.execute_command('bitfield ' + board + ' set u8 ' + str(i + 24) + ' ' + str(opacity))
    sqr = {'data': array, 'height': 1, 'width': 1}
    for sub in utils.get_entries(con):
        subobj = ast.literal_eval(sub[0])
        utils.send_web_push(subobj, str(sqr))
    return jsonify(sqr)

#@app.route("/dev/colors", methods=['GET'])
def dev_color():
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

#@app.route("/dev/subscription/", methods=["GET", "POST"])
def subscription():
    """
        POST creates a subscription
        GET returns vapid public key which clients uses to send around push notification
    """

    if request.method == "GET":
        return Response(response=json.dumps({"public_key": utils.VAPID_PUBLIC_KEY}),
            headers={"Access-Control-Allow-Origin": "*"}, content_type="application/json")

    subscription_token = request.get_json("subscription_token")
    utils.insert_entry(con, subscription_token)
    return Response(status=201, mimetype="application/json")

