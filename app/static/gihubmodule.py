import requests
import json

from app.static.models import gitmodelsmodule


class githubexp:
    def __init__(self):
        self.github_token = "39be6acd3b9fb23bcd2d6ab343633ffd56ccedb9"
        self.base_url = "https://api.github.com"
        self.git_urls = None

    def getAccessToAccount(self):
        r = requests.get(self.base_url, auth=('lakshmanraob@gmail.com', 'laksh2682'))
        print(r.status_code)
        print(r.headers['content-type'])
        return r.content

    def authenticateWithToken(self):
        token = "token " + self.github_token
        headers = {"Authorization": token}
        r = requests.get(self.base_url, headers=headers)

        if r.status_code == 200:
            self.git_urls = json.loads(r.content.decode("utf-8"), object_hook=self.getGitUrl)
            print(self.git_urls.current_user_authorizations_html_url)
            return self.getReposList()
            # return self.git_urls['current_user_url']
        else:
            return r.content

    # Dictionary to Object conversion method
    def getGitUrl(self, d):
        gitUrls = gitmodelsmodule.gitUrl()
        gitUrls.__dict__.update(d)
        return gitUrls

    """Gives the Repo list """

    def getReposList(self):
        if self.git_urls:
            token = "token " + self.github_token
            headers = {"Authorization": token}
            r = requests.get(self.base_url + "/user/repos", headers=headers)
            """"List of repos display will happen from here"""
            reposList = json.loads(r.content.decode("utf-8"))
            for repo in reposList:
                # print(repo['name'])
                gitrepoObj = gitmodelsmodule.gitrepo(repo)
                if gitrepoObj.name == "MyFireBaseProject":
                    # print(gitrepoObj.name)
                    gitOwner = gitmodelsmodule.gitrepoowner(gitrepoObj.owner)
                    self.getBranchList(owner=None, reponame=None, repo_url=gitrepoObj.url)
                    print(gitOwner)
            return r.content

    """Gives you the Number of branches available for the given repo"""

    def getBranchList(self, owner, reponame, repo_url):
        token = "token " + self.github_token
        headers = {"Authorization": token}
        if repo_url:
            branches_url = repo_url + "/branches"
        else:
            branches_url = self.base_url + "/repos/" + owner + "/" + reponame + "/branches"
        r = requests.get(branches_url, headers=headers)
        print(reponame)
        print(r.content)
        print("-----------------")
        return r.content

    def getcommitsforDev(self, maxresults):
        '''/repos/:owner/:repo/commits?sha=branchname'''
        token = "token " + self.github_token
        headers = {"Authorization": token}
        owner = 'lakshmanraob'
        reponame = 'MyFireBaseProject'
        branchname = 'dev'
        commit_details = []
        commits_url = branches_url = self.base_url + "/repos/" + owner + "/" + reponame + "/commits?sha=" + branchname
        r = requests.get(commits_url, auth=('lakshmanraob@gmail.com', 'laksh2682'))
        # reposList = json.loads(r.content.decode("utf-8"))
        # return reposList[0]
        content = json.loads(r.content.decode('utf-8'))
        for commit in content:
            if len(commit_details) <= maxresults:
                commit_details.append(
                    commit['commit']['message'] + " - " + commit['commit']['committer']['name'])
        return json.dumps(commit_details)
