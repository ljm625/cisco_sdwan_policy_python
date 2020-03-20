import json

from cisco_sdwan_policy.BaseObject import BaseObject


class SlaClass(BaseObject):

    def __init__(self,name,latency,loss,jitter,id=None,reference=None,**kwargs):
        self.type = "slaList"
        self.id = id
        self.name = name
        self.references = reference
        self.latency = latency
        self.loss = loss
        self.jitter = jitter
        self.url = "template/policy/list/sla"
        super().__init__(**kwargs)
        self.modified=False


    @classmethod
    def from_json(cls,config,**kwargs):
        id = config["listId"]
        name = config["name"]
        references = config.get("references")
        latency = config["entries"][0]["latency"]
        loss = config["entries"][0]["loss"]
        jitter = config["entries"][0]["jitter"]

        return cls(name,latency,loss,jitter,id,references,**kwargs)

    def to_json(self):
        # {"name": "test", "description": "Desc Not Required", "type": "sla",
        #  "entries": [{"latency": "100", "loss": "1", "jitter": "1"}]}
        return {
            "name":self.name,
            "description":"Desc Not Required",
            "type":"sla",
            "entries":[{"latency": self.latency, "loss": self.loss, "jitter": self.jitter}]
        }


