from lib.base import BaseGithubAction

__all__ = [
    'AddUpdateRepositoryEnvironmentAction'
]


class AddUpdateRepositoryEnvironmentAction(BaseGithubAction):

    def _get_team_id(self, enterprise, org, name):
        self.logger.debug("Getting team ID for name [%s]", name)
        response = self._request("GET",
                                f"/orgs/{org}/teams/{name}",
                                None,
                                self.token,
                                enterprise)
        self.logger.debug("Found ID [%d] for name [%s]", response["id"], name)
        return response["id"]

    def run(self, api_user, environment,
            owner, repo, github_type, reviewers, wait_timer, deployment_branch_policy):

        enterprise = self._is_enterprise(github_type)

        if api_user:
            self.token = self._get_user_token(api_user, enterprise)

        # Transforming team slug names in IDs
        for reviewer in reviewers:
            type = reviewer.get("type", None)
            name = reviewer.get("name", None)
            if type == "Team" and name:
                del reviewer["name"]
                reviewer["id"] = self._get_team_id(enterprise, owner, name)
            elif type == "User" and name:
                raise NotImplementedError("Providing reviewer of type user without \
                     ID is not implemented!")

        payload = {
            "wait_timer": int(wait_timer),
            "reviewers": reviewers,
            "deployment_branch_policy": deployment_branch_policy
        }

        self.logger.info(
            "Adding/Updating environment [%s] with parameters [%s] for repo [%s/%s] with user [%s]",
            environment, payload, owner, repo, api_user)

        try:
            response = self._request("PUT",
                                f"/repos/{owner}/{repo}/environments/{environment}",
                                payload,
                                self.token,
                                enterprise)
            results = {'response': response}
            return results
        except Exception as e:
            self.logger.error("Could not add/update environment, error: %s", repr(e))
            return (False, "Could not add/update environment, error: %s" % repr(e))

        return (False, "Could not add/update environment for unknown reason!")
