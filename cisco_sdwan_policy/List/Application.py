import json

from cisco_sdwan_policy.BaseObject import BaseObject


class Application(BaseObject):

    def __init__(self,name,app_list,is_app_family,id=None,reference=None,**kwargs):
        self.type = "appList"
        self.id = id
        self.name = name
        self.references = reference
        self.app_family=is_app_family
        self._entries = app_list
        self.url = "template/policy/list/app"
        super().__init__(**kwargs)
        self.modified=False

    def get_entries(self):
        return self._entries

    def set_entries(self,entries):
        self.modified=True
        self._entries=entries

    @classmethod
    def from_json(cls,jsonfile,**kwargs):

        id = jsonfile["listId"]
        name = jsonfile["name"]
        references = jsonfile.get("references")
        if len(jsonfile["entries"])>0 and jsonfile["entries"][0].get("app"):
            appFamily=False
            entries = [i["app"] for i in jsonfile["entries"]]
        else:
            if not jsonfile["entries"][0].get("appFamily"):
                return None
            else:
                appFamily=True
                entries = [i["appFamily"] for i in jsonfile["entries"]]
        return cls(name,entries,appFamily,id,references,**kwargs)

    def to_json(self):
        return {
            "name":self.name,
            "description":"Desc Not Required",
            "type":"app",
            "entries":[
                {"appFamily" if self.app_family else "app":i} for i in self._entries]
        }
