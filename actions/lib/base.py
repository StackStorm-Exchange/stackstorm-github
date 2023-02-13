from github import Github
import requests
from bs4 import BeautifulSoup
import json
import logging

from st2common.runners.base_action import Action

__all__ = [
    'BaseGithubAction'
]

# Default Github web URL (used by tasks which directly scrape data from HTML)
# pages
DEFAULT_WEB_URL = 'https://github.com'

# Default Github API url
DEFAULT_API_URL = 'https://api.github.com'


class BaseGithubAction(Action):

    def run(self, **kwargs):
        pass

    def __init__(self, config):
        super(BaseGithubAction, self).__init__(config=config)
        token = self.config.get('token', None)
        self.token = token or None

        self.web_url = self.config.get('web_url', None)
        self.base_url = self.config.get('base_url', None)

        self.default_github_type = self.config.get('github_type', None)

        if self.default_github_type == 'online':
            self._client = Github(self.token, base_url=DEFAULT_API_URL)
        else:
            self._client = Github(self.token, base_url=self.base_url)

        self._session = requests.Session()

    def _web_session(self, web_url=DEFAULT_WEB_URL):
        """Returns a requests session to scrape off the web"""
        login_url = web_url + '/login'
        session = requests.Session()
        request = session.get(login_url).text
        html = BeautifulSoup(request)
        token = html.find('input', {'name': 'authenticity_token'}).attrs['value']
        commit_value = html.find('input', {'name': 'commit'}).attrs['value']
        session_path = html.find('form', {'method': 'post'}).attrs['action']

        login_data = {
            'login': self.config['user'],
            'password': self.config['password'],
            'commit': commit_value,
            'authenticity_token': token
        }

        session_url = web_url + session_path
        session.post(session_url, data=login_data)
        return session

    def _get_analytics(self, category, repo, enterprise):
        if enterprise:
            url = self.web_url + repo + '/graphs/' + category + '.json'
            s = self._web_session(self.web_url)
        else:
            url = DEFAULT_WEB_URL + repo + '/graphs/' + category + '.json'
            s = self._web_session()

        response = s.get(url)
        return response.json()

    # Whether or not this execution is meant for enterprise github installation (on-premises)
    # or online installations (in the cloud)
    def _is_enterprise(self, github_type):

        if github_type == "enterprise":
            return True
        elif github_type == "online":
            return False
        elif self.default_github_type == "enterprise":
            return True
        elif self.default_github_type == "online":
            return False
        else:
            raise ValueError("Default GitHub Invalid!")

    # Github token will come from KV using this function.. and depending on whether
    # it's for enterprise or not, it will return have either of the key prefix below
    def _get_user_token(self, user, enterprise):
        """
        Return a users GitHub OAuth Token, if it fails replace '-'
        with '.' as '.' is not valid for GitHub names.
        """

        if enterprise:
            token_name = "token_enterprise_"
        else:
            token_name = "token_"

        token = self.action_service.get_value(token_name + user, local=False, decrypt=True)

        # if a token is not returned, try using reversing changes made by
        # GitHub Enterprise during LDAP sync'ing.
        if token is None:
            token = self.action_service.get_value(
                token_name + user.replace("-", "."))

        return token

    def _change_to_user_token_if_enterprise(self, api_user, github_type):
        enterprise = self._is_enterprise(github_type)
        if api_user:
            self._change_to_user_token(api_user, enterprise)

    # Changes the internal client used on this instance of action execution to
    # the one matching the configuration for enterprise/online and user given here
    def _change_to_user_token(self, user, enterprise):
        logging.debug("Changing github client for user [%s] and enterprise [%s]", user, enterprise)
        token = self._get_user_token(user, enterprise)

        if enterprise:
            self._client = Github(token, base_url=self.base_url)
        else:
            self._client = Github(token, base_url=DEFAULT_API_URL)

        return True

    # Sends a generic HTTP/s request to the github endpoint
    def _request(self, method, uri, payload, token, enterprise):
        headers = {'Authorization': 'token {}'.format(token)}

        if enterprise:
            url = "{}{}".format(self.base_url, uri)
        else:
            url = "{}{}".format(DEFAULT_API_URL, uri)

        r = None
        try:
            r = self._session.request(method,
                                      url,
                                      data=json.dumps(payload),
                                      headers=headers,
                                      verify=False)
            r.raise_for_status()
        except requests.exceptions.HTTPError:
            raise Exception(
                "ERROR: '{}'ing to '{}' - status code: {} payload: {} response: {}".format(
                    method, url, r.status_code, json.dumps(payload), r.json()))
        except requests.exceptions.ConnectionError as e:
            raise Exception("Could not connect to: {} : {}".format(url, e))
        else:
            if r.status_code == 204:
                return None
            else:
                return r.json()
