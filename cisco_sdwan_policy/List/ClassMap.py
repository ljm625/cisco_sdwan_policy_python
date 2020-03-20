import json

from cisco_sdwan_policy.BaseObject import BaseObject


class ClassMap(BaseObject):

    def __init__(self,name,queue,id=None,reference=None,**kwargs):
        self.type = "class"
        self.id = id
        self.name = name
        self.references = reference
        assert queue>=0 and queue<=7 and type(queue)==int
        self.queue = queue
        self.url= "template/policy/list/class"
        super().__init__(**kwargs)
        self.modified=False


    def get_entries(self):
        return self._entries

    def set_entries(self, entries):
        self.modified = True
        self._entries = entries

    @classmethod
    def from_json(cls,config,**kwargs):
        id = config["listId"]
        name = config["name"]
        references = config.get("references")
        queue = int(config["entries"][0]["queue"])

        return cls(name,queue,id,references,**kwargs)


    def to_json(self):
        # {"name": "DX", "description": "Desc Not Required", "type": "site", "listId": null,
        #  "entries": [{"siteId": "100"}, {"siteId": "200"}, {"siteId": "300"}]}
        return {
            "name":self.name,
            "description":"Desc Not Required",
            "type":self.type,
            "listId":None,
            "entries":[
                {"queue":self.queue}]
        }

