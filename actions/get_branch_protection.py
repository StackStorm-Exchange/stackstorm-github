from lib.base import BaseGithubAction
from lib.formatters import branch_protection_to_dict

__all__ = [
    'GetBranchProtectionAction'
]


class GetBranchProtectionAction(BaseGithubAction):
    def run(self, user, repo, branch):

        user = self._client.get_user(user)
        repo = user.get_repo(repo)
        branch = repo.get_branch(branch)
        branch_protection = branch.get_protection()
        result = branch_protection_to_dict(branch_protection)
        return result


if __name__ == '__main__':
    import os
    GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')
    GITHUB_ORG = os.environ.get('GITHUB_ORG')
    GITHUB_REPO = os.environ.get('GITHUB_REPO')
    GITHUB_BRANCH = os.environ.get('GITHUB_BRANCH')

    act = GetBranchProtectionAction(config={'token': GITHUB_TOKEN, 'github_type': 'online'})
    res = act.run(user=GITHUB_ORG, repo=GITHUB_REPO, branch=GITHUB_BRANCH)
    import pprint
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(res)
