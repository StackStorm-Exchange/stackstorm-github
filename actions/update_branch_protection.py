from lib.base import BaseGithubAction
from github.GithubObject import NotSet

__all__ = [
    'UpdateBranchProtectionAction'
]


class UpdateBranchProtectionAction(BaseGithubAction):
    def run(self, user, repo, branch, required_status_checks, enforce_admins,
            required_pull_request_reviews, restrictions, required_linear_history=False,
            allow_force_pushes=False, allow_deletions=False):

        user = self._client.get_user(user)
        repo = user.get_repo(repo)
        branch = repo.get_branch(branch)

        if not required_status_checks:
            strict = NotSet
            contexts = NotSet
        else:
            strict = required_status_checks['strict']
            contexts = required_status_checks['contexts']

        if not required_pull_request_reviews:
            dismissal_users = NotSet
            dismissal_teams = NotSet
            dismiss_stale_reviews = NotSet
            require_code_owner_reviews = NotSet
            required_approving_review_count = NotSet
        else:
            dismissal_users = required_pull_request_reviews['dismissal_users']
            dismissal_teams = required_pull_request_reviews['dismissal_teams']
            dismiss_stale_reviews = required_pull_request_reviews['dismiss_stale_reviews']
            require_code_owner_reviews = required_pull_request_reviews['require_code_owner_reviews']
            required_approving_review_count = required_pull_request_reviews[
                'required_approving_review_count']

        if not restrictions:
            user_push_restrictions = NotSet
            team_push_restrictions = NotSet
        else:
            user_push_restrictions = restrictions['user_push_restrictions']
            team_push_restrictions = restrictions['team_push_restrictions']

        branch.edit_protection(strict=strict, contexts=contexts,
                               enforce_admins=enforce_admins,
                               dismissal_users=dismissal_users,
                               dismissal_teams=dismissal_teams,
                               dismiss_stale_reviews=dismiss_stale_reviews,
                               require_code_owner_reviews=require_code_owner_reviews,
                               required_approving_review_count=required_approving_review_count,
                               user_push_restrictions=user_push_restrictions,
                               team_push_restrictions=team_push_restrictions)
        return True


if __name__ == '__main__':
    import os

    GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')
    GITHUB_ORG = os.environ.get('GITHUB_ORG')
    GITHUB_REPO = os.environ.get('GITHUB_REPO')
    GITHUB_BRANCH = os.environ.get('GITHUB_BRANCH')

    # As produced by get_branch_protection action
    BRANCH_PROTECTION = {'enforce_admins': True,
                         'required_pull_request_reviews': None,
                         'required_status_checks': {'contexts': [], 'strict': True},
                         'restrictions': None
                         }

    act = UpdateBranchProtectionAction(config={'token': GITHUB_TOKEN, 'github_type': 'online'})
    res = act.run(user=GITHUB_ORG, repo=GITHUB_REPO, branch=GITHUB_BRANCH,
                  required_status_checks=BRANCH_PROTECTION['required_status_checks'],
                  enforce_admins=BRANCH_PROTECTION['enforce_admins'],
                  required_pull_request_reviews=BRANCH_PROTECTION['required_pull_request_reviews'],
                  restrictions=BRANCH_PROTECTION['restrictions'])
    import pprint

    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(res)
