import json

from cisco_sdwan_policy.BaseObject import BaseObject


class Mirror(BaseObject):

    def __init__(self,name,source,dest,id=None,reference=None,**kwargs):
        self.type = "mirror"
        self.id = id
        self.name = name
        self.references = reference
        self.source = source
        self.dest = dest
        self.url= "template/policy/list/mirror"
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
        source = config["entries"][0]["source"]
        dest = config["entries"][0]["remoteDest"]

        return cls(name,source,dest,id,references,**kwargs)


    def to_json(self):
        # {"name": "DX", "description": "Desc Not Required", "type": "site", "listId": null,
        #  "entries": [{"siteId": "100"}, {"siteId": "200"}, {"siteId": "300"}]}
        return {
            "name":self.name,
            "description":"Desc Not Required",
            "type":self.type,
            "listId":None,
            "entries":[
                {"remoteDest": self.dest, "source": self.source }
            ]
        }

