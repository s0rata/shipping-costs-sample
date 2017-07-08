#!/usr/bin/env python

import urllib
import json
import os
import requests

from flask         import Flask
from flask         import json
from flask         import request
from flask         import make_response
# from weather       import Weather


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
            zone = parameters.get('geo.city', "phnom penh")
            apiurl = "api.openweathermap.org/data/2.5/forecast?q=%s&APPID=%s"%(zone,apikey)
            r   = requests.get(apiurl)
            result = eval(r.text)
            main = result.get('main')
            temp = main.get('temp')
            # weather = Weather()
            # lookup  = weather.weather.lookup_by_location(zone)
            # condition = lookup.condition()
            speech = "The current temperature in %s is %s."%(zone,temp)

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
