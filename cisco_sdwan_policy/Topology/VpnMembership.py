from cisco_sdwan_policy.BaseObject import BaseObject
from cisco_sdwan_policy.Helper.Sequence import Sequence


class VpnMembership(BaseObject):

    def __init__(self,name,description,entries,id=None,references=None,**kwargs):
        self.id = id
        self.description = description
        self.name = name
        self.references = references
        self._sites = entries
        self.url = "template/policy/definition/vpnmembershipgroup"
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
        sites_json = []
        for site in self._sites:
            tmp_site={}
            if type(site["siteList"])==list:
                tmp = []
                for s in site["siteList"]:
                    tmp.append(s.get_id())
                if len(tmp)==1:
                    tmp_site["siteList"]=tmp[0]
                else:
                    tmp_site["siteList"]=tmp
            else:
                tmp_site["siteList"]=site["siteList"].get_id()
            if type(site["vpnList"])==list:
                tmp = []
                for s in site["vpnList"]:
                    tmp.append(s.get_id())
                tmp_site["vpnList"]=tmp
            else:
                tmp_site["vpnList"]=site["vpnList"].get_id()
            sites_json.append(tmp_site)

        return {
            "name": self.name,
            "type": "vpnMembershipGroup",
            "description": self.description,
            "definition": {
                "sites": sites_json
            }
        }

    @classmethod
    def from_json(cls,json_info,lists,**kwargs):
        """
        Generate object from JSON.
        Actually SiteList is not a list...
        :return:
        """

        for site in json_info["definition"]["sites"]:
            if type(site["siteList"])==list:
                tmp=[]
                for s in site["siteList"]:
                    tmp.append(cls.get_list_obj(s,lists))
                site["siteList"]=tmp
            elif type(site["siteList"])==str:
                site["siteList"]=[cls.get_list_obj(site["siteList"],lists)]
            else:
                raise Exception("Unexpected Type")
            if type(site["vpnList"])==list:
                tmp=[]
                for s in site["vpnList"]:
                    tmp.append(cls.get_list_obj(s,lists))
                site["vpnList"]=tmp
            elif type(site["vpnList"])==str:
                site["vpnList"]=cls.get_list_obj(site["vpnList"],lists)
            else:
                raise Exception("Unexpected Type")
        json_info["sites"]=json_info["definition"]["sites"]

        id = json_info["definitionId"]
        description = json_info["description"]
        name = json_info["name"]
        references = json_info.get("references")
        sites = json_info["sites"]

        return cls(name,description,sites,id,references,**kwargs)

