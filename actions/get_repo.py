from lib.base import BaseGithubAction
from lib.formatters import repo_to_dict

__all__ = [
    'GetRepoAction'
]


class GetRepoAction(BaseGithubAction):
    def run(self, user, repo):
        user = self._client.get_user(user)
        repo = user.get_repo(repo)
        result = repo_to_dict(repo=repo)
        return result
