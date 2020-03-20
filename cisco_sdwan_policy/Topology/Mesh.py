import copy

from cisco_sdwan_policy.BaseObject import BaseObject
from cisco_sdwan_policy.Helper.Sequence import Sequence


class Mesh(BaseObject):

    def __init__(self,name,description,vpn,topos,id=None,references=None,**kwargs):
        self.id = id
        self.name = name
        self.type = "mesh"
        self.description = description
        self.references = references
        self.vpn =vpn
        self._topos =topos
        # config["defaultAction"]["type"]
        self.url = "template/policy/definition/mesh"
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
        topos = []

        for topo in self._topos:
            tmp = {
                "name":topo["name"],
                "siteLists":[i.get_id() for i in  topo["sites"]]
            }
            topos.append(tmp)

        return {
                "name": self.name,
                "type": "mesh",
                "description": self.description,
                "definition": {
                    "vpnList": self.vpn.get_id(),
                    "regions": topos
                }
            }

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
        vpn = cls.get_list_obj(config["definition"]["vpnList"],lists)
        topos = []
        for topo in config["definition"]["regions"]:
            tmp={
                "name":topo["name"],
                "sites":[cls.get_list_obj(i,lists) for i in topo["siteLists"]]
            }
            topos.append(tmp)
        return cls(name,description,vpn,topos,id,references,**kwargs)

    def add_topology(self,name,site_list):
        assert type(site_list)==list
        for topo in self._topos:
            if topo.name==name:
                raise Exception("Duplicate Name on Mesh Topo found.")
        self._topos.append({
            "name":name,
            "sites":site_list
        })
        self.modified=True