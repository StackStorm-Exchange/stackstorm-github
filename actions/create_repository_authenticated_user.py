import time
import datetime


from lib.base import BaseGithubAction

__all__ = [
    'CreateRepositoryAuthenticatedUserAction'
]

class CreateRepositoryAuthenticatedUserAction(BaseGithubAction):
    def run(self, api_user, user, name, description, github_type, homepage, private, 
            has_issues, has_projects, has_wiki, team_id, auto_init, gitignore_template, 
            license_template, allow_squash_merge, allow_merge_commit, allow_rebase_merge, 
            allow_auto_merge, delete_branch_on_merge, has_downloads, is_template, ):

        enterprise = self._is_enterprise(github_type)

        if api_user:
            self.token = self._get_user_token(api_user, enterprise)

        payload = { "user": user,
                    "name": name,
                    "description": description,
                    "homepage": homepage,
                    "private": private,
                    "has_issues": has_issues,
                    "has_projects": has_projects,
                    "has_wiki": has_wiki,
                    "team_id": team_id,
                    "auto_init": auto_init,
                    "gitignore_template": gitignore_template,
                    "license_template": license_template,
                    "allow_squash_merge": allow_squash_merge,
                    "allow_merge_commit": allow_merge_commit,
                    "allow_rebase_merge": allow_rebase_merge,
                    "allow_auto_merge": allow_auto_merge,
                    "delete_branch_on_merge": delete_branch_on_merge,
                    "has_downloads": has_downloads,
                    "is_template": is_template}

        response = self._request("POST",
                                 "/user/repos",
                                 payload,
                                 self.token,
                                 enterprise)

        results = {'owner': response['owner']['login']}
        results['response'] = response

        return results
