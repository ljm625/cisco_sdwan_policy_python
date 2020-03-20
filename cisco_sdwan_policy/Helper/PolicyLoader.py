import importlib
import json

from cisco_sdwan_policy.List.Application import Application
from cisco_sdwan_policy.List.Color import Color
from cisco_sdwan_policy.List.DataPrefix import DataPrefix
from cisco_sdwan_policy.List.Policer import Policer
from cisco_sdwan_policy.List.Prefix import Prefix
from cisco_sdwan_policy.List.Site import Site
from cisco_sdwan_policy.List.SlaClass import SlaClass
from cisco_sdwan_policy.List.Tloc import Tloc
from cisco_sdwan_policy.List.Vpn import Vpn
from cisco_sdwan_policy.MainPolicy import MainPolicy
from cisco_sdwan_policy.Topology.CustomTopo import CustomTopo
from cisco_sdwan_policy.Topology.HubAndSpoke import HubAndSpoke
from cisco_sdwan_policy.Topology.Mesh import Mesh
from cisco_sdwan_policy.Topology.VpnMembership import VpnMembership
from cisco_sdwan_policy.TrafficPolicy.AppRoute import AppRoute
from cisco_sdwan_policy.TrafficPolicy.DataPolicy import DataPolicy
from cisco_sdwan_policy.ViptelaRest import ViptelaRest


class PolicyLoader(object):
    instance = None

    def __init__(self,server_info,debug=False):
        self.rest = ViptelaRest.init(server_info)
        self.list_policies = []
        self.topo_policies = []
        self.traffic_policies = []
        self.main_policies = []
        self.debug = debug

    def load(self):
        self.get_list_policies()
        self.get_topo_policies()
        self.get_traffic_policies()
        self.get_main_policies()
    
    def get_list_policies(self):
        self.list_policies=[]
        policers = self.rest.get_request("template/policy/list/policer").json()
        for policer in policers["data"]:
            pc = Policer.from_json(policer,debug=self.debug)
            if pc:
                self.list_policies.append(pc)

        vpns = self.rest.get_request("template/policy/list/vpn").json()
        for vpn in vpns["data"]:
            v = Vpn.from_json(vpn,debug=self.debug)
            if v:
                self.list_policies.append(v)

        sites = self.rest.get_request("template/policy/list/site").json()
        for site in sites["data"]:
            v = Site.from_json(site,debug=self.debug)
            if v:
                self.list_policies.append(v)

        if int(self.rest.version.split(".")[0])>=19:
            prefix_url = "template/policy/list/ipprefixall"
        else:
            prefix_url = "template/policy/list/prefix"

        prefixs = self.rest.get_request(prefix_url).json()
        for prefix in prefixs["data"]:
            v = Prefix.from_json(prefix,debug=self.debug)
            if v:
                self.list_policies.append(v)

        if int(self.rest.version.split(".")[0])>=19:
            data_prefix_url = "template/policy/list/dataprefixall"
        else:
            data_prefix_url = "template/policy/list/dataprefix"


        prefixs = self.rest.get_request(data_prefix_url).json()
        for prefix in prefixs["data"]:
            v = DataPrefix.from_json(prefix,debug=self.debug)
            if v:
                self.list_policies.append(v)

        tlocs = self.rest.get_request("template/policy/list/tloc").json()
        for tloc in tlocs["data"]:
            v = Tloc.from_json(tloc,debug=self.debug)
            if v:
                self.list_policies.append(v)

        slas = self.rest.get_request("template/policy/list/sla").json()
        for sla in slas["data"]:
            v = SlaClass.from_json(sla,debug=self.debug)
            if v:
                self.list_policies.append(v)

        apps = self.rest.get_request("template/policy/list/app").json()
        for app in apps["data"]:
            v = Application.from_json(app,debug=self.debug)
            if v:
                self.list_policies.append(v)

        colors = self.rest.get_request("template/policy/list/color").json()
        for color in colors["data"]:
            v = Color.from_json(color,debug=self.debug)
            if v:
                self.list_policies.append(v)

    def get_topo_policies(self):
        self.topo_policies=[]

        hubandspokes = self.rest.get_request("template/policy/definition/hubandspoke").json()
        for hs in hubandspokes["data"]:
            topo_info = self.rest.get_request(
                "template/policy/definition/hubandspoke/{}".format(hs["definitionId"])).json()
            res = HubAndSpoke.from_json(topo_info, self.list_policies,debug=self.debug)
            self.topo_policies.append(res)

        meshes = self.rest.get_request("template/policy/definition/mesh").json()
        for mesh in meshes["data"]:
            topo_info = self.rest.get_request(
                "template/policy/definition/mesh/{}".format(mesh["definitionId"])).json()
            res = Mesh.from_json(topo_info, self.list_policies,debug=self.debug)
            self.topo_policies.append(res)


        custom_topos = self.rest.get_request("template/policy/definition/control").json()
        for custom_topo in custom_topos["data"]:
            topo_info = self.rest.get_request(
                "template/policy/definition/control/{}".format(custom_topo["definitionId"])).json()
            res = CustomTopo.from_json(topo_info, self.list_policies,debug=self.debug)
            self.topo_policies.append(res)
            # print(res.to_json())
            # print(res.name)

        vpn_memberships = self.rest.get_request("template/policy/definition/vpnmembershipgroup").json()
        for vpn_membership in vpn_memberships["data"]:
            vpn_info = self.rest.get_request(
                "template/policy/definition/vpnmembershipgroup/{}".format(vpn_membership["definitionId"])).json()
            res = VpnMembership.from_json(vpn_info, self.list_policies,debug=self.debug)
            self.topo_policies.append(res)
            # print(res.to_json())
            # print(res.name)

    def get_traffic_policies(self):
        self.traffic_policies=[]
        app_routes = self.rest.get_request("template/policy/definition/approute").json()
        for app_route in app_routes["data"]:
            route_info = self.rest.get_request(
                "template/policy/definition/approute/{}".format(app_route["definitionId"])).json()
            res = AppRoute.from_json(route_info, self.list_policies,debug=self.debug)
            # print(res.name)
            # print(res.to_json())
            self.traffic_policies.append(res)

        datas = self.rest.get_request("template/policy/definition/data").json()
        for data in datas["data"]:
            route_info = self.rest.get_request("template/policy/definition/data/{}".format(data["definitionId"])).json()
            res = DataPolicy.from_json(route_info, self.list_policies,debug=self.debug)
            # print(res.name)
            # print(res.to_json())
            self.traffic_policies.append(res)

    def get_main_policies(self):
        self.main_policies=[]
        main_policies = self.rest.get_request("template/policy/vsmart").json()
        for policy in main_policies["data"]:
            if policy["policyType"] == "feature":
                policy_info = self.rest.get_request("template/policy/vsmart/definition/{}".format(policy["policyId"])).json()
                res = MainPolicy.from_json(policy["policyId"], policy_info, self.topo_policies, self.traffic_policies, self.list_policies,debug=self.debug)
                # print(res.name)
                self.main_policies.append(res)

    def save_to_json(self):
        output ={
            "list_policies":[i.export() for i in self.list_policies],
            "topo_policies":[i.export() for i in self.topo_policies],
            "traffic_policies":[i.export() for i in self.traffic_policies],
            "main_policies":[i.export() for i in self.main_policies]
        }
        return json.dumps(output)

    def load_from_json(self,json_file,only_ref=False):
        backup = json.loads(json_file)
        # First load in temporary variables, then determine if there's any conflict.
        list_policies = []
        topo_policies = []
        traffic_policies = []
        main_policies = []
        for i in backup["list_policies"]:
            i["listId"] = i["id"]
            cls= self.get_class("List",i["class"])
            obj = cls.from_json(i,debug=self.debug)
            list_policies.append(obj)

        for i in backup["topo_policies"]:
            i["definitionId"] = i["id"]
            cls= self.get_class("Topology",i["class"])
            obj = cls.from_json(i,list_policies,debug=self.debug)
            topo_policies.append(obj)

        for i in backup["traffic_policies"]:
            i["definitionId"] = i["id"]
            cls= self.get_class("TrafficPolicy",i["class"])
            obj = cls.from_json(i,list_policies,debug=self.debug)
            traffic_policies.append(obj)

        for i in backup["main_policies"]:
            obj = MainPolicy.from_json(i["id"],i,topo_policies,traffic_policies,list_policies,debug=self.debug)
            main_policies.append(obj)

        if only_ref:
            for i in list_policies:
                if i.name not in [j.name for j in self.list_policies]:
                    pass
                else:
                    i.name = i.name + "_1"
                i.id = None
            for i in topo_policies:
                if i.name not in [j.name for j in self.topo_policies]:
                    pass
                else:
                    i.name = i.name + "_1"
                i.id = None
            for i in traffic_policies:
                if i.name not in [j.name for j in self.traffic_policies]:
                    pass
                else:
                    i.name = i.name + "_1"
                i.id = None
            for i in main_policies:
                if i.name in [j.name for j in self.main_policies]:
                    i.name = i.name + "_1"
                i.id = None
                # Save the new policy, all the dependencies will automatically created.
                i.save()
        else:

            # Find duplicate from current vManage (Only checks the name.)
            for i in list_policies:
                if i.name not in [ j.name for j in self.list_policies]:
                    i.id=None
                    i.save()
                    self.list_policies.append(i)
                else:
                    conflict = True
                    for j in self.list_policies:
                        if i.name==j.name and i.id==j.id:
                            conflict=False
                            break
                    if conflict:
                        i.name = i.name+"_1"
                        i.id = None
                        i.save()
                        self.list_policies.append(i)
            for i in topo_policies:
                if i.name not in [ j.name for j in self.topo_policies]:
                    i.id=None
                    i.save()
                    self.topo_policies.append(i)
                else:
                    conflict = True
                    for j in self.topo_policies:
                        if i.name==j.name and i.id==j.id:
                            conflict=False
                            break
                    if conflict:
                        i.name = i.name+"_1"
                        i.id = None
                        i.save()
                        self.topo_policies.append(i)

            for i in traffic_policies:
                if i.name not in [ j.name for j in self.traffic_policies]:
                    i.id=None
                    i.save()
                    self.traffic_policies.append(i)
                else:
                    conflict = True
                    for j in self.traffic_policies:
                        if i.name==j.name and i.id==j.id:
                            conflict=False
                            break
                    if conflict:
                        i.name = i.name+"_1"
                        i.id = None
                        i.save()
                        self.traffic_policies.append(i)

            for i in main_policies:
                if i.name not in [ j.name for j in self.main_policies]:
                    i.id=None
                    i.save()
                    self.main_policies.append(i)
                else:
                    conflict = True
                    for j in self.main_policies:
                        if i.name==j.name and i.id==j.id:
                            conflict=False
                            break
                    if conflict:
                        i.name = i.name+"_1"
                        i.id = None
                        i.save()
                        self.main_policies.append(i)

    @staticmethod
    def get_class(module_name, class_name):
        # load the module, will raise ImportError if module cannot be loaded
        m = importlib.import_module("cisco_sdwan_policy.{}.{}".format(module_name, class_name))
        # get the class, will raise AttributeError if class cannot be found
        c = getattr(m, class_name)
        return c

    @classmethod
    def init(cls,server_info=None):
        if cls.instance:
            return cls.instance
        else:
            cls.instance = cls(server_info)
            return cls.instance