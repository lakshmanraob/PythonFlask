import json


class jiraissue(object):
    id = ""
    summary = ""
    key = ""
    url = ""

    def __init__(self, dictionary):
        for key in dictionary:
            # if self.key:
            #     self.url = "https://jira.ddhive.com/browse/" + self.key
            #     setattr(self, "url", self.url)
            setattr(self, key, dictionary[key])

    def getJson(self):
        jsonDump = json.dumps(self.__dict__)
        return json.loads(jsonDump)

    def __repr__(self):
        return "<JIRA Issue: %s>" % self.__dict__
