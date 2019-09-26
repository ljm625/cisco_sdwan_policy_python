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
from cisco_sdwan_policy.Topology.VpnMembership import VpnMembership
from cisco_sdwan_policy.TrafficPolicy.AppRoute import AppRoute
from cisco_sdwan_policy.TrafficPolicy.DataPolicy import DataPolicy
from cisco_sdwan_policy.ViptelaRest import ViptelaRest


class PolicyLoader(object):
    instance = None

    def __init__(self,server_info):
        self.rest = ViptelaRest.init(server_info)
        self.list_policies = []
        self.topo_policies = []
        self.traffic_policies = []
        self.main_policies = []

    def load(self):
        self.get_list_policies()
        self.get_topo_policies()
        self.get_traffic_policies()
        self.get_main_policies()
    
    def get_list_policies(self):
        self.list_policies=[]
        policers = self.rest.get_request("template/policy/list/policer").json()
        for policer in policers["data"]:
            pc = Policer.from_json(policer)
            self.list_policies.append(pc)

        vpns = self.rest.get_request("template/policy/list/vpn").json()
        for vpn in vpns["data"]:
            v = Vpn.from_json(vpn)
            self.list_policies.append(v)

        sites = self.rest.get_request("template/policy/list/site").json()
        for site in sites["data"]:
            v = Site.from_json(site)
            self.list_policies.append(v)

        prefixs = self.rest.get_request("template/policy/list/ipprefixall").json()
        for prefix in prefixs["data"]:
            v = Prefix.from_json(prefix)
            self.list_policies.append(v)

        prefixs = self.rest.get_request("template/policy/list/dataprefixall").json()
        for prefix in prefixs["data"]:
            v = DataPrefix.from_json(prefix)
            self.list_policies.append(v)

        tlocs = self.rest.get_request("template/policy/list/tloc").json()
        for tloc in tlocs["data"]:
            v = Tloc.from_json(tloc)
            self.list_policies.append(v)

        slas = self.rest.get_request("template/policy/list/sla").json()
        for sla in slas["data"]:
            v = SlaClass.from_json(sla)
            self.list_policies.append(v)

        apps = self.rest.get_request("template/policy/list/app").json()
        for app in apps["data"]:
            v = Application.from_json(app)
            self.list_policies.append(v)

        colors = self.rest.get_request("template/policy/list/color").json()
        for color in colors["data"]:
            v = Color.from_json(color)
            self.list_policies.append(v)

    def get_topo_policies(self):
        self.topo_policies=[]

        custom_topos = self.rest.get_request("template/policy/definition/control").json()
        for custom_topo in custom_topos["data"]:
            topo_info = self.rest.get_request(
                "template/policy/definition/control/{}".format(custom_topo["definitionId"])).json()
            res = CustomTopo.from_json(topo_info, self.list_policies)
            self.topo_policies.append(res)
            # print(res.to_json())
            # print(res.name)

        vpn_memberships = self.rest.get_request("template/policy/definition/vpnmembershipgroup").json()
        for vpn_membership in vpn_memberships["data"]:
            vpn_info = self.rest.get_request(
                "template/policy/definition/vpnmembershipgroup/{}".format(vpn_membership["definitionId"])).json()
            res = VpnMembership.from_json(vpn_info, self.list_policies)
            self.topo_policies.append(res)
            # print(res.to_json())
            # print(res.name)

    def get_traffic_policies(self):
        self.traffic_policies=[]
        app_routes = self.rest.get_request("template/policy/definition/approute").json()
        for app_route in app_routes["data"]:
            route_info = self.rest.get_request(
                "template/policy/definition/approute/{}".format(app_route["definitionId"])).json()
            res = AppRoute.from_json(route_info, self.list_policies)
            # print(res.name)
            # print(res.to_json())
            self.traffic_policies.append(res)

        datas = self.rest.get_request("template/policy/definition/data").json()
        for data in datas["data"]:
            route_info = self.rest.get_request("template/policy/definition/data/{}".format(data["definitionId"])).json()
            res = DataPolicy.from_json(route_info, self.list_policies)
            # print(res.name)
            # print(res.to_json())
            self.traffic_policies.append(res)

    def get_main_policies(self):
        self.main_policies=[]
        main_policies = self.rest.get_request("template/policy/vsmart").json()
        for policy in main_policies["data"]:
            if policy["policyType"] == "feature":
                policy_info = self.rest.get_request("template/policy/vsmart/definition/{}".format(policy["policyId"])).json()
                res = MainPolicy.from_json(policy["policyId"], policy_info, self.topo_policies, self.traffic_policies, self.list_policies)
                # print(res.name)
                self.main_policies.append(res)

    @classmethod
    def init(cls,server_info=None):
        if cls.instance:
            return cls.instance
        else:
            cls.instance = cls(server_info)
            return cls.instance