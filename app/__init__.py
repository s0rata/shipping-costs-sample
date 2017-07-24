#!/usr/bin/env python

import json
import os

from flask          import Flask
from flask          import json
from flask          import request
from flask          import make_response
from .register       import *

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST', 'GET'])
def webhook():
    r = "Welcome"

    if request.method == "POST":
        req = request.get_json(silent=True, force=True)

        print("Request:")
        print(json.dumps(req, indent=4))

        res = makeWebhookResult(req)

        res = json.dumps(res, indent=4)
        print(res)
        r = make_response(res)
        r.headers['Content-Type'] = 'application/json'
    return r

def makeWebhookResult(req):
    result = req.get("result",{})
    action = result.get("action","")
    parameters = result.get("parameters",{})

    if action != "shipping.cost" and action != "weather.now":
        return {}
    else:
        # webhook for shipping cost
        if action == "shipping.cost":
            result = getShippingCost(parameters)

        # webhook for weather
        if action == "weather.now":
            result = getWeather(parameters)

        if action == "calendar.view"
            result == getCalendar(parameters)

    return result