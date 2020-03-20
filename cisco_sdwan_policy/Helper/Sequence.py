from cisco_sdwan_policy.BaseObject import BaseObject


class Sequence(BaseObject):

    def __init__(self,id,name,type,base_action,ip_type,match,actions,**kwargs):

        self.id = id
        self.name = name
        self.type = type
        self.baseAction = base_action
        self.ip_type=ip_type
        self.actions = actions
        self.match = match
        super().__init__(**kwargs)

    @staticmethod
    def get_list_obj(obj_id,lists):
        for obj in lists:
            if obj.id==obj_id:
                return obj
        return None

    @classmethod
    def from_json(cls,config,lists,**kwargs):
        for action in config["actions"]:
            if action.get("parameter"):
                if type(action["parameter"])==list:
                    for para in action["parameter"]:
                        if para.get("ref"):
                            resp = cls.get_list_obj(para.get("ref"),lists)
                            if resp:
                                action["parameter"][action["parameter"].index(para)]["ref"]=resp
                            else:
                                raise Exception("List not found")
            else:
                # Might be cflowd
                pass

        new_match=[]
        for match in config["match"]["entries"]:
            matched=False
            if match.get("ref"):
                resp = cls.get_list_obj(match.get("ref"), lists)
                if resp:
                    config["match"]["entries"][config["match"]["entries"].index(match)]["ref"]=resp
                else:
                    raise Exception("Undefined List found.")
        config["match"]=config["match"]["entries"]

        id = config["sequenceId"]
        name = config["sequenceName"]
        types = config["sequenceType"]
        baseAction = config.get("baseAction")
        ip_type = config.get("sequenceIpType")
        actions = config["actions"]
        match = config["match"]

        return cls(id,name,types,baseAction,ip_type,match,actions,**kwargs)

    def to_json(self):
        resp = {
              "sequenceId": self.id,
              "sequenceName": self.name,
              "baseAction": self.baseAction,
              "sequenceType": self.type,
              "match": {
                  "entries": []
              },
              "actions": []
        }
        if self.ip_type:
            resp["sequenceIpType"]=self.ip_type

        for match in self.match:
            if match.get("ref"):
                resp["match"]["entries"].append({
                    "field":match["field"],
                    "ref":match["ref"].get_id()
                })
            else:
                resp["match"]["entries"].append(match)
        for action in self.actions:
            if action.get("parameter"):
                if type(action["parameter"]) == list:
                    new_para = []
                    for para in action["parameter"]:
                        if para.get("ref"):
                            new_para.append({
                                "field": para["field"],
                                "ref": para["ref"].get_id()
                            })
                        else:
                            new_para.append(para)
                    resp["actions"].append({
                        "type":action["type"],
                        "parameter":new_para
                    })
                else:
                    resp["actions"].append(action)
            else:
                #cflowd
                resp["actions"].append(action)
        return resp

    def add_match(self,field,value):
        for matches in self.match:
            if matches["field"]==field:
                raise Exception("Duplicate field in Match.")
        if type(value) in [str,int,float]:
            self.match.append({
                "field":field,
                "value":value
            })
        else:
            self.match.append({
                "field":field,
                "ref":value
            })

    def add_action(self,action_type,field,value):
        def generate_param():
            if type(value) in [str, int, float]:
                return{
                    "field": field,
                    "value": value
                }
            else:
                return{
                    "field": field,
                    "ref": value
                }

        for action in self.actions:
            if action["type"]==action_type:
                for param in action["parameter"]:
                    if param["field"]==field:
                        raise Exception("Duplicate field in Action.")
                action["parameter"].append(generate_param())
                return True
        self.actions.append({
            "type":action_type,
            "parameter":[generate_param()]
        })

