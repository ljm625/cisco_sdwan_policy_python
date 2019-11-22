import json
import base64
import requests
import sys


class ViptelaRest(object):
    instance=None
    def __init__(self, vmanage_ip, username, password,port = 443,tenant=None):
        self.vmanage_ip = vmanage_ip
        self.port = port
        self.session = {}
        self.token=None
        self.tenant=None
        self.login(self.vmanage_ip, port, username, password)
        self.get_version()
        if tenant:
            try:
                base64.b64decode(tenant)
                self.tenant=tenant
            except:
                result = self.set_tenant(tenant)
                if not result:
                    raise Exception("ERROR : Given Tenant {} not found!".format(tenant))


    @classmethod
    def init(cls,server_info=None):
        if server_info:
            cls.instance = cls(server_info["hostname"],server_info["username"],server_info["password"],server_info["port"],server_info.get("tenant"))
            return cls.instance
        elif cls.instance:
            return cls.instance
        else:
            raise Exception("Viptela server not initialized.")

    def get_header(self):
        header = {'Content-Type': 'application/json'}
        if self.token:
            header["X-XSRF-TOKEN"]=self.token
        if self.tenant:
            header["VSessionId"]=self.tenant
        return header



    def login(self, vmanage_ip, port, username, password):
        """Login to vmanage"""
        base_url_str = 'https://%s:%s' % (vmanage_ip,port)

        login_action = '/j_security_check'

        # Format data for loginForm
        login_data = {'j_username': username, 'j_password': password}

        # Url for posting login data
        login_url = base_url_str + login_action

        url = base_url_str + login_url

        sess = requests.session()
        # If the vmanage has a certificate signed by a trusted authority change verify to True
        login_response = sess.post(url=login_url, data=login_data, verify=False,headers={"Content-Type":"application/x-www-form-urlencoded"})
        # if self.tenant:
        #     sess.headers.update({'vsession_id':self.tenant})

        if login_response.status_code>=300:
            # print(
            # "Login Failed")
            raise BaseException("ERROR : The username/password is not correct.")
        if '<html>' in login_response.text:
            raise BaseException("ERROR : Login Failed.")


        self.session = sess
        # Get xsrf_token for 19.2 and later versions
        response = self.session.get(base_url_str+ "/dataservice/client/token", verify=False)
        if response.status_code==200:
            self.token = response.text

    def set_tenant(self,tenant_name):
        resp = self.get_request("tenant")
        data = resp.json()
        tenant_id =None
        if data.get("data") and len(data.get("data"))>0:
            for tenant in data["data"]:
                if str(tenant["name"])==str(tenant_name):
                    tenant_id = tenant["tenantId"]
                elif str(tenant["tenantId"])==str(tenant_name):
                    tenant_id = tenant["tenantId"]
        if tenant_id:
            resp = self.post_request("tenant/{}/vsessionid".format(tenant_id),{})
            data = resp.json()
            if data.get("VSessionId"):
                self.tenant=data["VSessionId"]
                return True


    def get_request(self, mount_point):
        """GET request"""
        url = "https://%s:%s/dataservice/%s" % (self.vmanage_ip, self.port, mount_point)
        header = self.get_header()
        response = self.session.get(url, verify=False,headers=header)
        if response.status_code>=300:
            response.raise_for_status()
        elif response.status_code==200:
                return response
        else:
            return None

    def post_request(self, mount_point, payload):
        """POST request"""
        url = "https://%s:%s/dataservice/%s" % (self.vmanage_ip,self.port, mount_point)
        headers = self.get_header()
        payload = json.dumps(payload)
        response = self.session.post(url=url, data=payload, headers=headers, verify=False)
        return response

    def put_request(self, mount_point, payload=None):
        """
        PUT Method
        :param mount_point: The url for API
        :param payload: The payload for API
        :param headers: The header
        :return: response
        """
        url= "https://{}:{}/dataservice/{}".format(self.vmanage_ip,self.port,mount_point)
        headers = self.get_header()
        if payload:
            payload=json.dumps(payload)
            response = self.session.put(url=url,data=payload,headers=headers,verify=False)
        else:
            response=self.session.put(url=url,headers=headers,verify=False)
        return response

    def get_version(self):
        resp = self.get_request("device/action/install/devices/vmanage?groupId=all")
        self.version = resp.json()["data"][0]["version"]
        return resp.json()["data"][0]["version"]