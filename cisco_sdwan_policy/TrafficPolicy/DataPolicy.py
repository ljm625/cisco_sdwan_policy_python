from cisco_sdwan_policy.BaseObject import BaseObject
from cisco_sdwan_policy.Helper.Sequence import Sequence


class DataPolicy(BaseObject):

    def __init__(self,name,description,sequences,default_action=None,id=None,references=None,**kwargs):
        self.id = id
        self.description= description
        self.name = name
        self.references = references
        # if config.get("defaultAction"):
        #     if type(config["defaultAction"])==dict:
        #         self.defaultAction = config["defaultAction"]["type"]
        #     else:
        #         self.defaultAction = config["defaultAction"]
        # else:
        self.default_action = default_action
        self._sequence = sequences
        self.url = "template/policy/definition/data"
        super().__init__(**kwargs)
        self.modified=False




    def to_json(self):
        """
        Print json for REST API calls
        :return:
        """
        resp = {
            "name": self.name,
            "type": "data",
            "description": self.description,
            "sequences": [i.to_json() for i in self._sequence]
        }


        if type(self.default_action)==str:
            default_action={
                "type":self.default_action
            }
        elif not self.default_action:
            default_action=None
        else:
            default_action = {
                "type":self.default_action.type,
                "ref":self.default_action.get_id()
            }
        if default_action:
            resp["defaultAction"]=default_action
        return resp

    @classmethod
    def from_json(cls,json_info,lists,**kwargs):
        """
        Generate object from JSON.
        :return:
        """
        new_sequence=[]
        for sequence in json_info["sequences"]:
            tmp = Sequence.from_json(sequence,lists)
            new_sequence.append(tmp)
        json_info["sequences"] = new_sequence

        id = json_info["definitionId"]
        description=json_info["description"]
        name = json_info["name"]
        references = json_info.get("references")
        if json_info.get("defaultAction"):
            if type(json_info["defaultAction"])==dict:
                defaultAction = json_info["defaultAction"]["type"]
            else:
                defaultAction = json_info["defaultAction"]
        else:
            defaultAction = None
        sequence = json_info["sequences"]


        return cls(name,description,sequence,defaultAction,id,references,**kwargs)