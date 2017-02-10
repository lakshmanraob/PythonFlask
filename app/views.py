from app import app
from flask import render_template, redirect, url_for, request, abort


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
        print ("sample response",request.json)
        return "Hello user"
    elif request.method == 'GET':
        print ("Hello User from custom")
        return "GET method"
    else:
        abort(400)
