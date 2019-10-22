from cisco_sdwan_policy.ViptelaRest import ViptelaRest

main_templates={}
loaded_templates={}
policy_templates={}
uuid_pairs={}

def update_template(data):
    data["templateId"] = uuid_pairs[data["templateId"]]
    if data.get("subTemplates"):
        for sub_tmp in data["subTemplates"]:
            sub_tmp["templateId"] = uuid_pairs[sub_tmp["templateId"]]
    return data


def load_template(rest, data):
    result = rest.get_request("template/feature/object/{}".format(data["templateId"]))
    info = result.json()
    if data.get("subTemplates"):
        for sub_tmp in data["subTemplates"]:
            load_template(rest,sub_tmp)
    if not loaded_templates.get(data["templateId"]):
        loaded_templates[data['templateId']] = info
    # print(result.json())


if __name__ == '__main__':

    # From Server
    server_info = {
        "hostname": "198.18.1.10",
        "port": 8443,
        "username": "admin",
        "password": "admin"
    }

    # To Server
    server_info2 = {
        "hostname": "198.18.1.10",
        "port": 8443,
        "username": "admin",
        "password": "admin"
    }

    # Load all policy in vManage
    rest = ViptelaRest.init(server_info)
    resp = rest.get_request("template/device")
    templates = resp.json()["data"]
    for template in templates:
        result = rest.get_request("template/device/object/{}".format(template["templateId"]))
        obj= result.json()
        if obj["configType"]=="template":
            for sub_template in obj["generalTemplates"]:
                load_template(rest,sub_template)
            if "policyId" in obj and obj["policyId"]!="":
                policy_id = obj["policyId"]
                # Currently we do not support feature local policies. Stay tuned for the support from cisco-sdwan-policy module. So if the template has a feature policy, just ignore this template.
                result_t = rest.get_request("template/policy/vedge/definition/{}".format(policy_id))
                result=result_t.json()
                if result["policyType"]=="feature":
                    # Don't support yet.
                    del obj["policyId"]
                else:
                    policy_templates[policy_id] = result
            if "securityPolicyId" in obj and obj["securityPolicyId"]!="":
                security_policy = obj["securityPolicyId"]
                # Currently we do not support feature security policies.
                # result = rest.get_request("template/policy/vedge/definition/{}".format(policy_id))
                # if result["policyType"]=="feature":
                    # Don't support yet.
                del obj["securityPolicyId"]
        main_templates[template["templateId"]] = obj
    # Backup fininshed

    # Start recovery process
    rest = ViptelaRest.init(server_info2)
    # First recover the feature templates.
    result = rest.get_request("template/feature")
    exisiting_feature = [ i["templateName"] for i in result.json()["data"]]
    for uuid,temp in loaded_templates.items():
        if temp["templateName"] in exisiting_feature:
            temp["templateName"] = temp["templateName"]+"_1"
            if temp["templateName"] in exisiting_feature:
                raise Exception("ERROR : Still having name conflicts, are you running the script multiple times?")
        result = rest.post_request("template/feature/",temp)
        new_id = result.json()["templateId"]
        uuid_pairs[uuid]=new_id
    result = rest.get_request("template/policy/vedge")
    exisiting_policy = [ i["policyName"] for i in result.json()["data"]]
    for uuid,temp in policy_templates.items():
        if temp["policyName"] in exisiting_policy:
            temp["policyName"] = temp["policyName"]+"_1"
            if temp["policyName"] in exisiting_policy:
                raise Exception("ERROR : Still having name conflicts, are you running the script multiple times?")
        result = rest.post_request("template/policy/vedge/",temp)
        # For some **weird** reasons, the vManage policy API won't return policyId upon creation, so we have to use a workaround.
        # Hopefully it will be fixed soon.
        new_id = None
        if result.status_code!=200:
            result.raise_for_status()
        else:
            pl = rest.get_request("template/policy/vedge")
            pcs = pl.json()["data"]
            for tmp in pcs:
                if tmp["policyName"]==temp["policyName"]:
                    new_id = tmp["policyId"]
                    break
        if new_id:
            uuid_pairs[uuid]=new_id
        else:
            raise Exception("Policy create failed.")

    # Recover the main policies.
    result = rest.get_request("template/device")
    exisiting_main = [ i["templateName"] for i in result.json()["data"]]
    for uuid,temp in main_templates.items():
        feature = False
        if temp["templateName"] in exisiting_main:
            temp["templateName"] = temp["templateName"]+"_1"
            if temp["templateName"] in exisiting_main:
                raise Exception("ERROR : Still having name conflicts, are you running the script multiple times?")
        if temp["configType"] == "template":
            feature=True
            for sub_template in temp["generalTemplates"]:
                sub_template=update_template(sub_template)
            if "policyId" in temp and temp["policyId"]!="":
                temp["policyId"] = uuid_pairs[temp["policyId"]]
        new_temp = {
            "templateName": temp["templateName"],
            "templateDescription": temp["templateDescription"],
            "deviceType": temp["deviceType"],
            "configType": temp["configType"],
            "factoryDefault": temp["factoryDefault"]
        }
        if feature:
            if temp.get("policyId"): new_temp["policyId"]= temp["policyId"]
            else: new_temp["policyId"]=""
            if temp.get("featureTemplateUidRange"): new_temp["featureTemplateUidRange"]= temp["featureTemplateUidRange"]
            else: new_temp["featureTemplateUidRange"]=[]
            if temp.get("generalTemplates")!=None: new_temp["generalTemplates"]= temp["generalTemplates"]
            else: new_temp["generalTemplates"]=[]
            if temp.get("securityPolicyId")!=None: new_temp["securityPolicyId"]= temp["securityPolicyId"]
            else: new_temp["securityPolicyId"]=""

            result = rest.post_request("template/device/feature/",new_temp)
        else:
            new_temp["templateConfiguration"]= temp["templateConfiguration"]
            result = rest.post_request("template/device/cli/",new_temp)

        new_id = result.json()["templateId"]
        print("Created New Template {}".format(temp["templateName"]))








