from cisco_sdwan_policy.BaseObject import BaseObject
from cisco_sdwan_policy.Helper.Sequence import Sequence


class AppRoute(BaseObject):

    def __init__(self,name,description,sequences,default_action=None,id=None,references=None,**kwargs):
        self.id = id
        self.name = name
        self.references = references
        self.description = description
        # if default_action:
        self.default_action=default_action
            # if type(default_action)==str:
            #     self.defaultAction
            #     self.defaultAction = config["defaultAction"]["type"]
            # else:
            #     self.defaultAction = config["defaultAction"]
        # else:
        #     self.defaultAction = None
        self._sequence = sequences

        self.url = "template/policy/definition/approute"
        super().__init__(**kwargs)
        self.modified=False



    @staticmethod
    def get_list_obj(obj_id,lists):
        for obj in lists:
            if obj.id==obj_id:
                return obj
        raise Exception("Can't find list {}".format(obj_id))


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
        if json_info.get("defaultAction") and json_info["defaultAction"].get("ref"):
            json_info["defaultAction"] = cls.get_list_obj(json_info["defaultAction"].get("ref"),lists)

        id = json_info["definitionId"]
        name = json_info["name"]
        references = json_info.get("references")
        description = json_info["description"]
        if json_info.get("defaultAction"):
            if type(json_info["defaultAction"])==dict:
                defaultAction = json_info["defaultAction"]["type"]
            else:
                defaultAction = json_info["defaultAction"]
        else:
            defaultAction = None
        sequences = json_info["sequences"]
        return cls(name,description,sequences,defaultAction,id,references,**kwargs)
