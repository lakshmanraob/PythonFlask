import json


class jiraissue(object):
    id = ""
    summary = ""
    key = ""
    url = ""

    # def default(self, o):
    #     return o.__dict__

    def __init__(self, dictionary):
        for key in dictionary:
            # if self.key:
            #     self.url = "https://jira.ddhive.com/browse/" + self.key
            #     setattr(self, "url", self.url)
            setattr(self, key, dictionary[key])

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


        # def __repr__(self):
        #     return self.__dict__
