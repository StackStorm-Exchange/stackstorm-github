from lib.base import BaseGithubAction

__all__ = [
    'MergePullAction'
]


class MergePullAction(BaseGithubAction):
    def run(self, user, repo, pull_id):

        user = self._client.get_user(user)
        repo = user.get_repo(repo)
        pull = repo.get_pull(pull_id)

        if pull.merged:
            return False, 'Pull Request is already merged'
        if not pull.mergeable:
            return False, 'Pull Request is not mergeable'

        status = pull.merge()

        result = {'merged': status.merged, 'message': status.message}
        return result


if __name__ == '__main__':
    import os

    GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')
    GITHUB_ORG = os.environ.get('GITHUB_ORG')
    GITHUB_REPO = os.environ.get('GITHUB_REPO')
    GITHUB_BRANCH = os.environ.get('GITHUB_BRANCH')

    PULL_ID = 13
    act = MergePullAction(config={'token': GITHUB_TOKEN, 'github_type': 'online'})
    res = act.run(user=GITHUB_ORG, repo=GITHUB_REPO, pull_id=PULL_ID)
    import pprint

    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(res)
