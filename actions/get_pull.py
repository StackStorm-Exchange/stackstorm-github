from lib.base import BaseGithubAction
from lib.formatters import pull_to_dict

__all__ = [
    'GetPullAction'
]


class GetPullAction(BaseGithubAction):
    def run(self, user, repo, pull_id):
        issue_id = int(pull_id)

        user = self._client.get_user(user)
        repo = user.get_repo(repo)
        pull = repo.get_pull(issue_id)
        result = pull_to_dict(pull=pull)
        return result
