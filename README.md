# Cisco SD-WAN(Viptela) Policy Module

This Module is intend to make generating/modifying Cisco SD-WAN Policy easier as well as backing up policy. 


## Usage

```
pip install cisco-sdwan-policy
```

```python
from cisco_sdwan_policy import *


# vManage Info
server_info = {
    "hostname":"198.18.1.10",
    "port":8443,
    "username":"admin",
    "password":"admin"
    }
# Load all policy in vManage
pl = PolicyLoader.init(server_info)
pl.load()

# Show all the loaded Policy.
print([i.name for i in pl.main_policies])
print([i.name for i in pl.topo_policies])
print([i.name for i in pl.traffic_policies])
print([i.name for i in pl.list_policies])



# Create a new Policy
prefix_list1=[
    "10.0.0.0/24"
]
prefix_list2=[
    "192.168.1.0/24"
]

# Create Prefix list

data_prefix_source = DataPrefix(name="Prefix_source2",prefix_list=prefix_list1,is_ipv6=False)
data_prefix_dest = DataPrefix(name="Prefix_dest2",prefix_list=prefix_list2,is_ipv6=False)

# Create Policer
pc = Policer("SpeedLimit1",rate="150000",exceed="drop",burst="15000")

# Create Site List

site = Site("TestSite2",["100","1000-2000"])

# Create VPN List

vpn = Vpn("TestVPN2",["10"])


sq = Sequence(1,"Custom","data","accept","ipv4",match=[],actions=[])
# Create Match
sq.add_match("sourceDataPrefixList",data_prefix_source)
sq.add_match("destinationDataPrefixList",data_prefix_dest)
# Create Action
sq.add_action("set","policer",pc)
sq.add_action("nat","useVpn","0")
sq.add_action("nat","fallback","")
print(sq.to_json())

# Create Data Policy
dp = DataPolicy("NAT_Data_policy2","NAT",[sq],default_action="accept")

# Create Main Policy

main_policy = MainPolicy(name="API_Policy",description="API",control_policy_list=[],data_policy_list=[],vpn_membership_list=[],approute_policy_list=[])
main_policy.add_data_policy(dp,"service",[site],[vpn])
# Print Policy json
print(main_policy.to_json())
# Save Policy (Create)
main_policy.save()


```

#### Example 1 : Policy Backup & Restore

[Link](https://github.com/ljm625/cisco_sdwan_policy_python/blob/master/examples1.py)



There are more usage other than that, for example backup policy/transfer policy between vManage/Tenant etc.

More examples will be added later.