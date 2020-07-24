import datetime

from lib.base import BaseGithubAction
from lib.formatters import repo_to_dict

__all__ = [
    'ListReposAction'
]


class ListReposAction(BaseGithubAction):
    def run(self, user, since=None, visibility='all', limit=20):
        user = self._client.get_user(user)

        kwargs = {}
        if visibility:
            kwargs['visibility'] = visibility
        if since:
            kwargs['since'] = datetime.datetime.fromtimestamp(since)

        repos = user.get_repos(**kwargs)
        repos = list(repos)

        result = []
        for index, repo in enumerate(repos):
            repo = repo_to_dict(repo=repo)
            result.append(repo)

            if (index + 1) >= limit:
                break

        return result
