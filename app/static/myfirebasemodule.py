import pyrebase


class myfirebase:
    def __init__(self):
        self.config = {
            "apiKey": "apiKey",
            "authDomain": "projectId.firebaseapp.com",
            "databaseURL": "https://databaseName.firebaseio.com",
            "storageBucket": "projectId.appspot.com"
        }
        self.firebase = pyrebase.initialize_app(self.config)

    def accessFirebase(self):
        print("accessFirebase")
