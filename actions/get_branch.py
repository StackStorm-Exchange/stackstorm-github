import time
import datetime


from lib.base import BaseGithubAction

__all__ = [
    'GetBranchAction'
]

class GetBranchAction(BaseGithubAction):
    def run(self, api_user, branch, repository, github_type):

        enterprise = self._is_enterprise(github_type)

        if api_user:
            self.token = self._get_user_token(api_user, enterprise)

        
        # First, we have to get the sha1 for the given origin ref
        response = self._request("GET", f"/repos/{repository}/git/ref/heads/{branch}",
                                 {},
                                 self.token,
                                 enterprise)

        return { 'response': response }
