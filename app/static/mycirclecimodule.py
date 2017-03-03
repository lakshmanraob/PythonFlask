import os
from circleclient import circleclient


class mycircleclient(object):
    def __init__(self):
        '''This is the initial method for configuring'''
        self.token = 'f963b5e3eace0921e05203d60bbda3a81430a307'
        self.client = circleclient.CircleClient(api_token=self.token)

    def infoAboutAccount(self):
        return self.client.user.info()

    def giveprojectlist(self):
        return self.client.projects.list_projects()

    def triggerbuild(self):
        '''Method for triggering the build'''
        user = 'lakshmanraob'
        project = 'MyFireBaseProject'
        branch = 'dev'
        print(self.client.build.trigger(username=user, project=project, branch=branch))
        return "build triggered"
