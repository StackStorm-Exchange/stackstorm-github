from lib.base import BaseGithubAction
from github import GithubObject
from lib.formatters import ref_to_dict

__all__ = [
    'CreateGitRefAction'
]


class CreateGitRefAction(BaseGithubAction):
    def run(self, user, repo, ref, sha):
        user = self._client.get_user(user)
        repo = user.get_repo(repo)
        ref = repo.create_git_ref(ref, sha)
        result = ref_to_dict(ref=ref)
        return result
