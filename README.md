# Cisco SD-WAN(Viptela) Policy Module

This Module is intend to make generating/modifying Cisco SD-WAN Policy easier as well as backing up policy. 

Currently tested on 19.1.x and 19.2.x vManage.

Also included two cli tools for easiler backup/restore policy and template base on the project.

[中文文档](https://github.com/ljm625/cisco_sdwan_policy_python/blob/master/README_CHINESE.md)


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

The Server Info Part:

```json
server_info = {
    "hostname":"198.18.1.10",
    "port":8443,
    "username":"admin",
    "password":"admin",
    "tenant": "xxx"
    }
```
- hostname : The IP/Domain of vManage controller
- port : The port for vManage web portal, by default its 443/8443
- username : The username for vManage
- password : The password for vManage
- tenant : Optional, if not using multi-tenant mode, just don't present in the json. It **CAN** be Tenant name, Tenant-id or VSessionId, For example: "Tenant1" or "1554923113309" or "MTU1NDkyMzExMzMwOQ=="

When re-initiating ViptelaRest class, all the existing object will auto change to new server as well, so **make sure to reload the policy after changing server info**



## CLI tools usage

```
pip install cisco-sdwan-policy
```

#### For template backup/restore, run:

```bash
sdwan-template-tool -h
```

Example usage:
```bash
[*] Transfer template test:
sdwan-template-tool --mode=transfer --template=test --server1-ip=10.0.0.1 --server1-port=443 --server1-user=admin --server1-pw=admin --server2-ip=10.0.0.2 --server2-port=443 --server2-user=admin --server2-pw=admin
[*] Backup all template:
sdwan-template-tool --mode=backup --all-template --file=backup.json --server1-ip=10.0.0.1 --server1-port=443 --server1-user=admin --server1-pw=admin
[*] Restore template from a file:
sdwan-template-tool --mode=restore --file=backup.json --server1-ip=10.0.0.1 --server1-port=443 --server1-user=admin --server1-pw=admin```
```

#### For policy backup/restore, run:

```bash
sdwan-policy-tool -h
```

Example usage:
```bash
[*] Transfer policy 'Policy1':
sdwan-policy-tool --mode=transfer --policy=Policy1 --server1-ip=10.0.0.1 --server1-port=443 --server1-user=admin --server1-pw=admin --server2-ip=10.0.0.2 --server2-port=443 --server2-user=admin --server2-pw=admin
[*] Backup all policy:
sdwan-policy-tool --mode=backup --all-policy --file=backup.json --server1-ip=10.0.0.1 --server1-port=443 --server1-user=admin --server1-pw=admin
[*] Restore policy from a file:
sdwan-policy-tool --mode=restore --file=backup.json --server1-ip=10.0.0.1 --server1-port=443 --server1-user=admin --server1-pw=admin
```

#### Example 1 : Policy Backup & Restore

Below is the example of backing up policy into a json file, then transfer policy to a new vManage or restore to existing vManage. You can also tranfer policies between tenants.


[Link](https://github.com/ljm625/cisco_sdwan_policy_python/blob/master/example1.py)


#### Example 2 : Transfer a Main policy from Tenant1 to Tenant2

Below is the example of transfering a main policy from tenant 1 to tenant 2, and all the policy dependencies will automatically be transferred as well.

[Link](https://github.com/ljm625/cisco_sdwan_policy_python/blob/master/example2.py)


#### Example 3 : Generate a IP list base on domains

Below is the example of generate a IP list base on given domains, useful for not supported applications.

Before using this, please install sublist3r manually, it's not supported yet.

[Link](https://github.com/ljm625/cisco_sdwan_policy_python/blob/master/domain_to_prefix.py)



More examples will be added later.


## Questions and Contact Info

If you have any issues or a pull request, you can submit a Issue or contact me directly。

My Cisco CEC ID: jiaminli

Pull request of enhancements and examples are welcomed!

