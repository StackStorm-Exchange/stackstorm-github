import time
import datetime


from lib.base import BaseGithubAction

__all__ = [
    'GetRepositoryCollaborators'
]

class GetRepositoryCollaborators(BaseGithubAction):
    def run(self, api_user, owner, repo, affiliation, per_page, page, github_type ):

        enterprise = self._is_enterprise(github_type)

        if api_user:
            self.token = self._get_user_token(api_user, enterprise)

        payload = { "affiliation": affiliation,
                    "per_page": per_page,
                    "page": page }

        response = self._request("GET",
                                 "/repos/{}/{}/collaborators".format(owner,repo),
                                 payload,
                                 self.token,
                                 enterprise)

        results = {'response': response}
        
        return results
