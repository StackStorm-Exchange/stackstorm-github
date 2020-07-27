from lib.base import BaseGithubAction
from github import GithubObject
from lib.formatters import pull_to_dict

__all__ = [
    'CreatePullAction'
]


class CreatePullAction(BaseGithubAction):
    def run(self, user, repo, title, head, base, body=None,
            maintainer_can_modify=None):
        user = self._client.get_user(user)
        repo = user.get_repo(repo)
        pull = repo.create_pull(title=title, head=head, base=base, body=body or '',
                                maintainer_can_modify=maintainer_can_modify or GithubObject.NotSet)
        result = pull_to_dict(pull=pull)
        return result
