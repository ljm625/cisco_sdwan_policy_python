# Cisco SD-WAN(Viptela) Policy 模块

该模块将Cisco SD-WAN当中的Policy部分通过Python的类进行了建模，简化了程序化创建Policy，修改Policy，备份Policy，迁移Policy的工作量。

[English](https://github.com/ljm625/cisco_sdwan_policy_python/blob/master/README.md)



目前只支持Python3，

安装：
```
pip install cisco-sdwan-policy
```

简单的样例代码：
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

服务器信息部分:

```json
server_info = {
    "hostname":"198.18.1.10",
    "port":8443,
    "username":"admin",
    "password":"admin",
    "tenant": "xxx"
    }
```
- hostname : vManage控制器的域名/IP地址
- port : vManage控制器的网页IP，默认为 443/8443
- username : vManage用户名
- password : vManage密码
- tenant : 租户名称，可选，如果非多租户环境，请不要提供此项。可以设置为租户名称，Tenant-id 或者 VSessionId, 如: "Tenant1" 或 "1554923113309" 或 "MTU1NDkyMzExMzMwOQ=="

当重新初始化ViptelaRest类，PolicyLoader对象时，已经创建的policy对象会自动被导向到新的服务器信息，这可能会导致严重的问题，因此再重新初始化之后，请务必使用PolicyLoader的load功能重新载入Policy。

#### 例子 1 : 备份 & 恢复Policy

下面的例子是Policy的全量备份，保存到Json文件中，再通过加载备份的文件将Policy恢复到新的vManage中。

[Link](https://github.com/ljm625/cisco_sdwan_policy_python/blob/master/example1.py)


#### 例子2 2 : 将租户1中的一个主Policy迁移到租户2中

下面的例子是将一个主Policy从租户1迁移到租户2中，由于本代码中实现了依赖的自动检测&保存，因此主Policy中的所有依赖也会全部被迁移过来，无需人工干预

[Link](https://github.com/ljm625/cisco_sdwan_policy_python/blob/master/example2.py)


之后会更新更多的样例代码.

## 问题和联系方式

如果您有任何问题，可以提交Github Issue 或者直接联系我。

我的CEC ID: jiaminli
