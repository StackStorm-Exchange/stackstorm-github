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

from store_oauth_token import StoreOauthTokenAction


class StoreOauthTokenActionTestCase(GitHubBaseActionTestCase):
    __test__ = True
    action_cls = StoreOauthTokenAction

    def test_run_uses_online(self):
        expected = {'github_type': "online"}
        action = self.get_action_instance(self.enterprise_config)

        results = action.run(user="octocat",
                             token="foo",
                             github_type="online")

        self.assertEqual(results, expected)
        self.assertEqual("foo",
                         action.action_service.get_value("token_octocat"))

    def test_run_uses_enterprise(self):
        expected = {'github_type': "enterprise"}
        action = self.get_action_instance(self.enterprise_config)

        results = action.run(user="octocat",
                             token="foo",
                             github_type="enterprise")

        self.assertEqual(results, expected)
        self.assertEqual("foo",
                         action.action_service.get_value("token_enterprise_octocat"))

    def test_run_token_string_whitespace_start(self):
        expected = {'github_type': "online"}
        action = self.get_action_instance(self.full_config)

        results = action.run(user="octocat",
                             token=" foo",
                             github_type="online")

        self.assertEqual(results, expected)
        self.assertEqual("foo",
                         action.action_service.get_value("token_octocat"))

    def test_run_token_string_whitespace_end(self):
        expected = {'github_type': "online"}
        action = self.get_action_instance(self.full_config)

        results = action.run(user="octocat",
                             token="foo ",
                             github_type="online")

        self.assertEqual(results, expected)
        self.assertEqual("foo",
                         action.action_service.get_value("token_octocat"))

    def test_run_token_string_whitespace_both(self):
        expected = {'github_type': "online"}
        action = self.get_action_instance(self.full_config)

        results = action.run(user="octocat",
                             token=" foo ",
                             github_type="online")

        self.assertEqual(results, expected)
        self.assertEqual("foo",
                         action.action_service.get_value("token_octocat"))
