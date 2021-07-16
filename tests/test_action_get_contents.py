from github_base_action_test_case import GitHubBaseActionTestCase
from get_contents import GetContentsAction

from github import Github
from unittest.mock import patch
from unittest.mock import Mock


class AddCommentActionTestCase(GitHubBaseActionTestCase):
    __test__ = True
    action_cls = GetContentsAction

    def setUp(self):
        super(AddCommentActionTestCase, self).setUp()

        # This is base parameters for running this action
        self.action_params = {
            'user': 'st2-test',
            'repo': 'StackStorm-Test',
            'ref': 'HEAD',
            'path': 'file-test',
        }

        # There are mock data-set of returned contents
        _mock_data_base = {
            'size': 'test-size',
            'name': 'test-name',
            'path': 'test-path',
            'sha': 'test-sha',
            'url': 'https://example.com/test-url',
            'git_url': 'https://example.com/test-git_url',
            'html_url': 'https://example.com/test-html_url',
            'download_url': 'https://example.com/test-download_url',
        }
        self.mock_data_for_file = dict(_mock_data_base, **{
            'type': 'file',
            'encoding': 'base64',
            'content': 'test-content',
        })
        self.mock_data_for_symlink = dict(_mock_data_base, **{
            'type': 'symlink',
            'target': 'test-target',
        })
        self.mock_data_for_submodule = dict(_mock_data_base, **{
            'type': 'submodule',
            'submodule_git_url': 'https://example.com/submodule_git_url',
        })
        self.mock_data_for_directory = dict(_mock_data_base, **{
            'type': 'directory',
        })

    def _confirm_returned_contents(self, action_params, mock_content, expected_content):
        """
        This run github.get_contents action and confirm returned value is expected one.
        """
        action = self.get_action_instance(self.full_config)

        # Configure mocks not to send requests to the GitHub
        with patch.object(Github, 'get_user', return_value=Mock()) as mock_user:
            mock_user.return_value.get_repo.return_value.get_contents.return_value = mock_content

            # Run github.get_contents action with decode parameter
            result = action.run(**action_params)

        self.assertEqual(result, expected_content)

    def test_get_file(self):
        mock_content = Mock()
        for (key, value) in self.mock_data_for_file.items():
            setattr(mock_content, key, value)

        # run action and check returned contents
        self._confirm_returned_contents(self.action_params, mock_content, self.mock_data_for_file)

    def test_get_file_with_decode_param(self):
        mock_content = Mock()
        for (key, value) in self.mock_data_for_file.items():
            setattr(mock_content, key, value)

        # This is in case of calling ContentFile.decoded_content
        mock_content.decoded_content = 'test-decoded-content'

        # run action and check returned contents
        params = dict(self.action_params, **{'decode': True})
        self._confirm_returned_contents(params, mock_content, dict(self.mock_data_for_file, **{
            'content': 'test-decoded-content'
        }))

    def test_get_directory(self):
        mock_content = Mock()
        for (key, value) in self.mock_data_for_directory.items():
            setattr(mock_content, key, value)

        # run action and check returned contents
        self._confirm_returned_contents(self.action_params, [mock_content],
                                        [self.mock_data_for_directory])

    def test_get_symlink(self):
        mock_content = Mock()
        for (key, value) in self.mock_data_for_symlink.items():
            setattr(mock_content, key, value)

        # run action and check returned contents
        self._confirm_returned_contents(self.action_params, [mock_content],
                                        [self.mock_data_for_symlink])

    def test_get_submodule(self):
        mock_content = Mock()
        for (key, value) in self.mock_data_for_submodule.items():
            setattr(mock_content, key, value)

        # run action and check returned contents
        self._confirm_returned_contents(self.action_params, [mock_content],
                                        [self.mock_data_for_submodule])
