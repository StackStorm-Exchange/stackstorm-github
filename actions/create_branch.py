import time
import datetime


from lib.base import BaseGithubAction

__all__ = [
    'CreateBranchAction'
]

class CreateBranchAction(BaseGithubAction):
    def run(self, api_user, new_branch, origin_ref, repository, github_type):

        enterprise = self._is_enterprise(github_type)

        if api_user:
            self.token = self._get_user_token(api_user, enterprise)

        
        # First, we have to get the sha1 for the given origin ref
        response = self._request("GET", f"/repos/{repository}/git/ref/{origin_ref}",
                                 {},
                                 self.token,
                                 enterprise)
        
        if not response or not response['object']['sha']:
            raise Exception(f"Could not get ref [{origin_ref}]. Response: {response}")


        # Then, we create the branch based on the origin ref
        payload = { "ref": f"refs/heads/{new_branch}",
                    "sha": response['object']['sha']}

        response = self._request("POST",
                                 f"/repos/{repository}/git/refs",
                                 payload,
                                 self.token,
                                 enterprise)

        return { 'response': response }
