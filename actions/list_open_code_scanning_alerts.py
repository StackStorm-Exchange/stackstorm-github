# Licensed to the StackStorm, Inc ('StackStorm') under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and

from lib.base import BaseGithubAction


class ListOpenCodeScanningAlerts(BaseGithubAction):
    def run(self, api_user, user,repository, github_type):
        results = []

        enterprise = self._is_enterprise(github_type)

        if api_user:
            self.token = self._get_user_token(api_user,
                                              enterprise)
        page=1
        paginate = True
        alerts = []
        while paginate:
            response = self._request("GET",
                                    "/repos/{}/{}/code-scanning/alerts?state=open&per_page=20&page={}".format(user,repository,page),
                                    None,
                                    self.token,
                                    enterprise)
            if len(response) == 0:
                paginate = False
            else:
                alerts += response
                page += 1


        for alert in alerts:
            results.append(
                {'alert_number': alert['number'],
                 'created_at': alert['created_at'],
                 'updated_at': alert['updated_at'],
                 'tool_name': alert['tool']['name'],
                 'tool_version': alert['tool']['version'],
                 'rule_severity': alert['rule']['severity'],
                 'rule_name': alert['rule']['name'],
                 'rule_description': alert['rule']['description'],
                 'html_url': alert['html_url']
                 })

        return results
