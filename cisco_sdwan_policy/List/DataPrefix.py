import json

from cisco_sdwan_policy.BaseObject import BaseObject


class DataPrefix(BaseObject):

    def __init__(self,name,prefix_list,is_ipv6=False,id=None,reference=None,**kwargs):
        self.type = "dataprefixList"
        self.ipv6=is_ipv6

        self._entries=prefix_list
        self.id = id
        self.name = name
        self.references = reference
        super().__init__(**kwargs)
        if int(self.rest.version.split(".")[0])<19:
            self.ipv6=False
        if self.ipv6:
            self.url = "template/policy/list/dataipv6prefix"
        else:
            self.url = "template/policy/list/dataprefix"

        self.modified=False


    def get_entries(self):
        return self._entries

    def set_entries(self, entries):
        self.modified = True
        self._entries = entries

    @classmethod
    def from_json(cls,config,**kwargs):

        if config["type"] == "dataIpv6Prefix":
            ipv6=True
            entries = [i["ipv6Prefix"] for i in config["entries"]]

        else:
            ipv6=False
            entries = [i["ipPrefix"] for i in config["entries"]]

        id = config["listId"]
        name = config["name"]
        references = config.get("references")

        return cls(name,entries,ipv6,id,references,**kwargs)

    def to_json(self):
        return {
            "name":self.name,
            "description":"Desc Not Required",
            "type":"dataIpv6Prefix" if self.ipv6 else "dataPrefix",
            "entries":[
                {"ipv6Prefix" if self.ipv6 else "ipPrefix":i} for i in self._entries]
        }
