from flask import Flask, render_template, send_file, jsonify, request
from pywebpush import webpush, WebPushException
import redis
import random
import math
import os
import sqlite3
import json

def pixelpos(x, y, arrX, arrY):
    return (arrX*(y%arrY) + (x%arrX))%(arrX*arrY)

def diagpixelpos(x, y):
    x = abs(x)
    y = abs(y)
    return int((x+y)*(x+y+1)/2+y)

def sector(x, y, arrX, arrY):
    return math.floor(x/arrX), math.floor(y/arrY)

def connect_db(database_name):
    try:
        return sqlite3.connect(database_name)
    except sqlite3.Error as e:
        print(e)
    return -1

def create_table(c):
    print("Creating table")
    try:
        cursor_obj = c.cursor()
        cursor_obj.execute("CREATE TABLE subscription(sub text PRIMARY KEY)")
        c.commit()
    except sqlite3.OperationalError as e:
        print(e)

def insert_entry(c, sub):
    stmt = "INSERT INTO subscription VALUES(?)"
    sub.pop('expirationTime', None)
    entries = (json.dumps(sub),)
    try:
        cursor_obj = c.cursor()
        cursor_obj.execute(stmt, entries)
        c.commit()
    except sqlite3.IntegrityError as e:
        print("Entry already exists")
    print()

def get_entries(c):
    stmt = "SELECT * FROM subscription"
    try:
        cursor_obj = c.cursor()
        return cursor_obj.execute(stmt).fetchall()
    except Exception as e:
        print('fail')
        print(e)
    return []

cwd = "/var/www/pixelart/pixelart"
DER_BASE64_ENCODED_PRIVATE_KEY_FILE_PATH = os.path.join(cwd,"private_key.txt")
DER_BASE64_ENCODED_PUBLIC_KEY_FILE_PATH = os.path.join(cwd,"public_key.txt")

VAPID_PRIVATE_KEY = open(DER_BASE64_ENCODED_PRIVATE_KEY_FILE_PATH, "r+").readline().strip("\n")
VAPID_PUBLIC_KEY = open(DER_BASE64_ENCODED_PUBLIC_KEY_FILE_PATH, "r+").read().strip("\n")

VAPID_CLAIMS = {
        "sub": "mailto:admin@whisperwork.com"
}

def send_web_push(subscription_information, message_body):
    return webpush(
        subscription_info=subscription_information,
        data=message_body,
        vapid_private_key=VAPID_PRIVATE_KEY,
        vapid_claims=VAPID_CLAIMS
    )
