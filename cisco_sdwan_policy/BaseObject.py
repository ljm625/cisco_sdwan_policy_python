import json
from pprint import pprint

from cisco_sdwan_policy.ViptelaRest import ViptelaRest


class BaseObject(object):

    def __init__(self,**kwargs):
        # Initialized API Endpoints.
        self.modified=False
        self.rest = ViptelaRest.init()
        if kwargs.get("debug"):
            self.debug=kwargs["debug"]
        else:
            self.debug=False

    def to_json(self):
        "Used for override"
        return {}

    def get_id(self):
        self.save()
        return self.id

    def save(self):
        if self.__getattribute__("id"):
            if self.modified:
                self.update(self.url,self.to_json())
        else:
            id = self.create(self.url,self.to_json())
            self.id = id

    def create(self,path,data):
        if self.debug:
            print("Creating Object:")
            print("Calling: {}".format(path))
            print("Body:")
            pprint(data)

        if self.__getattribute__("id"):
            return False
        result = self.rest.post_request(path,data)
        if result.status_code == 200:
            if result.content:
                for k,v in result.json().items():
                    if "id" in k.lower():
                        return v
            else:
                return None
        else:
            raise Exception("Error Creating: {} {}".format(result.status_code, result.content))
        return None

    def export(self):
        result = self.to_json()
        result["class"]=type(self).__name__
        result["id"]=self.id
        return result
    def __del__(self):
        pass

    def __setattr__(self, instance, value):
        if instance=="modified":
            pass
        else:
            super().__setattr__("modified",True)
        super().__setattr__(instance,value)

    def update(self,path,data):
        if self.modified and self.id:
            if self.debug:
                print("Updating Object:")
                print("Calling: {}".format(path))
                print("Body:")
                pprint(data)

            result = self.rest.put_request("{}/{}".format(path,self.id),data)
            if result.status_code == 200:
                return True
            else:
                raise Exception("Error Updating: {} {}".format(result.status_code, result.content))

