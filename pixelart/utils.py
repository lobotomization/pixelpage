from flask import Flask, render_template, send_file, jsonify, request
import redis
import random
def pixelpos(x, y, arrX, arrY):
    return (arrX*(y%arrY) + (x%arrX))%(arrX*arrY)
def diagpixelpos(x, y):
    x = abs(x)
    y = abs(y)
    return int((x+y)*(x+y+1)/2+y)
