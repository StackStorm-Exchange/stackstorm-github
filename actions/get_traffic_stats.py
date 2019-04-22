from lib.base import BaseGithubAction

__all__ = [
    'GetTrafficStatsAction'
]


class GetTrafficStatsAction(BaseGithubAction):
    def run(self, repo):
        enterprise = self._is_enterprise(github_type)
        traffic_data = self._get_analytics(category='traffic-data', repo=repo, enterprise)
        return traffic_data['summary']
