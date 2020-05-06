from lib.base import BaseGithubAction
from lib.formatters import file_response_to_dict
from github.GithubObject import NotSet

__all__ = [
    'UpdateFileAction'
]


class UpdateFileAction(BaseGithubAction):
    def run(self, user, repo, path, message, content, sha, branch=None, committer=None,
            author=None):
        if not branch:
            branch = NotSet
        if not committer:
            committer = NotSet
        if not author:
            author = NotSet

        user = self._client.get_user(user)
        repo = user.get_repo(repo)
        api_response = repo.update_file(path=path, message=message, content=content, sha=sha,
                                        branch=branch, committer=committer, author=author)
        result = file_response_to_dict(api_response)
        return result


if __name__ == '__main__':
    import os
    GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')
    GITHUB_ORG = os.environ.get('GITHUB_ORG')
    GITHUB_REPO = os.environ.get('GITHUB_REPO')

    act = UpdateFileAction(config={'token': GITHUB_TOKEN, 'github_type': 'online'})
    res = act.run(user=GITHUB_ORG, repo=GITHUB_REPO, path='README.md', message='Test commit',
                  content='Super duper read me file, pushed from Stackstorm github pack!\n'
                          '##new lines added!\n\n*YES*\n',
                  sha='10ddd6d257e01349d514541981aeecea6b2e741d',
                  branch='branch1')
    import pprint
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(res)
