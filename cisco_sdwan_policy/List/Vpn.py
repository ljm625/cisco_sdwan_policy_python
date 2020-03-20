import json

from cisco_sdwan_policy.BaseObject import BaseObject


class Vpn(BaseObject):

    def __init__(self,name,vpn_list,id=None,reference=None,**kwargs):
        self.type = "vpnList"
        self.id = id
        self.name = name
        self.references = reference
        self._entries = vpn_list
        self.url ="template/policy/list/vpn"
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
        entries = [i["vpn"] for i in config["entries"]]

        return cls(name,entries,id,references,**kwargs)


    def to_json(self):
        # {"name": "test123", "description": "Desc Not Required", "type": "vpn", "listId": null,
        #  "entries": [{"vpn": "100"}, {"vpn": "200"}, {"vpn": "300"}]}
        return {
            "name":self.name,
            "description":"Desc Not Required",
            "type":"vpn",
            "entries":[
                {"vpn":i} for i in self._entries]
        }



