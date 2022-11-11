from lib.base import BaseGithubAction

__all__ = [
    'AddUpdateRepositoryTeamAction'
]


class AddUpdateRepositoryTeamAction(BaseGithubAction):
    def run(self, api_user, org, team_slug,
            owner, repo, github_type, permission):

        enterprise = self._is_enterprise(github_type)

        if api_user:
            self.token = self._get_user_token(api_user, enterprise)

        payload = {"permission": permission}

        response = self._request("PUT",
                            "/orgs/{}/teams/{}/repos/{}/{}".format(org, team_slug, owner, repo),
                            payload,
                            self.token,
                            enterprise)

        results = {'response': response}

        return results
