from lib.base import BaseGithubAction

__all__ = [
    'CheckIfUserIsRepositoryCollaborator'
]


class CheckIfUserIsRepositoryCollaborator(BaseGithubAction):
    def run(self, api_user, owner, repo, username, github_type):

        enterprise = self._is_enterprise(github_type)

        if api_user:
            self.token = self._get_user_token(api_user, enterprise)

        try:
            self._request("GET",
                          "/repos/{}/{}/collaborators/{}".format(owner, repo, username),
                          {},
                          self.token,
                          enterprise)
            results = {'response': f"The user {username} is a Collaborator"}
        except OSError as err:
            raise err
        except ValueError as err:
            raise err
        except Exception as err:
            if str(err).find("404"):
                results = {'response': f"The user {username} is not a Collaborator or not found"}
            else:
                raise err
        return results
