import json

from cisco_sdwan_policy.BaseObject import BaseObject


class Tloc(BaseObject):

    def __init__(self,name,tloc_list,id=None,reference=None,**kwargs):
        self.type = "tlocList"
        self.id = id
        self.name = name
        self.references = reference
        self._entries = tloc_list
        self.url = "template/policy/list/tloc"

        # TODO :

        super().__init__(**kwargs)
        self.modified=False


    def get_entries(self):
        return self._entries

    def set_entries(self, entries):
        self.modified = True
        self._entries = entries

    def add_tloc(self,tloc,color,encap,preference):
        self.modified = True
        self._entries.append({
            "tloc":tloc,
            "color":color,
            "encap":encap,
            "preference":preference
        })

    @classmethod
    def from_json(cls,config,**kwargs):
        id = config["listId"]
        name = config["name"]
        references = config.get("references")
        entries = config["entries"]

        return cls(name,entries,id,references,**kwargs)

    def to_json(self):
        # {"name": "test1", "description": "Desc Not Required", "type": "tloc",
        #  "entries": [{"tloc": "1.1.1.1", "color": "3g", "encap": "ipsec", "preference": "1"},
        #              {"tloc": "2.2.2.2", "color": "bronze", "encap": "gre", "preference": "2"}]}
        return {
            "name":self.name,
            "description":"Desc Not Required",
            "type":"tloc",
            "entries":self._entries
        }

