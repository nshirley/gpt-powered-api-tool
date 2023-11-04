import requests
from .api_base_connector import API_Base_Connector

class Octopi_API_Connector(API_Base_Connector):
    url = ""
    def __init__(self):
        API_Base_Connector.__init__(self, "Please reference any documentation you have available on the Octopi API.")
    
    def req(self, route, payload):
        params = payload
        requests.get(url=self.url+route, params=params)