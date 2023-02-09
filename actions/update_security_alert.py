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


class UpdateSecurityAlert(BaseGithubAction):
    def run(self, api_user, user, repository, github_type, alert_type, alert_number, state, dismissed_reason = None, dismissed_comment = None):
        enterprise = self._is_enterprise(github_type)

        if api_user:
            self.token = self._get_user_token(api_user,
                                              enterprise)
        payload = {
            'state': state
        }
        if state == 'dismissed':
            payload.update({
                'dismissed_reason': dismissed_reason,
                'dismissed_comment': dismissed_comment
            })

        response = self._request("PATCH",
            "/repos/{}/{}/{}/alerts/{}".format(user,repository,alert_type,alert_number),
            payload,
            self.token,
            enterprise)

        results = {
            'alert_number' : response['number'],
            'state': response['state'],
            'html_url': response['html_url']
        }

        return results
