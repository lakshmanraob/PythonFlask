from app import app
from flask import render_template, redirect, url_for, request, abort, jsonify
import json
import urllib.request, urllib.parse, urllib.error
from app.static import myfirebasemodule


@app.route('/')
@app.route('/index')
def index():
    user = {'nickname': 'lakshman'}

    posts = [
        {
            'author': {'nickname': 'lakshman'},
            'body': 'Beautiful day in India'
        },
        {
            'author': {'nickname': 'madhu'},
            'body': 'Good man'
        },
        {
            'author': {'nickname': 'anoop'},
            'body': 'Quality Assurance'
        }
    ]
    myfirebase = myfirebasemodule.myfirebase()
    myfirebase.accessFirebase()

    return render_template('index.html', posts=posts, user=user)


def checkFun():
    return "check functionality"


# Another way of routing
app.add_url_rule('/check', 'checkStr', checkFun)


@app.route("/admin")
def iamAdmin():
    return "hi Admin"


# argument passing
@app.route('/hi/<name>')
def checkName(name):
    if name == 'admin':
        return redirect(url_for('iamAdmin'))
    else:
        return "hello %s!" % name


@app.route('/square/<int:postId>')
def square(postId):
    return str(postId * postId)


@app.route('/rev/<float:revNo>')
def revNumber(revNo):
    return str(revNo)


@app.route('/login', methods=['POST', 'GET'])
def loginAccount():
    if request.method == 'POST':
        user = request.form['nm']
        return 'POST method..' + user
    else:
        user = request.args.get('nm')
        return 'GET method..' + user


@app.route('/webhook', methods=['POST', 'GET'])
def webhookExp():
    if request.method == 'POST':
        location = getLocation(req=request)
        if location:
            print("weather condition required for ..", location)
            return processAction(request)
        else:
            print("actual json file", request.json)
    elif request.method == 'GET':
        return processGetrequest(request)
    else:
        abort(400)


# extract location
def getLocation(req):
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
def processGetrequest(req):
    print("Hello User from custom")
    return jsonify({'status': 'success', 'method': 'GET', 'message': 'This is simple message'}), 200


# Processing the location to get the Weather for the extracted location
def processAction(req):
    if req.json["result"]["action"] in ['weather.search', 'wind.search']:
        return processWeatherSearch(req, action=req.json["result"]["action"])
    elif req.json["result"]['action'] != 'weather.search':
        return {}
    else:
        return processWeatherSearch(req)


def processWeatherSearch(req, action):
    baseurl = "https://query.yahooapis.com/v1/public/yql?"
    yql_query = makeyqlQuery(req)
    if yql_query:
        yql_query = baseurl + urllib.parse.urlencode({'q': yql_query}) + "&format=json"
        result = urllib.request.urlopen(yql_query).read().decode('utf-8')
        if result:
            data = json.loads(result)
            if action == 'weather.search':
                return extractWeather(data)
            elif action == 'wind.search':
                return extractWind(data)
        else:
            return processErrorrequest(result.getcode())
    else:
        return processErrorrequest(206)


def extractWind(result):
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
                return processErrorrequest(206, "fail in channel")
        else:
            return processErrorrequest(206, "fail in result")
    return processErrorrequest(206, "fail in query")


def makeyqlQuery(req):
    city = getLocation(req)
    if city:
        return "select * from weather.forecast where woeid in (select woeid from geo.places(1) where text='" + city + "')"
    else:
        return processErrorrequest(206, "failed in makeyqlQuery fails")


def processErrorrequest(code, msg):
    return jsonify({'code': code, 'message': errorResponse(code, msg=msg)}), code


def errorResponse(code, msg):
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


def extractWeather(result):
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
                for forecast in forecastForFuture:
                    print(processForecast(forecast))
                speech = "Today in " + cityLocation + ' weather is ' + forecastForToday[
                    'text'] + ' with temperature of ' + \
                         forecastForToday[
                             'temp'] + units
                # return jsonify({'status': 'success', 'message': parsed_json[10]}), 200
                return jsonify(
                    {'speech': speech, 'displayText': speech, 'source': 'lakshman weather support from yahoo',
                     'contextOut': [{'name': 'weather', 'lifespan': 2, 'parameters': {'city': cityName}}]}), 200
            else:
                return processErrorrequest(206, "fail in channel")
        else:
            return processErrorrequest(206, "fail in result")
    return processErrorrequest(206, "fail in query")


def processForecast(forecast):
    return forecast['day'] + "," + forecast['date'] + " highest " + forecast['high'] + " lowest " + forecast[
        'low'] + " " + forecast['text']
