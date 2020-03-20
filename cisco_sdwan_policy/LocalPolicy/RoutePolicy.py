from cisco_sdwan_policy.BaseObject import BaseObject
from cisco_sdwan_policy.Helper.Sequence import Sequence


class RoutePolicy(BaseObject):

    def __init__(self,name,description,default_action,senquences,id=None,references=None,**kwargs):
        self.id = id
        self.name = name
        self.description = description
        self.references = references
        self.defaultAction = default_action
        # config["defaultAction"]["type"]
        self.type = "vedgeRoute"
        self._sequence = senquences
        self.url = "template/policy/definition/vedgeroute"
        super().__init__(**kwargs)
        self.modified=False




    def to_json(self):
        """
        Print json for REST API calls
        :return:
        """
        return {
            "name": self.name,
            "type": self.type,
            "description": self.description,
            "defaultAction": {
                "type": self.defaultAction
            },
            "sequences": [ i.to_json() for i in self._sequence ]
        }
                # {
                #     "sequenceId": 1,
                #     "sequenceName": "Access Control List",
                #     "baseAction": "accept",
                #     "sequenceType": "acl",
                #     "sequenceIpType": "ipv4",
                #     "match": {
                #         "entries": [
                #             {
                #                 "field": "sourceDataPrefixList",
                #                 "ref": "f1403abf-e964-4bb4-9adc-4d2ca8fd391c"
                #             }
                #         ]
                #     },
                #     "actions": [
                #         {
                #             "type": "class",
                #             "parameter": {
                #                 "ref": "f3c7d739-9bd3-4698-a214-8650afa7a224"
                #             }
                #         }
                #     ]
                # }

        # return {
        #     "name": self.name,
        #     "type": "control",
        #     "description": self.description,
        #     "defaultAction": {
        #         "type": self.defaultAction
        #     },
        #     "sequences":[i.to_json() for i in self._sequence]
        # }

    @classmethod
    def from_json(cls,config,lists,**kwargs):
        """
        Generate object from JSON.
        :return:
        """
        new_sequence=[]
        for sequence in config["sequences"]:
            tmp = Sequence.from_json(sequence,lists)
            new_sequence.append(tmp)
        config["sequences"] = new_sequence

        id = config["definitionId"]
        name = config["name"]
        description = config["description"]
        references = config.get("references")
        defaultAction = config["defaultAction"]["type"]
        sequence = config["sequences"]
        return cls(name,description,defaultAction,sequence,id,references,**kwargs)

        pass