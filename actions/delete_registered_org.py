from lib.base import BaseGithubAction
import json
from st2client.client import Client
from st2client.models import KeyValuePair

__all__ = [
    'DeleteOrgAction'
]


class DeleteOrgAction(BaseGithubAction):
    def run(self, user, url):

        client = Client()
        gitorgs = client.keys.get_by_name(name='git-orgs', decrypt=True)
        if gitorgs:
            dict=json.loads(gitorgs.value)
        else:
            dict={}

        if user+'|'+url in dict:
            del dict[user+'|'+url]
        gitorgs=json.dumps(dict)

        client.keys.update(KeyValuePair(name='git-orgs', value=gitorgs, secret=True))

        return True
