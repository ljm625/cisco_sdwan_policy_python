import copy

from cisco_sdwan_policy.BaseObject import BaseObject
from cisco_sdwan_policy.Helper.Sequence import Sequence


class HubAndSpoke(BaseObject):

    def __init__(self,name,description,vpn,topos,id=None,references=None,**kwargs):
        self.id = id
        self.name = name
        self.type = "hubAndSpoke"
        self.description = description
        self.references = references
        self.vpn =vpn
        self._topos =topos
        # config["defaultAction"]["type"]
        self.url = "template/policy/definition/hubandspoke"
        super().__init__(**kwargs)
        self.modified=False

    @staticmethod
    def get_list_obj(obj_id,lists):
        for obj in lists:
            if obj.id==obj_id:
                return obj
        raise Exception("Can't find list {}".format(obj_id))

    def add_topology(self,name,spokes,hubs,advertise_tloc=False,equal_preference=True,tloc= None):
        spoke_list= []
        for spoke in spokes:
            spoke_list.append( {
                        "siteList": spoke,
                        "hubs": [
                            {
                                "siteList": hubs,
                                "prefixLists": [],
                                "ipv6PrefixLists": []
                            }
                        ]
                    })
        topo = {
                "name": name,
                "equalPreference": equal_preference,
                "advertiseTloc": advertise_tloc,
                "spokes": spoke_list,
            }
        if advertise_tloc and tloc:
            topo["tlocList"]=tloc

        self._topos.append(topo)
        self.modified=True

    def add_prefix(self,name,spoke,hub,prefix_list,ipv6=False):
        for topo in self._topos:
            if topo["name"]==name:
                for spokes in topo["spokes"]:
                    if spokes["siteList"]==spoke:
                        for hubs in spokes["hubs"]:
                            if hubs["siteList"]==hub:
                                if ipv6:
                                    if prefix_list not in hubs["ipv6PrefixLists"]:
                                        hubs["ipv6PrefixLists"].append(prefix_list)
                                        self.modified=True
                                else:
                                    if prefix_list not in hubs["prefixLists"]:
                                        hubs["prefixLists"].append(prefix_list)
                                        self.modified=True


    def to_json(self):
        """
        Print json for REST API calls
        :return:
        """
        subdefs = []

        for topo in self._topos:
            tmp = copy.copy(topo)
            if tmp.get("tlocList"):
                tmp["tlocList"]=tmp["tlocList"].get_id()
            for spoke in tmp["spokes"]:
                spoke["siteList"]=spoke["siteList"].get_id()
                for hub in spoke["hubs"]:
                    hub["siteList"]=hub["siteList"].get_id()
                    for i in range(0,len(hub["prefixLists"])):
                        hub["prefixLists"][i] = hub["prefixLists"][i].get_id()
                    for i in range(0,len(hub["ipv6PrefixLists"])):
                        hub["ipv6PrefixLists"][i] = hub["ipv6PrefixLists"][i].get_id()
            subdefs.append(tmp)

        return {
            "name": self.name,
            "type": self.type,
            "description": self.description,
            "definition":{
                "vpnList": self.vpn.get_id(),
                "subDefinitions": subdefs
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
        for topo in config["definition"]["subDefinitions"]:
            for spoke in topo["spokes"]:
                spoke["siteList"]= cls.get_list_obj(spoke["siteList"],lists)
                for hub in spoke["hubs"]:
                    hub["siteList"] = cls.get_list_obj(hub["siteList"], lists)
                    for i in range(0,len(hub["prefixLists"])):
                        hub["prefixLists"][i] = cls.get_list_obj(hub["prefixLists"][i], lists)
                    if hub.get("ipv6PrefixLists"):
                        for i in range(0,len(hub["ipv6PrefixLists"])):
                            hub["ipv6PrefixLists"][i] = cls.get_list_obj(hub["ipv6PrefixLists"][i], lists)
                    else:
                        hub["ipv6PrefixLists"]=[]
            if topo.get("tlocList"):
                topo["tlocList"]=cls.get_list_obj(topo["tlocList"],lists)
            topos.append(topo)
        return cls(name,description,vpn,topos,id,references,**kwargs)