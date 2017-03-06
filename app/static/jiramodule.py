from jira import JIRA
import json

from app.static.models import jiramodelsmodule


class myjiraclient(object):
    def __init__(self):
        self.options = {'server': 'https://jira.ddhive.com/'}
        self.jira = JIRA(options=self.options, basic_auth=('labattula', 'Bat123456!'))

    def getprojectlist(self):
        return self.jira.projects()

    def getIssuesInProject(self, project):
        return self.jira.search_issues('project=BBBY')

    def allProjectIssues(self):
        return self.jira.search_issues('project=BBBY and assignee != currentUser()')

    def getCurrentUserIssues(self, maxResults):
        ''' oh_crap = jira.search_issues('assignee = currentUser() and due < endOfWeek() order by priority desc', maxResults=5)'''
        # print(self.jira.search_issues('assignee = currentUser() order by priority desc', maxResults=maxResults,
        #                               json_result=True))

        jiraissues = self.jira.search_issues('assignee = currentUser() order by priority desc', maxResults=maxResults,
                                             json_result=True)

        jiraissueslist = []
        # jiraissueslist.append(jiraissues)
        for jiraissue in jiraissues['issues']:
            issue = jiraissue['key'] + " : " + jiraissue['fields']['summary'] + " - " + jiraissue['fields']['status'][
                'name']
            # print(jiraissue['key'])
            # print(jiraissue['fields']['summary'])
            jiraissueslist.append(issue)

        return json.dumps(jiraissueslist)

    def getIssuedetails(self, issue):
        '''Give the details aboot the jira issue'''
        return self.jira.issue(issue)
