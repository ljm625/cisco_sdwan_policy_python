import json

from cisco_sdwan_policy.BaseObject import BaseObject


class Policer(BaseObject):

    def __init__(self,name,rate,exceed,burst,id=None,reference=None,**kwargs):
        self.type = "policerList"
        self.id = id
        self.name = name
        self.references = reference
        self.burst = burst
        self.exceed = exceed
        self.rate = rate
        self.url = "template/policy/list/policer"
        super().__init__(**kwargs)
        self.modified=False



    @classmethod
    def from_json(cls,config,**kwargs):
        id = config["listId"]
        name = config["name"]
        references = config.get("references")
        burst = config["entries"][0]["burst"]
        exceed = config["entries"][0]["exceed"]
        rate = config["entries"][0]["rate"]

        return cls(name,rate,exceed,burst,id,references,**kwargs)

    def to_json(self):
        return {
            "name":self.name,
            "description":"Desc Not Required",
            "type":"policer",
            "entries":[{"burst": self.burst, "exceed": self.exceed, "rate": self.rate}]
        }

