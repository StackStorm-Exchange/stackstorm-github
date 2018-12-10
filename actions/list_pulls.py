import re

from lib.base import BaseGithubAction
from lib.formatters import pull_to_dict

__all__ = [
    'ListPullsAction'
]


class ListPullsAction(BaseGithubAction):
    def run(self, user, repo, filter=None, state=None, sort=None,
            direction=None, base=None, head=None, since=None, limit=20):
        user = self._client.get_user(user)
        repo = user.get_repo(repo)

        kwargs = {}
        if state:
            kwargs['state'] = state
        if sort:
            kwargs['sort'] = sort
        if direction:
            kwargs['direction'] = direction
        if base:
            kwargs['base'] = base
        if head:
            kwargs['head'] = head

        if filter:
            pattern = re.escape(filter['pattern'])

        # Note: PyGithub library introduces an abstraction for paginated lists
        # which doesn't conform to Python's iterator spec so we can't use
        # array slicing to exhaust the list :/
        pulls = repo.get_pulls(**kwargs)
        pulls = list(pulls)

        result = []
        for index, pull in enumerate(pulls):
            pull = pull_to_dict(pull=pull)
            if filter:
                if re.search(pattern, pull[filter['key']]):
                    result.append(pull)
                    if (index + 1) >= limit:
                        break
            else:
                result.append(pull)
                if (index + 1) >= limit:
                    break

        return result
