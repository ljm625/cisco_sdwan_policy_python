import json

import requests
import sys


class ViptelaRest(object):
    instance=None
    def __init__(self, vmanage_ip, username, password,port = 443,tenant=None):
        self.vmanage_ip = vmanage_ip
        self.port = port
        self.session = {}
        self.tenant=tenant
        self.token=None
        self.login(self.vmanage_ip, port, username, password)

    @classmethod
    def init(cls,server_info=None):
        if server_info:
            cls.instance = cls(server_info["hostname"],server_info["username"],server_info["password"],server_info["port"],server_info.get("tenant_id"))
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


        self.session[vmanage_ip] = sess
        # Get xsrf_token for 19.2 and later versions
        response = self.session[vmanage_ip].get(base_url_str+ "/dataservice/client/token", verify=False)
        if response.status_code==200:
            self.token = response.text



    def get_request(self, mount_point):
        """GET request"""
        url = "https://%s:%s/dataservice/%s" % (self.vmanage_ip, self.port, mount_point)
        header = self.get_header()
        response = self.session[self.vmanage_ip].get(url, verify=False,headers=header)
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
        response = self.session[self.vmanage_ip].post(url=url, data=payload, headers=headers, verify=False)
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
            response = self.session[self.vmanage_ip].put(url=url,data=payload,headers=headers,verify=False)
        else:
            response=self.session[self.vmanage_ip].put(url=url,headers=headers,verify=False)
        return response