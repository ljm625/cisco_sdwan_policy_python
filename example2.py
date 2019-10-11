from cisco_sdwan_policy.Helper.PolicyLoader import PolicyLoader

if __name__ == '__main__':

    # Example 2: Transfer a specific policy from tenant1 to tenant2.

    # Server Tenant1 Info
    server_info = {
        "hostname": "192.168.100.32",
        "port": 443,
        "username": "admin",
        "password": "admin",
        "tenant": "T1"
    }
    # Load all policy in vManage
    pl = PolicyLoader.init(server_info)
    pl.load()

    # Show all the loaded Policy.(Optional)
    print([i.name for i in pl.main_policies])
    print([i.name for i in pl.topo_policies])
    print([i.name for i in pl.traffic_policies])
    print([i.name for i in pl.list_policies])

    # Backup all the policies
    old_main = pl.main_policies
    old_topo = pl.topo_policies
    old_traffic = pl.traffic_policies
    old_list =pl.list_policies

    # Find the policy to move
    policy_to_move=None
    for i in pl.list_policies:
        if i.name=="test":
            policy_to_move=i

    # Input the Tenant2 info
    new_server_info = {
        "hostname": "192.168.100.32",
        "port": 443,
        "username": "admin",
        "password": "admin",
        "tenant": "T2"
    }

    # Load the Tenant2 Policies
    pl = PolicyLoader.init(new_server_info)
    pl.load()



    if policy_to_move:
        # In order to restore all policy referenced list/topos, we need to check the existing policy from new tenant and then make use of auto save feature.
        for i in old_list:
            if i.name not in [j.name for j in pl.list_policies]:
                pass
            else:
                i.name = i.name + "_1"
            i.id = None
        for i in old_topo:
            if i.name not in [j.name for j in pl.topo_policies]:
                pass
            else:
                i.name = i.name + "_1"
            i.id = None
        for i in old_traffic:
            if i.name not in [j.name for j in pl.topo_policies]:
                pass
            else:
                i.name = i.name + "_1"
            i.id = None
        if policy_to_move.name in [j.name for j in pl.main_policies]:
            policy_to_move.name = policy_to_move+"_1"

        # Save the new policy, all the dependencies will automatically created.
        policy_to_move.save()

