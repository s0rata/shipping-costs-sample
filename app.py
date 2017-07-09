#!/usr/bin/env python

import urllib
import json
import os
import requests

from flask         import Flask
from flask         import json
from flask         import request
from flask         import make_response
from config        import *


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
            zone = parameters.get("shipping-zone")

            cost = {'Europe':100, 'North America':200, 'South America':300, 'Asia':400, 'Africa':500}

            speech = "The cost of shipping to " + zone + " is " + str(cost[zone]) + " euros."

        # webhook for weather
        if action == "weather.now":
            zone = parameters.get("geo-city")
            query = "q=%s"%(zone)
            appid = "APPID=%s"%(apikey)
            qtype = "type=accurate"
            units = "units=metric"
            apiurl = "http://api.openweathermap.org/data/2.5/forecast?%s&%s&%s&%s"%(query,appid,qtype,units)
            r   = requests.get(apiurl)
            result = eval(r.text)
            l = result.get('list')[0]
            main = l.get('main')
            temp = main.get('temp')

            speech = "The current temperature in %s is %s degree celcius."%(zone,temp)

        print("Response:")
        print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        #"data": {},
        # "contextOut": [],
        "source": "apiai-onlinestore-shipping"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print ("Starting app on port %s" % port) 

    app.run(debug=True, port=port, host='0.0.0.0')
