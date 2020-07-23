import datetime
 
from lib.base import BaseGithubAction
from lib.formatters import user_to_dict

__all__ = [
    'ListMembersAction'
]


class ListMembersAction(BaseGithubAction):
    def run(self, user,filter=None, role=None, limit=20):
        org = self._client.get_organization(user)

        kwargs = {}
        if filter:
            kwargs['filter'] = filter
        if role:
            kwargs['role'] = role

        members = org.get_members(**kwargs)
        members = list(members)

        result = []
        for index, member in enumerate(members):
            member = user_to_dict(user=member)
            result.append(member)

            if (index + 1) >= limit:
                break

        return result
