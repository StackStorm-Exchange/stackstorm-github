from lib.base import BaseGithubAction
from lib.formatters import file_response_to_dict
from github.GithubObject import NotSet

__all__ = [
    'CreateFileAction'
]


class CreateFileAction(BaseGithubAction):
    def run(self, user, repo, path, message, content, branch=None, committer=None, author=None):
        if not branch:
            branch = NotSet
        if not committer:
            committer = NotSet
        if not author:
            author = NotSet

        user = self._client.get_user(user)
        repo = user.get_repo(repo)
        api_response = repo.create_file(path=path, message=message, content=content, branch=branch,
                                        committer=committer, author=author)
        result = file_response_to_dict(api_response)
        return result


if __name__ == '__main__':
    import os
    GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')
    GITHUB_ORG = os.environ.get('GITHUB_ORG')
    GITHUB_REPO = os.environ.get('GITHUB_REPO')

    act = CreateFileAction(config={'token': GITHUB_TOKEN, 'github_type': 'online'})
    res = act.run(user=GITHUB_ORG, repo=GITHUB_REPO, path='README5.md', message='Test commit',
                  content='Super duper read me file, pushed from Stackstorm github pack!\n',
                  branch='branch1')
    import pprint
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(res)
