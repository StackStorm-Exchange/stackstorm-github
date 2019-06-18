from lib.base import BaseGithubAction

__all__ = [
    'GetTrafficStatsAction'
]


class GetTrafficStatsAction(BaseGithubAction):
    def run(self, repo, github_type):
        traffic_data = self._get_analytics(
            category='traffic-data', repo=repo, enterprise=self._is_enterprise(github_type))
        return traffic_data['summary']
