class gitUrl(object):
    current_user_url = ""
    current_user_authorizations_html_url = ""
    code_search_url = ""
    commit_search_url = ""
    emails_url = ""
    emojis_url = ""
    events_url = ""
    feeds_url = ""
    followers_url = ""
    user_url = ""
    user_organizations_url = ""
    user_repositories_url = ""
    user_search_url = ""
    repository_url = ""


class gitrepo(object):
    id = ""
    name = ""
    owner = None
    full_name = ""
    private = ""
    description = ""
    url = ""
    collaborators_url = ""
    branches_url = ""
    contributors_url = ""
    subscribers_url = ""
    commits_url = ""
    git_commits_url = ""
    comments_url = ""
    issue_comment_url = ""
    deployments_url = ""
    releases_url = ""

    def __init__(self, dictionary):
        for key in dictionary:
            setattr(self, key, dictionary[key])

    def __repr__(self):
        return "<gitRepo: %s>" % self.__dict__


class gitrepoowner(object):
    login = ""
    id = ""
    avatar_url = ""
    gravatar_id = ""
    url = ""
    html_url = ""
    followers_url = ""
    following_url = ""
    gists_url = ""
    starred_url = ""
    subscriptions_url = ""
    organizations_url = ""
    repos_url = ""
    events_url = ""
    received_events_url = ""
    type = ""
    site_admin = ""

    def __init__(self, dictionary):
        for key in dictionary:
            setattr(self, key, dictionary[key])

    def __repr__(self):
        return "<gitRepoOwner: %s>" % self.__dict__
