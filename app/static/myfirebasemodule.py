import pyrebase
from requests import HTTPError
import json


class myfirebase:
    def __init__(self):
        self.config = {
            "apiKey": "AIzaSyAEhH-XHoAnnZPl4U2UbFoXLJ11gbyF18Y",
            "authDomain": "https://fbauthentication-9b3a2.firebaseio.com",
            "databaseURL": "https://fbauthentication-9b3a2.firebaseio.com",
            "storageBucket": "gs://fbauthentication-9b3a2.appspot.com/"
        }
        self.firebase = pyrebase.initialize_app(self.config)
        self.auth = self.firebase.auth()
        self.user = None

    # accessing the Firebase with given username and password
    '''If the user given the login id which is not registered, then will automatically
    routed to create user'''

    def loginFirebase(self, email, password):
        try:
            self.user = self.auth.sign_in_with_email_and_password(email=email, password=password)
            return json.dumps({'status': 'logged in as ' + email, 'responsecode': '200', 'user': self.user})
        except HTTPError as e:
            errorJson = json.loads(e.strerror)
            if errorJson['error']['code'] == 400:
                if errorJson['error']['message'] == 'EMAIL_NOT_FOUND':
                    return self.createUser(email=email, password=password)
                elif errorJson['error']['message'] == 'INVALID_PASSWORD':
                    return json.dumps({'status': 'Invalid password!, please enter the password',
                                       'responsecode': errorJson['error']['code']})
                else:
                    return json.dumps({'status': errorJson['error']['message'],
                                       'responsecode': errorJson['error']['code']})
            else:
                return json.dumps({'status': errorJson['error']['message'],
                                   'responsecode': errorJson['error']['code']})

    # creating the user with given username and password
    def createUser(self, email, password):
        print("creating the new user")
        try:
            self.user = self.auth.create_user_with_email_and_password(email=email, password=password)
            return json.dumps({'status': 'created a profile for ' + email, 'responsecode': '200', 'user': self.user})
        except HTTPError as e:
            errorJson = json.loads(e.strerror)
            if errorJson['error']['code'] == 400:
                if errorJson['error']['message'] == 'EMAIL_EXISTS':
                    return self.loginFirebase(email=email, password=password)
                else:
                    return json.dumps({'status': errorJson['error']['message'],
                                       'responsecode': errorJson['error']['code']})

            else:
                return json.dumps({'status': errorJson['error']['message'],
                                   'responsecode': errorJson['error']['code']})

    # For accessing the Database for getting the particular device/book status
    def accessDatabase(self, email, password, item):
        print("User need to access the Database {},{},{}", email, password, item)
        self.user = self.loginFirebase(email=email, password=password)
        token = json.loads(self.user)["user"]["idToken"]
        print(token)
        db = self.firebase.database()
        devices = db.child("devices").get(token=token)
        try:
            print(devices.val()[item])
            status = devices.val()[item]['modelState']
            return json.dumps({'status': ' status of  ' + item + " is " + status, 'responsecode': '200'})
        except KeyError as e:
            print(e)
            return json.dumps(
                {'status': "looks like " + item + " is not part of our collection", 'responsecode': '200'})
