import base64

from github_base_action_test_case import GitHubBaseActionTestCase
from create_file import CreateFileAction

from github import Github
from unittest.mock import patch
from unittest.mock import Mock


class CreateFileTest(GitHubBaseActionTestCase):
    __test__ = True
    action_cls = CreateFileAction

    def setUp(self):
        super(CreateFileTest, self).setUp()

        self._test_data = {}
        # This is base parameters for running this action
        self.action_params = {
            'user': 'st2-test',
            'repo': 'StackStorm-Test',
            'path': 'file-test',
            'message': 'commit message',
            'content': 'file content',
        }

    def test_create_file(self):
        def _side_effect(*args, **kwargs):
            self._test_data['content'] = kwargs['content']
            return {'commit': Mock()}

        action = self.get_action_instance(self.full_config)

        with patch.object(Github, 'get_user', return_value=Mock()) as mock_user:
            mock_user.return_value.get_repo.return_value.create_file.side_effect = _side_effect
            action.run(**self.action_params)

        # This chceks sending content value is expected value
        self.assertEqual(self._test_data['content'], self.action_params['content'])

    def test_create_file_with_encoding_param(self):
        def _side_effect(*args, **kwargs):
            self._test_data['content'] = kwargs['content']
            return {'commit': Mock()}

        action = self.get_action_instance(self.full_config)

        with patch.object(Github, 'get_user', return_value=Mock()) as mock_user:
            mock_user.return_value.get_repo.return_value.create_file.side_effect = _side_effect
            action.run(**dict(self.action_params, **{'encoding': 'base64'}))

        # This chceks sending content value is expected value
        self.assertEqual(self._test_data['content'],
                         base64.b64encode(self.action_params['content'].encode('utf-8')))
