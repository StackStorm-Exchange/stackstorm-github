from lib.base import BaseGithubAction
from lib.formatters import pull_to_dict

__all__ = [
    'CreatePullAction'
]


class CreatePullAction(BaseGithubAction):
    def run(self, user, repo, title, body, head, base, api_user, github_type):
        self._change_to_user_token_if_enterprise(api_user, github_type)

        user = self._client.get_user(user)
        repo = user.get_repo(repo)
        pull = repo.create_pull(title=title, body=body, head=head, base=base)
        result = pull_to_dict(pull=pull)
        return result
