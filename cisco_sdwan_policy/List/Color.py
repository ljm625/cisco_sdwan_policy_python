import json

from cisco_sdwan_policy.BaseObject import BaseObject


class Color(BaseObject):

    def __init__(self,name,color_list,id=None,reference=None,**kwargs):
        self.type = "colorList"
        self.id = id
        self.name = name
        self.references = reference
        self._entries = color_list

        self.url = "template/policy/list/color"
        super().__init__(**kwargs)
        self.modified=False


    def get_entries(self):
        return self._entries

    def set_entries(self, entries):
        self.modified = True
        self._entries = entries

    @classmethod
    def from_json(cls,jsonfile,**kwargs):
        id = jsonfile["listId"]
        name = jsonfile["name"]
        references = jsonfile.get("references")
        entries = [i["color"] for i in jsonfile["entries"]]

        return cls(name,entries,id,references,**kwargs)

    def to_json(self):
        return {
            "name":self.name,
            "description":"Desc Not Required",
            "type":"color",
            "entries":[
                {"color":i} for i in self._entries]
        }
