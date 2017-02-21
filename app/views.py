from app import app
from flask import render_template, redirect, url_for, request, abort

from app.static import myfirebasemodule
from app.static import climatemodule

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
    webhookaction = getActionFromWebhook(request=request)
    if webhookaction in ['weather.action', 'wind.action']:
        climateaction = climatemodule.climateaction()
        if request.method == 'POST':
            location = climateaction.getLocation(req=request)
            if location:
                print("weather condition required for ..", location)
                return climateaction.processAction(request)
            else:
                print("actual json file", request.json)
        elif request.method == 'GET':
            return climateaction.processGetrequest(request)
        else:
            abort(400)
    elif webhookaction == 'firebase.action':
        return processFirebaseRequests(request=request)
    else:
        abort(400)


@app.route('/firebase', methods=['POST', 'GET'])
def firebaseapp():
    return processFirebaseRequests(request=request)


def getActionFromWebhook(request):
    return request.json["result"]["action"]


def processFirebaseRequests(request):
    firebaseapp = myfirebasemodule.myfirebase()
    if request.method == 'POST':
        username = request.json["result"]["parameters"]["username"]
        password = request.json["result"]["parameters"]["password"]
        if username == None:
            username = request.form('username')
        if password == None:
            password = request.form('password')

        return firebaseapp.loginFirebase(email=username, password=password)
    else:
        print("GET Method ", request.args.get("nm"))
        # method = "GET Method " + request.args.get("nm")
        username = request.args.get("username")
        password = request.args.get("password")
        print("username" + username + ",password." + password)
        return firebaseapp.createUser(username=username, password=password)


def getProperty(request, attributeName):
    return request.json["result"][attributeName]
