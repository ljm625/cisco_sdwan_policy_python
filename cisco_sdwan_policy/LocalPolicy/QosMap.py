import copy

from cisco_sdwan_policy.BaseObject import BaseObject


class QosMap(BaseObject):

    def __init__(self,name,description,qos_queues=[],id=None,references=None,**kwargs):
        self.id = id
        self.name = name
        self.type = "qosMap"
        self.description = description
        self.references = references
        # config["defaultAction"]["type"]
        self._qos_queues = qos_queues
        self.url = "template/policy/definition/qosmap"
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
                "qosSchedulers": []
            }
        }
        for qos_queue in self._qos_queues:
            tmp_qos = copy.copy(qos_queue)
            if type(tmp_qos["classMapRef"])!=str:
                tmp_qos["classMapRef"]=tmp_qos["classMapRef"].get_id()
            resp["definition"]["qosSchedulers"].append(tmp_qos)

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
        for qos in config["definition"]["qosSchedulers"]:
            if qos["classMapRef"]!= "":
                qos["classMapRef"] = cls.get_list_obj(qos["classMapRef"],lists)
        qos_queues = config["definition"]["qosSchedulers"]
        return cls(name,description,qos_queues,id,references,**kwargs)

        pass