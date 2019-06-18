from lib.base import BaseGithubAction
from lib.formatters import user_to_dict

__all__ = [
    'GetUserAction'
]


class GetUserAction(BaseGithubAction):
    def run(self, user, token_user, github_type):
        enterprise = self._is_enterprise(github_type)
        if token_user:
            self._change_to_user_token(token_user, enterprise)

        user = self._client.get_user(user)
        result = user_to_dict(user=user)
        return result
