from app import app
from flask import render_template, redirect, url_for, request, abort

from app.static import myfirebasemodule
from app.static import climatemodule

from app.static import gihubmodule
from app.static import mycirclecimodule
from app.static import jiramodule

import json
from flask import jsonify


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
    # myfirebase.accessFirebase()

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


@app.route('/topplaces', methods=['POST', 'GET'])
def top_places_details():
    print(request.json)
    buildaction = getActionFromWebhook(request=request)
    print(buildaction)
    if buildaction == "topplaces.action":
        return topplaces(request=request)
    elif buildaction == "hunger.action":
        return hunger_details()
    elif buildaction == 'city_found.action':
        return city_found_details()
    return buildaction


# top places details
def topplaces(request):
    category, city = get_category_city_name(request)

    print(category)
    print(city)

    return_content = '''
    That’s exactly i was about to tell you. Here are the best places of udaipur
        1. City Palace, Distance : 1.0 KM\n
        2. lake Pichola, Distance : 1.5KMS\n
        3. jag Mandir, Distance : 2.4KMS\n
        4. Fatehsagar Lake, Distance : 4.5KMS\n
        5. Jagdish Temple…
        Ask me, More Places..
    '''

    content = buildResponse(speech=return_content, displayText=return_content, source="lakshman", contextOut=None,
                            responseCode=200)
    return content


def get_category_city_name(request):
    category_name = ""
    city_name = ""
    contexts = request.json["result"]["contexts"]

    for ctx in contexts:
        if ctx["city_name"]:
            city_name = ctx["city_name"]
        if ctx["parameters"]:
            if ctx["parameters"]["categories.original"]:
                category_name = ctx["parameters"]["categories.original"]

    return category_name, city_name


def hunger_details():
    return_content = jsonify({
        'response': 'Udaipur Hunger details'
    })
    buildResponse(speech=return_content, displayText=return_content, source="lakshman", contextOut=None,
                  responseCode=200)
    return return_content


def city_found_details():
    return_content = jsonify({
        'response': 'none other than me'
    })
    buildResponse(speech=return_content, displayText=return_content, source="lakshman", contextOut=None,
                  responseCode=200)
    return return_content


@app.route('/content', methods=['POST', 'GET'])
def content_display():
    # print(request.headers)
    # print(request.headers['Content-Type'])
    # print(request.headers['x-api-key'])
    category = 'category'
    task_number = 'task_number'
    # print(request.method)

    if request.method == 'POST':
        if 'application/json' in request.headers['Content-Type'] and request.headers['x-api-key'] == 'Deloitte2017WUSS':
            print(request)
            content_json = json.dumps(request.json)
            print(content_json)
            category = request.json['LiMSS_PM_Cater_c']
            task_number = request.json['LiMSS_Task_Number_s__c']
            return_content = jsonify(
                {
                    'P_ID': 1,
                    'FileName': 'SOme file name',
                    'Title': 'Machinary Title',
                    'SubTitle': 'Machinary Sub Title',
                    'PMCategory': category,
                    'TaskList': 'T012345',
                    'PRTDocument': 'Some value',
                    'F_ID': 9,
                    'TaskNum': task_number,
                    'Descr': "Content is realted to Machinary coming from rest API",
                    'DescrMore': 'More content value need to be added',
                    'Notes': 'Some Notes can also be added'})
        else:
            return_content = jsonify({
                'reason': 'Invalid Media Type'
            })
            return return_content
    elif request.method == 'GET':
        if request.headers['Apikey'] == 'Deloitte2017WUSS':
            category = request.args.get('PMCategory')
            task_number = request.args.get('TaskNumber')
            return_content = jsonify(
                {
                    'P_ID': 1,
                    'FileName': 'SOme file name',
                    'Title': 'Machinary Title',
                    'SubTitle': 'Machinary Sub Title',
                    'PMCategory': category,
                    'TaskList': 'T012345',
                    'PRTDocument': 'Some value',
                    'F_ID': 9,
                    'TaskNum': task_number,
                    'Descr': "Content is realted to Machinary coming from rest API",
                    'DescrMore': 'More content value need to be added',
                    'Notes': 'Some Notes can also be added'})
        else:
            return_content = jsonify({
                'reason': 'Invalid APIKey'
            })
            return return_content
    else:
        return_content = jsonify({
            'reason': 'Method not supported'
        })
        return return_content
    return return_content


@app.route('/webhook', methods=['POST', 'GET'])
def webhookExp():
    webhookaction = getActionFromWebhook(request=request)
    if webhookaction in ['weather.search', 'wind.search']:
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
    elif webhookaction in ['firebase.action', 'firebase.status.action']:
        return processFirebaseRequests(request=request)
    else:
        abort(400)


@app.route('/firebase', methods=['POST', 'GET'])
def firebaseapp():
    return processFirebaseRequests(request=request)


@app.route('/github', methods=['POST', 'GET'])
def accessGithub():
    print("git hub access")
    github = gihubmodule.githubexp()
    # return github.authenticateWithToken()
    results = github.getcommitsforDev(maxresults=10)
    print(results)
    return processGitCommitDetails(results)


@app.route('/circleci', methods=['POST', 'GET'])
def accesscircleci(sessionId):
    '''For triggering the build in the circle CI'''
    print("access circle ci")
    circle = mycirclecimodule.mycircleclient()
    triggerBuild = circle.triggerbuild()
    speech = "build intiated.."
    return buildResponse(speech=speech, displayText=speech, source="lakshman web hook", contextOut=None,
                         responseCode=200)


@app.route('/cipostaccept', methods=['POST', 'GET'])
def cipostaccept():
    print('this request came')
    print(request.json["payload"]["outcome"])
    print(request.json["payload"]["username"])
    print(request.json["payload"]["committer_date"])
    if request.json["payload"]["outcome"] == "success":
        circle = mycirclecimodule.mycircleclient()
        user = request.json["payload"]["username"]
        project = request.json["payload"]["reponame"]
        buildnum = request.json["payload"]["build_num"]
        artifacts = circle.getartifactslist(user=user, project=project, buildnumber=buildnum)
        artifactsList = []
        for arti in artifacts:
            str = arti['url']
            artifactsList.append(str)
        return buildResponse(speech=artifactsList, displayText=artifactsList, source="lakshman webhook",
                             contextOut=None, responseCode=200)
        # return json.dumps(artifactsList)
    else:
        speech = "fail to get the artifacts"
        return buildResponse(speech=speech, displayText=speech, source="lakshman webhook",
                             contextOut=None, responseCode=400)


@app.route('/jiraissues', methods=['POST', 'GET'])
def getJiraIssues():
    jiraclient = jiramodule.myjiraclient()
    # for jiraIssue in jiraclient.getCurrentUserIssues(maxResults=10):
    #     print(jiraclient.getIssuedetails(jiraIssue).fields.summary)
    results = jiraclient.getCurrentUserIssues(maxResults=10)
    return buildResponse(speech=results, displayText=results, contextOut=None, source="lakshman web hook",
                         responseCode=200)


@app.route('/buildhook', methods=['POST', 'GET'])
def handlebuildDetails():
    try:
        if request.json["payload"]:
            return cipostaccept()
    except KeyError as e:
        buildaction = getActionFromWebhook(request=request)
        if buildaction == "gitdetails.action":
            return accessGithub()
        elif buildaction == 'jiradetails.action':
            return getJiraIssues()
        elif buildaction == 'ci.action':
            sessionId = request.json["sessionId"]
            return accesscircleci(sessionId)
        return buildaction


def getActionFromWebhook(request):
    return request.json["result"]["action"]


def processFirebaseRequests(request):
    firebaseapp = myfirebasemodule.myfirebase()
    if request.method == 'POST':
        print(request.json)
        action = request.json["result"]["action"]
        username = request.json["result"]["parameters"]["username"]
        password = request.json["result"]["parameters"]["password"]
        if username == None:
            username = request.form('username')
        if password == None:
            password = request.form('password')
        if action == 'firebase.action':
            loginInfo = firebaseapp.loginFirebase(email=username, password=password)
            result = json.loads(loginInfo)
            # here we are not sending the User object as response
            return buildResponse(speech=result['status'], displayText=result['status'], source='lak webhook',
                                 contextOut=None,
                                 responseCode=result['responsecode'])
        elif action == 'firebase.status.action':
            item = request.json["result"]["parameters"]["deviceorbook"]
            statusInfo = firebaseapp.accessDatabase(email=username, password=password, item=item)
            result = json.loads(statusInfo)
            # here we are not sending the User object as response
            return buildResponse(speech=result['status'], displayText=result['status'], source='lak webhook',
                                 contextOut=None,
                                 responseCode=result['responsecode'])
        else:
            str = 'Not able recognize the request'
            return buildResponse(speech=str, displayText=str, source='laksh webhook', contextOut=None, responseCode=400)

    else:
        print("GET Method ", request.args.get("nm"))
        # method = "GET Method " + request.args.get("nm")
        username = request.args.get("username")
        password = request.args.get("password")
        print("username" + username + ",password." + password)
        createUserInfo = firebaseapp.createUser(username=username, password=password)
        result = json.loads(createUserInfo)
        # here we are not sending the User object as response
        return buildResponse(speech=result['status'], displayText=result['status'], source='lak webhook',
                             contextOut=result['user'], responseCode=result['responsecode'])


def processGitCommitDetails(jsonresult):
    speech = jsonresult
    # for sp in speech:
    #     print(sp)
    return buildResponse(speech=speech, displayText=speech, source="lakshman webhook", contextOut=None,
                         responseCode=200)

    # return buildGitResponse(speech=None, displayText=None, source=None, contextOut=None, responseCode=200)


def getProperty(request, attributeName):
    return request.json["result"][attributeName]


def buildGitResponse(speech, displayText, source, contextOut, responseCode):
    messages = '[{"type":0,"speech":"message1"},{"type":0,"speech":"message2"},{"type":0,"speech":"message3"},{"imageUrl":"https://www.sencha.com/wp-content/uploads/2016/02/icon-sencha-test-cli.png","type":3}]'
    # return jsonify(
    #     {'speech': speech, 'displayText': displayText, 'source': source,
    #      'contextOut': contextOut, 'message': messages}), responseCode
    return jsonify(
        {'speech': "", 'displayText': "displaytext", 'source': "lakshman",
         'contextOut': None, 'message': messages}), responseCode


def buildResponse(speech, displayText, source, contextOut, responseCode):
    messages = '[{"type":0,"speech":"build server not able to serve your request"},{"imageUrl":"https://www.sencha.com/wp-content/uploads/2016/02/icon-sencha-test-cli.png","type":3}]'
    # return jsonify(
    #     {'speech': speech, 'displayText': displayText, 'source': source,
    #      'contextOut': contextOut, 'message': messages}), responseCode
    return jsonify(
        {'speech': speech, 'displayText': displayText, 'source': source,
         'contextOut': contextOut}), responseCode
