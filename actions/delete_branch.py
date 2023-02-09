from lib.base import BaseGithubAction

__all__ = [
    'DeleteBranchAction'
]


class DeleteBranchAction(BaseGithubAction):
    def run(self, api_user, branch, repository, github_type):

        enterprise = self._is_enterprise(github_type)

        if api_user:
            self.token = self._get_user_token(api_user, enterprise)

        response = self._request("DELETE",
                                 f"/repos/{repository}/git/refs/heads/{branch}",
                                 {},
                                 self.token,
                                 enterprise)

        return {'response': response}
