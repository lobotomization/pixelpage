from flask import Flask, render_template, send_file, jsonify, request
import redis
import random
def pixelpos(x, y, arrX, arrY):
    return (arrX*(y%arrY) + (x%arrX))%(arrX*arrY)
