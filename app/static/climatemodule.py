import json
import urllib.request, urllib.parse, urllib.error
from flask import jsonify


class climateaction:
    # extract location
    def getLocation(self, req):
        location = req.json['result']['parameters']['geo-city']
        if location:
            return location
        else:
            requestContexts = req.json['result']['contexts']
            if requestContexts and len(requestContexts) > 0:
                for reqContext in requestContexts:
                    if reqContext['lifespan'] > 0:
                        return reqContext['parameters']['geo-city']

    # Processing the Get request
    def processGetrequest(self, req):
        print("Hello User from custom")
        return jsonify({'status': 'success', 'method': 'GET', 'message': 'This is simple message'}), 200

    # Processing the location to get the Weather for the extracted location
    def processAction(self, req):
        if req.json["result"]["action"] in ['weather.search', 'wind.search']:
            action = req.json["result"]["action"]
            return self.processWeatherSearch(req=req, action=action)
        elif req.json["result"]['action'] != 'weather.search':
            return {}
        else:
            return self.processWeatherSearch(req)

    def processWeatherSearch(self, req, action):
        baseurl = "https://query.yahooapis.com/v1/public/yql?"
        yql_query = self.makeyqlQuery(req)
        if yql_query:
            yql_query = baseurl + urllib.parse.urlencode({'q': yql_query}) + "&format=json"
            result = urllib.request.urlopen(yql_query).read().decode('utf-8')
            if result:
                data = json.loads(result)
                if action == 'weather.search':
                    return self.extractWeather(data)
                elif action == 'wind.search':
                    return self.extractWind(data)
            else:
                return self.processErrorrequest(result.getcode())
        else:
            return self.processErrorrequest(206)

    def extractWind(self, result):
        query = result['query']
        if query:
            result = query['results']
            if result:
                channel = result['channel']
                if channel:
                    units = channel['units']['speed']
                    cityName = channel['location']['city']
                    cityLocation = channel['location']['city'] + "," + channel['location']['country']
                    windCondition = channel['wind']
                    speech = "Today in " + cityLocation + ' wind is flowing  with a speed of ' + \
                             windCondition['speed'] + units
                    # return jsonify({'status': 'success', 'message': parsed_json[10]}), 200
                    return jsonify(
                        {'speech': speech, 'displayText': speech, 'source': 'lakshman weather support from yahoo',
                         'contextOut': [{'name': 'weather', 'lifespan': 2, 'parameters': {'city': cityName}}]}), 200
                else:
                    return self.processErrorrequest(206, "fail in channel")
            else:
                return self.processErrorrequest(206, "fail in result")
        return self.processErrorrequest(206, "fail in query")

    def makeyqlQuery(self, req):
        city = self.getLocation(req)
        if city:
            return "select * from weather.forecast where woeid in (select woeid from geo.places(1) where text='" + city + "')"
        else:
            return self.processErrorrequest(206, "failed in makeyqlQuery fails")

    def processErrorrequest(self, code, msg):
        return jsonify({'code': code, 'message': self.errorResponse(code, msg=msg)}), code

    def errorResponse(self, code, msg):
        if code == 400:
            return "400 BAD request"
        elif code == 401:
            return "401 Unauthorized"
        elif code == 403:
            return "403 Forbidden"
        elif code == 404:
            return "404 Not found"
        elif code == 500:
            return "500 Server fault"
        elif code == 503:
            return "503 server not available"
        else:
            return "webhook call failed with %code% error ", msg

    def extractWeather(self, result):
        query = result['query']
        if query:
            result = query['results']
            if result:
                channel = result['channel']
                if channel:
                    units = channel['units']['temperature']
                    cityName = channel['location']['city']
                    cityLocation = channel['location']['city'] + "," + channel['location']['country']
                    forecastForToday = channel['item']['condition']
                    forecastForFuture = channel['item']['forecast']
                    # attachContextOut = jsonify(
                    #     [{'name': 'weather', 'lifespan': 2, 'parameters': {'city': cityName}}])
                    for fore in forecastForFuture:
                        print(self.processForecast(fore))
                    speech = "Today in " + cityLocation + ' weather is ' + forecastForToday[
                        'text'] + ' with temperature of ' + \
                             forecastForToday[
                                 'temp'] + units
                    # return jsonify({'status': 'success', 'message': parsed_json[10]}), 200
                    return jsonify(
                        {'speech': speech, 'displayText': speech, 'source': 'lakshman weather support from yahoo',
                         'contextOut': [{'name': 'weather', 'lifespan': 2, 'parameters': {'city': cityName}}]}), 200
                else:
                    return self.processErrorrequest(206, "fail in channel")
            else:
                return self.processErrorrequest(206, "fail in result")
        return self.processErrorrequest(206, "fail in query")

    def processForecast(self, forecast):
        return forecast['day'] + "," + forecast['date'] + " highest " + forecast['high'] + " lowest " + forecast[
            'low'] + " " + forecast['text']
