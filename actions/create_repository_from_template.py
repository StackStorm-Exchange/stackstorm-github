from lib.base import BaseGithubAction

__all__ = ["CreateRepositoryFromTemplateAction"]


class CreateRepositoryFromTemplateAction(BaseGithubAction):
    def run(
        self,
        api_user,
        github_type,
        template_owner,
        template_repo,
        owner,
        name,
        description,
        include_all_branches,
        private,
    ):

        enterprise = self._is_enterprise(github_type)

        if api_user:
            self.token = self._get_user_token(api_user, enterprise)

        payload = {
            "owner": owner,
            "name": name,
            "description": description,
            "include_all_branches": include_all_branches,
            "private": private,
        }

        response = self._request(
            "POST",
            "/repos/{}/{}/generate".format(template_owner, template_repo),
            payload,
            self.token,
            enterprise,
        )

        results = {"owner": response["owner"]["login"]}
        results["response"] = response

        return results
