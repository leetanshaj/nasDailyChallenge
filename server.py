import requests
from flask import Flask, request, Response, current_app, render_template, jsonify
import json
from datetime import datetime
from dateutil import tz
import threading
import os
from functions import *
os.system('clear')


app = Flask(__name__)
size = 5
carParking = ParkingLot(size)


def prettify(js,statusCode):
    return current_app.response_class(json.dumps(js), mimetype="application/json"),statusCode

@app.route('/v1/carPark/', methods = ['GET', 'POST'])
def r1():
    if request.method == 'GET':
        carNumber = request.args.get('carNumber')
    elif request.method == 'POST':
        carNumber = request.args['carNumber']
    else:
        return {"error": "Unsupported Request Method"}
    print(carNumber)
    return prettify(*carParking.insert(carNumber.lower()  if carNumber else None))

@app.route('/v1/unparkCar/', methods = ['GET', 'POST'])
def r2():
    if request.method == 'GET':
        slotId = request.args.get('slotId')
    elif request.method == 'POST':
        slotId = request.args['slotId']
    else:
        return {"error": "Unsupported Request Method"}
    return prettify(*carParking.delete(slotId))

@app.route('/v1/shiftCar/', methods = ['GET', 'POST'])
def r3():
    if request.method == 'GET':
        slotId = request.args.get('slotId')
        carNumber = request.args.get('carNumber')
    elif request.method == 'POST':
        slotId = request.args['slotId']
        carNumber = request.args['carNumber']
    else:
        return {"error": "Unsupported Request Method"}
    return prettify(*carParking.move(carNumber.lower()  if carNumber else None, slotId))

@app.route('/v1/fetchInfo/', methods = ['GET', 'POST'])
def r4():
    if request.method == 'GET':
        slotId = request.args.get('slotId')
        carNumber = request.args.get('carNumber')
    elif request.method == 'POST':
        slotId = request.args['slotId']
        carNumber = request.args['carNumber']
    else:
        return {"error": "Unsupported Request Method"}
    return prettify(*carParking.fetchInfo(carNumber.lower() if carNumber else None, slotId))



if __name__ == "__main__":
    app.run(debug=True)