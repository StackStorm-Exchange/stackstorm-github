from lib.base import BaseGithubAction
import json
from st2client.client import Client
from st2client.models import KeyValuePair

__all__ = [
    'ListOrgAction'
]


class ListOrgsAction(BaseGithubAction):
    def run(self):
        results = []

        client = Client()
        gitorgs = client.keys.get_by_name(name='git-orgs', decrypt=True)
        if gitorgs:
            dict=json.loads(gitorgs.value)
        else:
            dict={}
        results = list(dict.keys())

        return results
