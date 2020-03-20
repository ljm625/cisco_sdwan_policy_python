import json

from cisco_sdwan_policy.BaseObject import BaseObject


class Community(BaseObject):

    def __init__(self,name,community_list,id=None,reference=None,**kwargs):
        self.type = "community"
        self.id = id
        self.name = name
        self.references = reference
        self._entries = community_list
        self.url= "template/policy/list/community"
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
        entries = [i["community"] for i in config["entries"]]

        return cls(name,entries,id,references,**kwargs)


    def to_json(self):
        # {"name": "DX", "description": "Desc Not Required", "type": "site", "listId": null,
        #  "entries": [{"siteId": "100"}, {"siteId": "200"}, {"siteId": "300"}]}
        return {
            "name":self.name,
            "description":"Desc Not Required",
            "type":self.type,
            "listId":None,
            "entries":[
                {"community":i} for i in self._entries]
        }

