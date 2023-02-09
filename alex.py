from github import Github

DEFAULT_API_URL = 'https://api.github.com'

client = Github('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', base_url=DEFAULT_API_URL)

repo= client.get_organization('doshii-io').get_repo('doshii-connect').get_codescan_alerts()

print(dir(repo))