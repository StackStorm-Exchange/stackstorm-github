from lib.base import BaseGithubAction

__all__ = [
    'MergePullAction'
]


class MergePullAction(BaseGithubAction):
    def run(self, user, repo, pull_id):

        user = self._client.get_user(user)
        repo = user.get_repo(repo)
        pull = repo.get_pull(pull_id)

        if pull.mergeable:
            return (False, 'Pull Request is not mergeable')
        if pull.merged:
            return (False, 'Pull Request is already merged')

        status = pull.merge()

        result = {'merged': status.merged, 'message': status.message}
        return result
