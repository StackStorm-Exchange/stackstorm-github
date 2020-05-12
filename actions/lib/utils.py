import re
from github.InputGitAuthor import InputGitAuthor
from github.GithubObject import NotSet

__all__ = [
    'prep_github_params_for_file_ops'
]

# expecting string in the format of "FirstName LastName <email@address>"
author_pattern = re.compile(r"^(.*?)\s+<([a-zA-Z0-9_.+-]+?@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)?>$")


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
