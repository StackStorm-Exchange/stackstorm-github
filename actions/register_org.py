from lib.base import BaseGithubAction
import json
from st2client.client import Client
from st2client.models import KeyValuePair

__all__ = [
    'AddOrgAction'
]


class AddOrgAction(BaseGithubAction):
    def run(self, user, url, token, github_type):

        client = Client()
        gitorgs = client.keys.get_by_name(name='git-orgs', decrypt=True)
        if gitorgs:
            dict=json.loads(gitorgs.value)
        else:
            dict={}
        org = {'user': user, 'url': url, 'token': token, 'type': github_type}
        dict[user+'|'+url]=org
        gitorgs=json.dumps(dict)

        client.keys.update(KeyValuePair(name='git-orgs', value=gitorgs, secret=True))

        return True
