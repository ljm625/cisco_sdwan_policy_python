from cisco_sdwan_policy.Helper.PolicyLoader import PolicyLoader

if __name__ == '__main__':

    # Example 1: Save policy to local disk & restore it.

    # Input server Info here
    server_info = {
        "hostname": "192.168.100.32",
        "port": 443,
        "username": "admin",
        "password": "admin",
    }
    # Load all policy in vManage
    pl = PolicyLoader.init(server_info)
    pl.load()

    # Show all the loaded Policy.(Optional)
    print([i.name for i in pl.main_policies])
    print([i.name for i in pl.topo_policies])
    print([i.name for i in pl.traffic_policies])
    print([i.name for i in pl.list_policies])

    # Generate backup json
    backup = pl.save_to_json()

    # Save to file
    with open("policy_dump.json","w+") as file:
        file.write(backup)



    # Read from file
    with open("policy_dump.json","r") as file:
        info = file.read()
    # Load to vMange and auto merge if needed.
    pl.load_from_json(info)

