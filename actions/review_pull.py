from lib.base import BaseGithubAction
from lib.formatters import pull_to_dict

__all__ = [
    'ReviewPullAction'
]


class ReviewPullAction(BaseGithubAction):
    def run(self, user, repo, pull_id, message, event):

        user = self._client.get_user(user)
        repo = user.get_repo(repo)
        pull = repo.get_pull(pull_id)
        pull.create_review(commit=repo.get_commit(pull.merge_commit_sha),
            body=str(message), event=str(event))
        result = pull_to_dict(pull)
        return result
