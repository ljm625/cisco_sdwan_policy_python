import json

from cisco_sdwan_policy.BaseObject import BaseObject


class Prefix(BaseObject):

    def __init__(self,name,prefix_list,is_ipv6=False,id=None,reference=None):
        self.type = "prefixList"
        self.id = id
        self.name = name
        self.references = reference
        self.ipv6=is_ipv6
        if self.ipv6:
            self.url = "template/policy/list/ipv6prefix"
        else:
            self.url = "template/policy/list/prefix"

        self._entries=prefix_list
        super().__init__()
        self.modified=False


    def get_entries(self):
        return self._entries

    def set_entries(self, entries):
        self.modified = True
        self._entries = entries

    @classmethod
    def from_json(cls,config):

        if config["type"].lower() == "ipv6prefix":
            ipv6=True
            entries = [i["ipv6Prefix"] for i in config["entries"]]

        else:
            ipv6=False
            entries = [i["ipPrefix"] for i in config["entries"]]

        id = config["listId"]
        name = config["name"]
        references = config.get("references")
        return cls(name,entries,ipv6,id,references)

    def to_json(self):
        return {
            "name":self.name,
            "description":"Desc Not Required",
            "type":"ipv6prefix" if self.ipv6 else "prefix",
            "entries":[
                {"ipv6Prefix" if self.ipv6 else "ipPrefix":i} for i in self._entries]
        }
