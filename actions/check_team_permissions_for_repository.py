from lib.base import BaseGithubAction

__all__ = [
    'CheckTeamPermissionsForRepository'
]


class CheckTeamPermissionsForRepository(BaseGithubAction):
    def run(self, api_user, org, team_slug, owner, repo, github_type):

        enterprise = self._is_enterprise(github_type)

        if api_user:
            self.token = self._get_user_token(api_user, enterprise)

        try:
            self._request("GET",
                          "/orgs/{}/teams/{}/repos/{}/{}".format(org, team_slug, owner, repo),
                          {},
                          self.token,
                          enterprise)

            results = {
                'response': "The team {} has access to the repository {}".format(team_slug, repo)
            }
        except OSError as err:
            raise err
        except ValueError as err:
            raise err
        except Exception as err:
            if str(err).find("404"):
                results = {'response': "The team don't have access to the repository or not found"}
            else:
                raise err
        return results
