from jira import JIRA


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
        print(self.jira.search_issues('assignee = currentUser() order by priority desc', maxResults=maxResults,
                                      json_result=True))
        return "Success"

    def getIssuedetails(self, issue):
        '''Give the details aboot the jira issue'''
        return self.jira.issue(issue)
