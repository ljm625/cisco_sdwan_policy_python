import json

from cisco_sdwan_policy.Helper.PolicyLoader import PolicyLoader
from cisco_sdwan_policy.Helper.Sequence import Sequence
from cisco_sdwan_policy.List.Application import Application
from cisco_sdwan_policy.List.Color import Color
from cisco_sdwan_policy.List.DataPrefix import DataPrefix
from cisco_sdwan_policy.List.Prefix import Prefix
from cisco_sdwan_policy.List.Policer import Policer
from cisco_sdwan_policy.List.Site import Site
from cisco_sdwan_policy.List.Tloc import Tloc
from cisco_sdwan_policy.List.Vpn import Vpn
from cisco_sdwan_policy.MainPolicy import MainPolicy
from cisco_sdwan_policy.Topology.CustomTopo import CustomTopo
from cisco_sdwan_policy.Topology.VpnMembership import VpnMembership
from cisco_sdwan_policy.TrafficPolicy.AppRoute import AppRoute
from cisco_sdwan_policy.TrafficPolicy.DataPolicy import DataPolicy
from cisco_sdwan_policy.ViptelaRest import ViptelaRest
policy_list = []
topo_list = []
traffic_policy_list=[]
main_policy_list=[]






if __name__ == '__main__':
    server_info = {
        "hostname":"198.18.1.10",
        "port":8443,
        "username":"admin",
        "password":"admin"
    }
    # 加载系统内所有的现有Policy（如果不编辑已经存在的Policy可以忽略）
    pl = PolicyLoader.init(server_info)
    pl.load()


    # 开始创建Policy
    prefix_list1=[
        "10.0.0.0/24"
    ]
    prefix_list2=[
        "192.168.1.0/24"
    ]

    # 创建Prefix列表

    data_prefix_source = DataPrefix(name="Prefix_source2",prefix_list=prefix_list1,is_ipv6=False)
    data_prefix_dest = DataPrefix(name="Prefix_dest2",prefix_list=prefix_list2,is_ipv6=False)

    # 创建Policer限速规则
    pc = Policer("SpeedLimit1",rate="150000",exceed="drop",burst="15000")

    # 创建Site列表

    site = Site("TestSite2",["100","1000-2000"])

    # 创建VPN列表

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







