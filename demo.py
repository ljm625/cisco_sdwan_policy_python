import json

from Helper.Sequence import Sequence
from List.Application import Application
from List.Color import Color
from List.DataPrefix import DataPrefix
from List.Prefix import Prefix
from List.Policer import Policer
from List.Site import Site
from List.Tloc import Tloc
from List.Vpn import Vpn
from MainPolicy import MainPolicy
from Topology.CustomTopo import CustomTopo
from Topology.VpnMembership import VpnMembership
from TrafficPolicy.AppRoute import AppRoute
from TrafficPolicy.DataPolicy import DataPolicy
from ViptelaRest import ViptelaRest
policy_list = []
topo_list = []
traffic_policy_list=[]
main_policy_list=[]


def policy_loader(server_info):
    rest = ViptelaRest.init(server_info)
    # resp = rest.post_request("template/policy/vsmart/",json.loads('{"policyDescription":"zxzxzxz","policyType":"feature","policyName":"sssss","policyDefinition":{"assembly":[{"definitionId":"725381e6-4cb4-41ce-aae2-34033727938f","type":"vpnMembershipGroup"}]},"isPolicyActivated":false}'))
    # result=rest.get_request("template/policy/vsmart")
    policers = rest.get_request("template/policy/list/policer").json()
    for policer in policers["data"]:
        pc = Policer.from_json(policer)
        policy_list.append(pc)

    vpns = rest.get_request("template/policy/list/vpn").json()
    for vpn in vpns["data"]:
        v = Vpn.from_json(vpn)
        policy_list.append(v)

    sites = rest.get_request("template/policy/list/site").json()
    for site in sites["data"]:
        v = Site.from_json(site)
        policy_list.append(v)

    prefixs = rest.get_request("template/policy/list/ipprefixall").json()
    for prefix in prefixs["data"]:
        v = Prefix.from_json(prefix)
        policy_list.append(v)
        if v.name=="InfrastructureRoutes":
            v.name="InfrastructureRoutes1"
            v.update(v.url,v.to_json())

    prefixs = rest.get_request("template/policy/list/dataprefixall").json()
    for prefix in prefixs["data"]:
        v = DataPrefix.from_json(prefix)
        policy_list.append(v)

    tlocs = rest.get_request("template/policy/list/tloc").json()
    for tloc in tlocs["data"]:
        v = Tloc.from_json(tloc)
        policy_list.append(v)

    slas = rest.get_request("template/policy/list/sla").json()
    for sla in slas["data"]:
        v = Tloc.from_json(sla)
        policy_list.append(v)

    apps = rest.get_request("template/policy/list/app").json()
    for app in apps["data"]:
        v = Application.from_json(app)
        print(v.to_json())
        policy_list.append(v)


    colors = rest.get_request("template/policy/list/color").json()
    for color in colors["data"]:
        v = Color.from_json(color)
        print(v.to_json())
        policy_list.append(v)




    # for item in policy_list:
    #     print("{} {} {}".format(item.type,item.name,item.id))

    custom_topos = rest.get_request("template/policy/definition/control").json()
    for custom_topo in custom_topos["data"]:
        topo_info = rest.get_request("template/policy/definition/control/{}".format(custom_topo["definitionId"])).json()
        res = CustomTopo.from_json(topo_info,policy_list)
        topo_list.append(res)
        # print(res.to_json())
        # print(res.name)

    vpn_memberships = rest.get_request("template/policy/definition/vpnmembershipgroup").json()
    for vpn_membership in vpn_memberships["data"]:
        vpn_info = rest.get_request("template/policy/definition/vpnmembershipgroup/{}".format(vpn_membership["definitionId"])).json()
        res = VpnMembership.from_json(vpn_info,policy_list)
        topo_list.append(res)
        # print(res.to_json())
        # print(res.name)


    app_routes = rest.get_request("template/policy/definition/approute").json()
    for app_route in app_routes["data"]:
        route_info = rest.get_request("template/policy/definition/approute/{}".format(app_route["definitionId"])).json()
        res = AppRoute.from_json(route_info,policy_list)
        # print(res.name)
        # print(res.to_json())
        traffic_policy_list.append(res)

    datas = rest.get_request("template/policy/definition/data").json()
    for data in datas["data"]:
        route_info = rest.get_request("template/policy/definition/data/{}".format(data["definitionId"])).json()
        res = DataPolicy.from_json(route_info,policy_list)
        # print(res.name)
        # print(res.to_json())
        traffic_policy_list.append(res)


    main_policies = rest.get_request("template/policy/vsmart").json()
    for policy in main_policies["data"]:
        if policy["policyType"]=="feature":
            policy_info = rest.get_request("template/policy/vsmart/definition/{}".format(policy["policyId"])).json()
            res = MainPolicy.from_json(policy["policyId"],policy_info,topo_list,traffic_policy_list,policy_list)
            # print(res.name)
            main_policy_list.append(res)
            # print(res.to_json())
            # if res.name=="Hub-Spoke-Policy-PCI":
            #     res.name="testpolicy_dude1"
            #     res.create(res.url,res.to_json())
            # print(res.modified)
            # res.name="dude"
            # print(res.modified)





if __name__ == '__main__':
    server_info = {
        "hostname":"198.18.1.10",
        "port":8443,
        "username":"admin",
        "password":"admin"
    }
    policy_loader(server_info)

    # 开始创建Policy
    prefix_list1=[
        "10.0.0.0/24"
    ]
    prefix_list2=[
        "192.168.1.0/24"
    ]

    data_prefix_source = DataPrefix(name="Prefix_source2",prefix_list=prefix_list1,is_ipv6=False)
    data_prefix_dest = DataPrefix(name="Prefix_dest2",prefix_list=prefix_list2,is_ipv6=False)

    # 创建Policer限速规则
    pc = Policer("SpeedLimit1",rate="150000",exceed="drop",burst="15000")

    # 创建Site 列表

    site = Site("TestSite2",["100","1000-2000"])

    # 创建VPN 列表

    vpn = Vpn("TestVPN2",["10"])


    sq = Sequence(1,"Custom","data","accept","ipv4",match=[],actions=[])
    # 创建Match规则
    sq.add_match("sourceDataPrefixList",data_prefix_source)
    sq.add_match("destinationDataPrefixList",data_prefix_dest)
    # 创建Action规则
    sq.add_action("set","policer",pc)
    sq.add_action("nat","useVpn","0")
    sq.add_action("nat","fallback","")
    print(sq.to_json())

    # 创建Data Policy
    dp = DataPolicy("NAT_Data_policy2","NAT",[sq],default_action="accept")

    # 创建Main Policy

    main_policy = MainPolicy(name="API_Policy",description="API",control_policy_list=[],data_policy_list=[],vpn_membership_list=[],approute_policy_list=[])
    main_policy.add_data_policy(dp,"service",[site],[vpn])
    # 打印Policy
    print(main_policy.to_json())
    # 保存Policy
    main_policy.save()



    # for mem in topo_list:
    #     if mem.name=="xxzcasad":
    #         mem.name="Niubi"
    # for policy in main_policy_list:
    #     if policy.name =="xzczxcz":
    #         policy.name ="new_doge"
    #         policy.save()









