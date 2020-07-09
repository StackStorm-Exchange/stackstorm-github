import re
from github.InputGitAuthor import InputGitAuthor
from github.GithubObject import NotSet

__all__ = [
    'prep_github_params_for_file_ops', 'branch_protection_attributes',
    'required_pull_request_reviews_attributes', 'restrictions_attributes'
]

# expecting string in the format of "FirstName LastName <email@address>"
author_pattern = re.compile(r"^(.*?)\s+<([a-zA-Z0-9_.+-]+?@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)?>$")

branch_protection_attributes = ['url', 'required_status_checks', 'enforce_admins',
                                'required_pull_request_reviews', 'required_linear_history',
                                'allow_force_pushes', 'allow_deletions']

required_pull_request_reviews_attributes = ['dismissal_teams', 'dismissal_users',
                                            'dismiss_stale_reviews',
                                            'require_code_owner_reviews',
                                            'required_approving_review_count']

restrictions_attributes = ['users', 'teams', 'apps']


def create_github_author(s):
    match = re.match(author_pattern, s)
    if match:
        name = match.group(1)
        email = match.group(2)
        return InputGitAuthor(name=name, email=email)
    else:
        return None


def prep_github_params_for_file_ops(author, branch, committer):
    if not branch:
        branch = NotSet

    if committer:
        committer = create_github_author(committer)
    else:
        committer = NotSet

    if author:
        author = create_github_author(author)
    else:
        author = NotSet

    return author, branch, committer
