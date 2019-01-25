import os
import json
import requests


class PipedriveAPI():

    api_token = os.environ.get("PIPEDRIVE_API_TOKEN")
    root = 'http://api.pipedrive.com/v1'
    endpoints = {}

    def getOrgByName(self, q):

        endpoint = f'{self.root}/organizations/find'
        params = {}
        params['term'] = q
        params['api_token'] = self.api_token
        resp = requests.get(endpoint, params=params)
        return resp

    def getOrgDetails(self, _id):
        url = f'{self.root}/organizations/{_id}?api_token={self.api_token}'
        resp = requests.get(url)
        return resp
