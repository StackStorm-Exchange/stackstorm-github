import time
import datetime


from lib.base import BaseGithubAction

__all__ = [
    'AddRepositoryCollaboratorAction'
]

class AddRepositoryCollaboratorAction(BaseGithubAction):
    def run(self, api_user, owner, repo, username, github_type, permission ):

        enterprise = self._is_enterprise(github_type)

        if api_user:
            self.token = self._get_user_token(api_user, enterprise)

        payload = { "permission": permission }

        response = self._request("PUT",
                                 "/repos/{}/{}/collaborators/{}".format(owner,repo,username ),
                                 payload,
                                 self.token,
                                 enterprise)

        results = {'response': response}

        return results
