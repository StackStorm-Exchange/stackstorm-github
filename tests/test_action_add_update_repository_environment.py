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

# from mock import MagicMock

from github_base_action_test_case import GitHubBaseActionTestCase

from add_update_repository_environment import AddUpdateRepositoryEnvironmentAction


class AddUpdateRepositoryEnvironmentActionTestCase(GitHubBaseActionTestCase):
    __test__ = True
    action_cls = AddUpdateRepositoryEnvironmentAction

    expectedCreateEnvPayload = None

    def _mock_request(self, method, uri, data, *args, **kwargs):
        if uri == "/repos/org/repo/environments/env-test":
            self.assertEquals(data, self.expectedCreateEnvPayload)
            return self.load_json('add_update_repository_environment/result_successful.json')

        if uri == "/orgs/org/teams/test-team":
            self.assertEquals(data, None)
            return {
                'id': 123
            }

        return super()._mock_request(method, uri, data, *args, **kwargs)

    def test_successful(self):

        action = self.get_action_instance(self.full_config)
        self.assertIsInstance(action, self.action_cls)

        expected_results = {
            'response': self.load_json('add_update_repository_environment/result_successful.json')
        }
        self.expectedCreateEnvPayload = (
            {
                "wait_timer": 0,
                "reviewers": [
                    {
                        "type": "Team",
                        "id": 123
                    }
                ],
                "deployment_branch_policy": None
            })

        results = action.run(
            api_user="test",
            environment="env-test",
            owner="org",
            repo="repo",
            github_type="online",
            reviewers=[
                {
                    "type": "Team",
                    "id": 123
                }
            ],
            wait_timer=0,
            deployment_branch_policy=None
        )

        self.assertEquals(results, expected_results)

    def test_successful_team_with_name(self):

        action = self.get_action_instance(self.full_config)
        self.assertIsInstance(action, self.action_cls)

        expected_results = {
            'response': self.load_json('add_update_repository_environment/result_successful.json')
        }
        self.expectedCreateEnvPayload = (
            {
                "wait_timer": 0,
                "reviewers": [
                    {
                        "type": "Team",
                        "id": 123
                    }
                ],
                "deployment_branch_policy": None
            })

        results = action.run(
            api_user="test",
            environment="env-test",
            owner="org",
            repo="repo",
            github_type="online",
            reviewers=[
                {
                    "type": "Team",
                    "name": "test-team"
                }
            ],
            wait_timer=0,
            deployment_branch_policy=None
        )

        self.assertEquals(results, expected_results)
