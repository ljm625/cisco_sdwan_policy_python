from cisco_sdwan_policy.BaseObject import BaseObject
from cisco_sdwan_policy.Helper.Sequence import Sequence


class MainPolicy(BaseObject):

    def __init__(self,name,description,control_policy_list,data_policy_list,vpn_membership_list,approute_policy_list,id=None,activated=False,**kwargs):
        self.id = id
        self.name = name
        self.description=description
        self.type="feature"
        self.vpnMembershipGroup = vpn_membership_list
        self.control = control_policy_list
        self.data = data_policy_list
        self.approute = approute_policy_list
        self.activated = activated
        self.url="template/policy/vsmart"
        super().__init__(**kwargs)

    @staticmethod
    def get_list_obj(obj_id,lists):
        for obj in lists:
            if obj.id==obj_id:
                return obj
        raise Exception("{} Not Found".format(obj_id))

    def add_control_policy(self,control_policy,in_sites,out_sites):
        self.control.append({
            "policy":control_policy,
            "in":in_sites,
            "out":out_sites
        })
        pass

    def add_data_policy(self,data_policy,direction,sites,vpns):
        for policy in self.data:
            if policy.name == data_policy:
                policy[direction]["site"].extend(sites)
                policy[direction]["vpn"].extend(vpns)
                return True
        self.data.append({
            "policy": data_policy,
            "service": {
                        "site":[],
                        "vpn":[]
                    },
            "tunnel": {
                        "site":[],
                        "vpn":[]
                    },
            "all": {
                        "site":[],
                        "vpn":[]
                    }

        })
        self.data[-1][direction]["site"].extend(sites)
        self.data[-1][direction]["vpn"].extend(vpns)
        return True

    def add_approute_policy(self,approute_policy,sites,vpns):
        for policy in self.approute:
            if policy.name == approute_policy:
                policy["entries"].append({
                    "site": sites,
                    "vpn": vpns
                })
                return True
        self.approute.append({
            "policy": approute_policy,
            "entries": [{
                "site": sites,
                "vpn": vpns
            }],
        })
        return True

    def add_vpnmembership_policy(self,vpnmembership_policy):
        if vpnmembership_policy in self.vpnMembershipGroup:
            return False
        else:
            self.vpnMembershipGroup.append(vpnmembership_policy)
            return True




    def to_json(self):
        """
        Print json for REST API calls
        :return:
        """
        resp = {
            "policyDescription": self.description,
            "policyType": "feature",
            "policyName": self.name,
            "isPolicyActivated": self.activated,
            "policyDefinition": {
                "assembly": [
                ]
                }
            }
        for control in self.control:
            tmp  = {
                "type": "control",
                "entries": [
                ]
            }
            sites=[]
            for in_site in control["in"]:
                sites.append(in_site.get_id())
            if sites:
                tmp["entries"].append({
                        "direction": "in",
                        "siteLists": sites
                })
            sites=[]
            for out_site in control["out"]:
                sites.append(out_site.get_id())
            if sites:
                tmp["entries"].append({
                        "direction": "out",
                        "siteLists": sites
                })
            # control["policy"].get_id()
            tmp["definitionId"]=control["policy"].get_id()
            assert type(tmp["definitionId"])==str
            resp["policyDefinition"]["assembly"].append(tmp)
        # Data Policy
        for data in self.data:
            tmp  = {
                "type": "data",
                "entries": [
                ]
            }
            if data["service"]["site"] or data["service"]["vpn"]:
                tmp2={
                        "direction": "service",
                        "siteLists": [
                        ],
                        "vpnLists": [
                        ]
                    }
                for site in data["service"]["site"]:
                    tmp2["siteLists"].append(site.get_id())
                for vpn in data["service"]["vpn"]:
                    tmp2["vpnLists"].append(vpn.get_id())
                tmp["entries"].append(tmp2)
            if data["tunnel"]["site"] or data["tunnel"]["vpn"]:
                tmp2={
                        "direction": "tunnel",
                        "siteLists": [
                        ],
                        "vpnLists": [
                        ]
                    }
                for site in data["tunnel"]["site"]:
                    tmp2["siteLists"].append(site.get_id())
                for vpn in data["tunnel"]["vpn"]:
                    tmp2["vpnLists"].append(vpn.get_id())
                tmp["entries"].append(tmp2)
            if data["all"]["site"] or data["all"]["vpn"]:
                tmp2={
                        "direction": "all",
                        "siteLists": [
                        ],
                        "vpnLists": [
                        ]
                    }
                for site in data["all"]["site"]:
                    tmp2["siteLists"].append(site.get_id())
                for vpn in data["all"]["vpn"]:
                    tmp2["vpnLists"].append(vpn.get_id())
                tmp["entries"].append(tmp2)
            tmp["definitionId"]=data["policy"].get_id()
            resp["policyDefinition"]["assembly"].append(tmp)
        # AppRoute
        for approute in self.approute:
            tmp  = {
                "type": "appRoute",
                "entries": []
            }
            for entry in approute["entries"]:
                tmp_entry = {
                    "siteLists": [
                    ],
                    "vpnLists": [
                    ]
                }
                for site in entry["sites"]:
                    tmp_entry["siteLists"].append(site.get_id())
                for vpn in entry["vpns"]:
                    tmp_entry["vpnLists"].append(vpn.get_id())
                tmp["entries"].append(tmp_entry)

            tmp["definitionId"]=approute["policy"].get_id()
            resp["policyDefinition"]["assembly"].append(tmp)
        for vpnMembershipGroup in self.vpnMembershipGroup:
            resp["policyDefinition"]["assembly"].append({
                "definitionId": vpnMembershipGroup.get_id(),
                "type": "vpnMembershipGroup"
            })
        return resp

    @classmethod
    def from_json(cls,id,json_info,topo_list,traffic_list,lists,**kwargs):
        """
        Generate object from JSON.
        :return:
        """
        vpnMembershipGroup=[]
        control = []
        data = []
        approute=[]
        for policy in json_info["policyDefinition"]["assembly"]:
            if policy["type"]=="vpnMembershipGroup":
                # pass
                result = cls.get_list_obj(policy["definitionId"],topo_list)
                if result:
                    vpnMembershipGroup.append(result)
                else:
                    raise Exception("VPN Membership Group Not found.")
            elif policy["type"]=="control":
                result = cls.get_list_obj(policy["definitionId"],topo_list)
                if result:
                    site_out=[]
                    site_in=[]
                    for entry in policy["entries"]:
                        if entry["direction"]=="out":
                            for site in entry["siteLists"]:
                                site_out.append(cls.get_list_obj(site, lists))
                        elif entry["direction"]=="in":
                            for site in entry["siteLists"]:
                                site_in.append(cls.get_list_obj(site, lists))
                    resp = {
                        "policy":result,
                        "out":site_out,
                        "in":site_in
                    }
                    control.append(resp)
                else:
                    raise Exception("Control Group Not found.")
            elif policy["type"]=="data":
                result = cls.get_list_obj(policy["definitionId"],traffic_list)
                if result:
                    service={
                        "site":[],
                        "vpn":[]
                    }
                    tunnel={
                        "site":[],
                        "vpn":[]
                    }
                    all = {
                        "site": [],
                        "vpn": []
                    }
                    for entry in policy["entries"]:
                        if entry["direction"]=="service":
                            for site in entry["siteLists"]:
                                service["site"].append(cls.get_list_obj(site, lists))
                            for vpn in entry["vpnLists"]:
                                service["vpn"].append(cls.get_list_obj(vpn, lists))
                        elif entry["direction"] == "tunnel":
                            for site in entry["siteLists"]:
                                tunnel["site"].append(cls.get_list_obj(site, lists))
                            for vpn in entry["vpnLists"]:
                                tunnel["vpn"].append(cls.get_list_obj(vpn, lists))
                        elif entry["direction"] == "all":
                            for site in entry["siteLists"]:
                                all["site"].append(cls.get_list_obj(site, lists))
                            for vpn in entry["vpnLists"]:
                                all["vpn"].append(cls.get_list_obj(vpn, lists))

                    resp = {
                        "policy":result,
                        "service":service,
                        "tunnel":tunnel,
                        "all":all
                    }
                    data.append(resp)
                else:
                    raise Exception("Control Group Not found.")
            elif policy["type"]=="appRoute":
                result = cls.get_list_obj(policy["definitionId"],traffic_list)
                if result:
                    entries = []
                    for entry in policy["entries"]:
                        tmp = {
                            "sites": [],
                            "vpns": []
                        }

                        for site in entry["siteLists"]:
                            tmp["sites"].append(cls.get_list_obj(site, lists))
                        for vpn in entry["vpnLists"]:
                            tmp["vpns"].append(cls.get_list_obj(vpn, lists))
                        entries.append(tmp)
                    resp = {
                        "policy":result,
                        "entries":entries,
                    }
                    approute.append(resp)
                else:
                    raise Exception("AppRoute Group Not found.")

        name = json_info["policyName"]
        description=json_info["policyDescription"]
        activated = json_info["isPolicyActivated"]

        return cls(name,description,control,data,vpnMembershipGroup,approute,id,activated,**kwargs)
