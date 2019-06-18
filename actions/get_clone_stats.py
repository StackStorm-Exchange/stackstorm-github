from lib.base import BaseGithubAction

__all__ = [
    'GetCloneStatsAction'
]


class GetCloneStatsAction(BaseGithubAction):
    def run(self, repo, github_type):
        clone_data = self._get_analytics(
            category='clone-activity-data', repo=repo, enterprise=self._is_enterprise(github_type))
        return clone_data['summary']
