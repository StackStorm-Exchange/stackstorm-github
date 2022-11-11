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

import yaml
import json
# from mock import MagicMock
from lib.base import BaseGithubAction

from st2tests.base import BaseActionTestCase


class GitHubBaseActionTestCase(BaseActionTestCase):
    __test__ = False


    

    def _mock_request(self, method, uri, data, *args, **kwargs):
        # Defaults to using old request :)
        return self.oldRequest(method, uri, data, *args, **kwargs)

    def tearDown(self):
        super(GitHubBaseActionTestCase, self).tearDown()
        BaseGithubAction._request = self.oldRequest

    def setUp(self):
        super(GitHubBaseActionTestCase, self).setUp()

        self._blank_config = self.load_yaml('blank.yaml')
        self._full_config = self.load_yaml('full.yaml')
        self._enterprise_default_config = self.load_yaml(
            'full-enterprise.yaml')

        self.oldRequest = BaseGithubAction._request
        BaseGithubAction._request = self._mock_request
    

    def load_yaml(self, filename):
        return yaml.safe_load(self.get_fixture_content(filename))
    def load_json(self, filename):
        return json.loads(self.get_fixture_content(filename))

    @property
    def blank_config(self):
        return self._blank_config

    @property
    def full_config(self):
        return self._full_config

    @property
    def enterprise_config(self):
        return self._enterprise_default_config

    def test_run_no_config(self):
        action = self.get_action_instance(self.full_config)
        self.assertIsInstance(action, self.action_cls)

    def test_run_is_instance(self):
        action = self.get_action_instance(self.full_config)
        self.assertIsInstance(action, self.action_cls)
