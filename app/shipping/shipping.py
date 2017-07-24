def getShippingCost(parameters):
    zone = parameters.get("shipping-zone")
    cost = {'Europe':100, 'North America':200, 'South America':300, 'Asia':400, 'Africa':500}
    speech = "The cost of shipping to " + zone + " is " + str(cost[zone]) + " euros."

    return {
        "speech": speech,
        "displayText": speech,
        #"data": {},
        # "contextOut": [],
        "source": "apiai-onlinestore-shipping"
    }