import copy

from cisco_sdwan_policy.BaseObject import BaseObject


class QosMap(BaseObject):

    def __init__(self,name,description,rewrite_rules=[],id=None,references=None,**kwargs):
        self.id = id
        self.name = name
        self.type = "rewriteRule"
        self.description = description
        self.references = references
        # config["defaultAction"]["type"]
        self._rewrite_rules = rewrite_rules
        self.url = "template/policy/definition/rewriterule"
        super().__init__(**kwargs)
        self.modified=False


    @staticmethod
    def get_list_obj(obj_id,lists):
        for obj in lists:
            if obj.id==obj_id:
                return obj
        raise Exception("Can't find list {}".format(obj_id))


    # TODO: Implement add & modify QosMap




    def to_json(self):
        """
        Print json for REST API calls
        :return:
        """
        resp = {
            "name": self.name,
            "type": self.type,
            "description": self.description,
            "definition": {
                "rules": []
            }
        }
        for rewrite_rule in self._rewrite_rules:
            tmp_rule = copy.copy(rewrite_rule)
            if type(tmp_rule["class"])!=str:
                tmp_rule["class"]=tmp_rule["class"].get_id()
            resp["definition"]["rules"].append(tmp_rule)

        return resp


    @classmethod
    def from_json(cls,config,lists,**kwargs):
        """
        Generate object from JSON.
        :return:
        """
        id = config["definitionId"]
        name = config["name"]
        description = config["description"]
        references = config.get("references")
        for rule in config["definition"]["rules"]:
            if rule["class"]!= "":
                rule["class"] = cls.get_list_obj(rule["class"],lists)
        rewrite_rules = config["definition"]["rules"]
        return cls(name,description,rewrite_rules,id,references,**kwargs)

        pass