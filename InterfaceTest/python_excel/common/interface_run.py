import requests

class InterfaceRun:
    def __init__(self):
        self.method = None
        self.url = None
        self.data = None
        self.headers = None


    def get_request(self,url,data=None,headers=None,verify=False):
        session = requests.session()
        res = session.get(url,data=data,headers = headers)
        return res
    def post_request(self,url,data=None,headers=None,verify=False):
        #session = requests.session()
        res = requests.post(url,data,headers = headers)
        return res

    def main_request(self,method,url,data=None,headers=None):
        if str(method).lower() == 'get':
            res = self.get_request(url,data,headers)
        elif str(method).lower() == 'post':
            res = self.post_request(url, data, headers)
        else:
            res = None
        return res

