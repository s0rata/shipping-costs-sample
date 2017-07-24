import app.config as config
import requests
def getWeather(parameters):
    zone = parameters.get("geo-city")
    query = "q=%s"%(zone)
    appid = "APPID=%s"%(config.apikey)
    qtype = "type=accurate"
    units = "units=metric"
    apiurl = "http://api.openweathermap.org/data/2.5/forecast?%s&%s&%s&%s"%(query,appid,qtype,units)
    r   = requests.get(apiurl)
    result = eval(r.text)
    l = result.get('list')[0]
    main = l.get('main')
    temp = main.get('temp')

    speech = "The current temperature in %s is %s degree celcius."%(zone,temp)
    
    return {
        "speech": speech,
        "displayText": speech,
        #"data": {},
        # "contextOut": [],
        "source": "apiai-onlinestore-shipping"
    }