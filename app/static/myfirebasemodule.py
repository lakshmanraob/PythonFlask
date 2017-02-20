import pyrebase
from requests import HTTPError
import json
from flask import jsonify


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

    # accessing the Firebase with given username and password
    def loginFirebase(self, email, password):
        user = self.auth.sign_in_with_email_and_password(email=email, password=password)
        print(user)
        return jsonify({'status': 'login', 'responsecode': '200', 'user': user})

    # creating the user with given username and password
    def createUser(self, username, password):
        print("creating the new user")
        try:
            user = self.auth.create_user_with_email_and_password(email=username, password=password)
            return jsonify({'status': 'newuser', 'responsecode': '200', 'user': user})
        except HTTPError as e:
            errorJson = json.loads(e.strerror)
            if errorJson['error']['code'] == 400:
                if errorJson['error']['message'] == 'EMAIL_EXISTS':
                    return self.loginFirebase(email=username, password=password)
                else:
                    return jsonify({'status': errorJson['error']['message'],
                                    'responsecode': errorJson['error']['code']})

            else:
                return jsonify({'status': errorJson['error']['message'],
                                'responsecode': errorJson['error']['code']})
