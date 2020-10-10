from flask import Flask, render_template, send_file, jsonify, request
import redis
import random
r = redis.Redis(host='localhost', port=6379, db=0)
app = Flask(__name__)


def pixelpos(x, y, arrX, arrY):
    return (arrX*(y%arrY) + (x%arrX))%(arrX*arrY)

@app.route("/rando")
def rando():
    for i in range(0, 10000):
        r.execute_command('bitfield test set u8 ' + str(8*i) + ' ' + str(random.randint(0,255)))
    return "atchoo"

@app.route("/unrando")
def unrando():
    for i in range(0, 10000):
        r.execute_command('bitfield test set u8 ' + str(8*i) + ' ' + str(i%256))
    return "atchoo"

@app.route('/api/a')
def image():
    return send_file('/var/www/pixelart/pixelart/static/football.png',  mimetype='image/png')

@app.route('/api/b')
def square():
    array = []
    for i in range(0, 9999, 4):
        array.append(random.randint(0, 255))
        array.append(random.randint(0, 255))
        array.append(random.randint(0, 255))
        array.append(255)
    return {'data': array, 'height': 50, 'width': 50}

@app.route("/v0")
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


@app.route("/v1")
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

@app.route("/v2")
def v2():
    template  = "index.v2.html" 
    array = []
#    for i in range(0, 10000):
#        array.append(r.execute_command('bitfield test get u4 ' + str(4*i))[0])
    for i in range(0, 9999, 4):
        array.append(r.execute_command('bitfield test get u8 ' + str(8*i + 0))[0])
        array.append(r.execute_command('bitfield test get u8 ' + str(8*i + 8))[0])
        array.append(r.execute_command('bitfield test get u8 ' + str(8*i + 16))[0])
        array.append(255)
    sqr = {'data': array, 'height': 50, 'width': 50}
    return render_template(template, sqr=sqr)

@app.route("/v3")
def v3():
    template  = "index.v3.html" 
    array = []
    for i in range(0, 9999, 4):
        array.append(r.execute_command('bitfield test get u8 ' + str(8*i + 0))[0])
        array.append(r.execute_command('bitfield test get u8 ' + str(8*i + 8))[0])
        array.append(r.execute_command('bitfield test get u8 ' + str(8*i + 16))[0])
        array.append(255)
    sqr = {'data': array, 'height': 50, 'width': 50}
    return render_template(template, sqr=sqr)

@app.route("/v4")
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

@app.route("/v4/api", methods=['GET'])
def v4_api():
    if 'ox' and 'oy' in request.args:
        ox = int(request.args['ox'])
        oy = int(request.args['oy'])
    else:
        return "Error: Missing 'ox' or 'oy' field. Please specify both ox and oy."

    array = []
    for y in range(oy, oy + 50):
        for x in range(ox, ox + 50):
            i = 32*pixelpos(x, y, 50, 50) #32 bits per pixel
            array.append(r.execute_command('bitfield test get u8 ' + str(i + 0))[0])
            array.append(r.execute_command('bitfield test get u8 ' + str(i + 8))[0])
            array.append(r.execute_command('bitfield test get u8 ' + str(i + 16))[0])
            array.append(255)
    sqr = {'data': array, 'height': 50, 'width': 50}
    return jsonify(sqr)


@app.route("/v5")
def v5():
    template  = "index.v5.html" 
    return render_template(template)

@app.route("/v5/api", methods=['GET'])
def v5_api():
    if 'ox' and 'oy' in request.args:
        ox = int(request.args['ox'])
        oy = int(request.args['oy'])
    else:
        return "Error: Missing 'ox' or 'oy' field. Please specify both ox and oy."

    array = []
    for y in range(oy, oy + 50):
        for x in range(ox, ox + 50):
            i = 32*pixelpos(x, y, 50, 50) #32 bits per pixel
            array.append(r.execute_command('bitfield test get u8 ' + str(i + 0))[0])
            array.append(r.execute_command('bitfield test get u8 ' + str(i + 8))[0])
            array.append(r.execute_command('bitfield test get u8 ' + str(i + 16))[0])
            array.append(255)
    sqr = {'data': array, 'height': 50, 'width': 50}
    return jsonify(sqr)

@app.route("/v5/click", methods=['GET'])
def v5_click():
    if 'ox' and 'oy' and 'clickx' and 'clicky' in request.args:
        ox = int(request.args['ox'])
        oy = int(request.args['oy'])
        clickx = int(request.args['clickx'])
        clicky = int(request.args['clicky'])
    else:
        return "Error: Missing 'ox', 'oy', 'clickx' or 'clicky' field. Please specify all four variables."

    array = []
    i = 32*pixelpos(ox + clickx, oy + clicky, 50, 50) #32 bits per pixel
    array.append(r.execute_command('bitfield test get u8 ' + str(i + 0))[0])
    array.append(r.execute_command('bitfield test get u8 ' + str(i + 8))[0])
    array.append(r.execute_command('bitfield test get u8 ' + str(i + 16))[0])
    array.append(255)
    sqr = {'data': array, 'height': 1, 'width': 1}
    return jsonify(sqr)

@app.route("/v6")
def v6():
    template  = "index.v6.html" 
    return render_template(template)

@app.route("/v6/api", methods=['GET'])
def v6_api():
    if 'ox' and 'oy' in request.args:
        ox = int(request.args['ox'])
        oy = int(request.args['oy'])
    else:
        return "Error: Missing 'ox' or 'oy' field. Please specify both ox and oy."

    array = []
    for y in range(oy, oy + 50):
        for x in range(ox, ox + 50):
            i = 32*pixelpos(x, y, 50, 50) #32 bits per pixel
            array.append(r.execute_command('bitfield test get u8 ' + str(i + 0))[0])
            array.append(r.execute_command('bitfield test get u8 ' + str(i + 8))[0])
            array.append(r.execute_command('bitfield test get u8 ' + str(i + 16))[0])
            array.append(255)
    sqr = {'data': array, 'height': 50, 'width': 50}
    return jsonify(sqr)

@app.route("/v6/click", methods=['GET'])
def v6_click():
    if 'ox' and 'oy' and 'clickx' and 'clicky' in request.args:
        ox = int(request.args['ox'])
        oy = int(request.args['oy'])
        clickx = int(request.args['clickx'])
        clicky = int(request.args['clicky'])
    else:
        return "Error: Missing 'ox', 'oy', 'clickx' or 'clicky' field. Please specify all four variables."

    array = []
    i = 32*pixelpos(ox + clickx, oy + clicky, 50, 50) #32 bits per pixel
    r.execute_command('bitfield test set u8 ' + str(i + 0) + ' 0')
    r.execute_command('bitfield test set u8 ' + str(i + 8) + ' 0')
    r.execute_command('bitfield test set u8 ' + str(i + 16) + ' 0')
    r.execute_command('bitfield test set u8 ' + str(i + 24) + ' 255')
    array.append(r.execute_command('bitfield test get u8 ' + str(i + 0))[0])
    array.append(r.execute_command('bitfield test get u8 ' + str(i + 8))[0])
    array.append(r.execute_command('bitfield test get u8 ' + str(i + 16))[0])
    array.append(255)
    sqr = {'data': array, 'height': 1, 'width': 1}
    return jsonify(sqr)

@app.route("/v7", methods=['GET'])
def v7():
    template  = "index.v7.html" 
    if 'board' not in request.args:
        board = 'test';
    else:
        board = str(request.args['board'])
    if not board.isalpha():
        return "Error: Board name is not alphabetical"
    return render_template(template, board=board)

@app.route("/v7/api", methods=['GET'])
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
            i = 32*pixelpos(x, y, 50, 50) #32 bits per pixel

            array.append(r.execute_command('bitfield ' + board + ' get u8 ' + str(i + 0))[0])
            array.append(r.execute_command('bitfield ' + board + ' get u8 ' + str(i + 8))[0])
            array.append(r.execute_command('bitfield ' + board + ' get u8 ' + str(i + 16))[0])
            array.append(255)
    sqr = {'data': array, 'height': 50, 'width': 50}
    return jsonify(sqr)

@app.route("/v7/click", methods=['GET'])
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
    i = 32*pixelpos(ox + clickx, oy + clicky, 50, 50) #32 bits per pixel
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

@app.route("/v8", methods=['GET'])
def v8():
    template  = "index.v8.html" 
    if 'board' not in request.args:
        board = 'test';
    else:
        board = str(request.args['board'])
    if not board.isalpha():
        return "Error: Board name is not alphabetical"
    return render_template(template, board=board)

@app.route("/v8/api", methods=['GET'])
def v8_api():
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
            i = 32*pixelpos(x, y, 50, 50) #32 bits per pixel

            array.append(r.execute_command('bitfield ' + board + ' get u8 ' + str(i + 0))[0])
            array.append(r.execute_command('bitfield ' + board + ' get u8 ' + str(i + 8))[0])
            array.append(r.execute_command('bitfield ' + board + ' get u8 ' + str(i + 16))[0])
            array.append(255)
    sqr = {'data': array, 'height': 50, 'width': 50}
    return jsonify(sqr)

@app.route("/v8/click", methods=['GET'])
def v8_click():
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
    i = 32*pixelpos(ox + clickx, oy + clicky, 50, 50) #32 bits per pixel
    r.execute_command('bitfield ' + board + ' set u8 ' + str(i + 0 ) + ' ' + str(red))
    r.execute_command('bitfield ' + board + ' set u8 ' + str(i + 8 ) + ' ' + str(green))
    r.execute_command('bitfield ' + board + ' set u8 ' + str(i + 16) + ' ' + str(blue))
    r.execute_command('bitfield ' + board + ' set u8 ' + str(i + 24) + ' ' + str(opacity))
    sqr = {'data': array, 'height': 1, 'width': 1}
    return jsonify(sqr)

@app.route("/v8/colors", methods=['GET'])
def v8_color():
    colors = [140,30,44,255,220,68,60,255,255,140,102,255,199,91,56,255,214,111,36,255,228,186,50,255,33,145,59,255,131,181,53,255,235,213,189,255,102,195,217,255,56,124,238,255,53,57,162,255,153,141,162,255,89,78,111,255,43,26,75,255,8,5,14,255]
    if 'clickx' and 'clicky' in request.args:
        clickx = int(request.args['clickx'])
        clicky = int(request.args['clicky'])
    else:
        return jsonify({'data': colors, 'height': 4, 'width': 4})
    if 'rclick' in request.args:
        rclick = 1
    else:
        rclick = 0
    pos = 4*pixelpos(clickx, clicky, 4, 4) # Four entries per pixel
    return jsonify({'data': colors[pos:pos+4], 'height': 1, 'width': 1, 'rclick': rclick})

if __name__ == "__main__":
    app.run()
