from lib.base import BaseGithubAction
from lib.formatters import contents_to_dict

__all__ = [
    'GetContentsAction'
]


class GetContentsAction(BaseGithubAction):
    def run(self, user, repo, ref, path, decode=False):

        user = self._client.get_user(user)
        repo = user.get_repo(repo)
        contents = repo.get_contents(path, ref=ref)
        result = contents_to_dict(contents=contents, decode=decode)
        return result


if __name__ == '__main__':
    import os
    GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')
    GITHUB_ORG = os.environ.get('GITHUB_ORG')
    GITHUB_REPO = os.environ.get('GITHUB_REPO')

    act = GetContentsAction(config={'token': GITHUB_TOKEN, 'github_type': 'online'})
    res = act.run(user=GITHUB_ORG, repo=GITHUB_REPO, ref='branch1', path='README.md', decode=True)
    import pprint
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(res)
