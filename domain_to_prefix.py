import argparse
from pprint import pprint

try:
    import yaml
    import sublist3r
    import dns.resolver
except Exception as e:
    print("Error loading libraries, please run following commands first:")
    print("pip install pyyaml dnspython")
    print("git clone https://github.com/aboul3la/Sublist3r")
    print("cd Sublist3r")
    print("python setup.py install")
    exit(1)
from cisco_sdwan_policy.List.DataPrefix import DataPrefix

from cisco_sdwan_policy.List.Prefix import Prefix

from cisco_sdwan_policy import PolicyLoader


def config_reader(config_file):
    '''
    Read config from yaml file
    :return: config in dict format
    '''
    with open(config_file) as file:
        config = yaml.load(file.read(),Loader=yaml.FullLoader)
        # print(result)
        return config

def parse_domain(domain,nameserver):
    domain_list=[]
    ip_list=set()
    if "*" in domain and domain[0:2]!="*.":
        raise Exception("Invalid domain: {}".format(domain))
    elif "*" in domain:
        sub_domains = sublist3r.main(domain[2:], 40, None, ports=None, silent=False, verbose=False,
                                    enable_bruteforce=False, engines=None)

        print(sub_domains)
        domain_list.extend(sub_domains)
    else:
        domain_list.append(domain)
    # Use DNSPYTHON to get info.
    resolver = dns.resolver.Resolver()
    resolver.lifetime = resolver.timeout = 20.0
    for domain_name in domain_list:
        print("Resolving: {}".format(domain_name))
        try:
            resolver.nameservers=[nameserver]
            response =resolver.query(domain_name)
            for answer in response.response.answer:
                for ip in answer.items:
                    if ip.rdtype == 1:
                        ip_list.add(ip.address+"/32")
        except:
            pass
        # try:
        #     response = dns.resolver.query(domain_name, "CNAME")
        #     for answer in response.response.answer:
        #         for ip in answer.items:
        #             if ip.rdtype == 1:
        #                 ip_list.add(ip.address+"/32")
        # except:
        #     pass

    return ip_list



if __name__ == '__main__':
    # First read all the configurations from config file.
    parser = argparse.ArgumentParser(description='App List Genenrator.')
    parser.add_argument('config', metavar='config_file_path', type=str,
                        help='config yaml path')
    args = parser.parse_args()
    config_file=args.config
    try:
        config = config_reader(config_file)
        print("Config file {} loaded".format(args.config))
        app_ip_info ={}
        assert type(config["sdwan_server"])==dict
        assert type(config["apps"])==dict
        assert type(config["dns_server"])==str
    except Exception as e:
        print("ERROR : Invalid config file.")
        print(e)
        exit(1)

    for appname,domain_list in config["apps"].items():
        app_ips=set()
        for domain in domain_list:
            ip_list = parse_domain(domain,config["dns_server"])
            app_ips = app_ips | ip_list
        app_ip_info[appname]=list(app_ips)
    pprint(app_ip_info)
    if config["policy_create"]:
        print("Start creating Prefix Lists")
        pl = PolicyLoader.init(config["sdwan_server"])
        pl.load()
        existing_list=[i.name for i in pl.list_policies]
        for appname,ip_list in app_ip_info.items():
            if  "{}_prefix".format(appname) not in existing_list:
                Prefix("{}_prefix".format(appname),prefix_list=ip_list).save()
                print("Created Prefix List: {}_prefix".format(appname))
            else:
                for i in pl.list_policies:
                    if i.name=="{}_prefix".format(appname):
                        i.set_entries(ip_list)
                        i.save()
                        print("Updated Prefix List: {}".format(i.name))
            if "{}_dataprefix".format(appname) not in existing_list:
                DataPrefix("{}_dataprefix".format(appname),prefix_list=ip_list).save()
                print("Created Data Prefix List: {}_dataprefix".format(appname))

            else:
                for i in pl.list_policies:
                    if i.name=="{}_dataprefix".format(appname):
                        i.set_entries(ip_list)
                        i.save()
                        print("Updated Data Prefix List: {}".format(i.name))



