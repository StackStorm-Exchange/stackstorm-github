# Github Integration Pack

Pack which allows integration with [Github](https://github.com/).

## Configuration

Copy the example configuration in [github.yaml.example](./github.yaml.example)
to `/opt/stackstorm/configs/github.yaml` and edit as required.

It must contain:

* ``token`` - Authentication token. Note: token only needs to be specified for
  actions such as ``add_comment`` and ``add_status`` which require
  authentication. If you use ``get_issue`` action only with public
  repositories, then token doesn't need to be specified.
* ``repository_sensor.repositories`` - A list of repositories to monitor. Each
  item needs to contain the following keys: ``user`` - user or organization the
  repository you want to monitor belongs to and ``name`` - name of the
  repository you want to monitor.
* ``repository_sensor.event_type_whitelist`` - List of whitelisted events to listen for.
* ``user`` - GitHub Username (only for use with ``get_traffic_stats`` and ``get_clone_stats`` actions).
* ``password`` - GitHub Password (only for use with ``get_traffic_stats`` and ``get_clone_stats`` actions).

Keep in mind that even though actions which operate on public repositories
don't require an authentication token, you are still encouraged to supply one
because unauthenticated requests have a very low rate limit.

**Note** : When modifying the configuration in `/opt/stackstorm/configs/` please
           remember to tell StackStorm to load these new values by running
           `st2ctl reload --register-configs`

## Obtaining an Authentication Token

To obtain an authentication token, follow the instructions on the [Creating an
access token for command-line use](https://help.github.com/articles/creating-an-access-token-for-command-line-use/)
page.

## Sensors

### GithubRepositorySensor

This sensor monitors Github repository for activity and dispatches a trigger
for each repository event.

> Note that current default poll interval requires authentication because of
GitHub [rate-limiting](https://developer.github.com/v3/#rate-limiting) for
unauthenticated requests.

Currently supported event types:

* ``IssuesEvent`` - Triggered when an issue is assigned, unassigned, labeled,
  unlabeled, closed, or reopened.
* ``IssueCommentEvent`` - Triggered when an issue comment is created.
* ``ForkEvent`` - Triggered when a user forks a repository.
* ``WatchEvent`` - Triggered when a user stars a repository.
* ``ReleaseEvent`` - Triggered when new release is available.
* ``PushEvent`` - Triggered when a repository branch is pushed to. In addition to branch pushes, webhook push events are also triggered when repository tags are pushed.

**Note** : The sensor will only listen events for the `github_type` you chosen
           in config.yaml


#### github.repository_event trigger

Example trigger payload:

```json
{
    "repository": "st2",
    "id": "2482918921",
    "type": "WatchEvent",
    "created_at": "2014-12-25T11:47:27.000000Z",
    "actor": {
        "bio": null,
        "name": null,
        "url": "https://api.github.com/users/odyss009",
        "id": 483157,
        "loaction": null,
        "email": "redacted"
    },
    "payload": {
        "action": "started"
    }
}
```

All the events contain `repository`, `id`, `created_at`, `actor` and
`payload` attribute.

Value of the payload attribute depends on the event type. You can see a list
of the available event types and their attributes on the [Event Types &
Payloads](https://developer.github.com/v3/activity/events/types/) page.

Note: Similar thing can be achieved using Github webhooks in combination with
StackStorm webhook handler.

## Actions

* ``add_comment`` - Add comment to the provided issue / pull request.
* ``add_status`` - Add commit status to the provided commit.
* ``create_file`` - Create new file.
* ``create_issue`` - Create a new issue.
* ``delete_branch_protection`` - Remove branch protection settings.
* ``get_branch_protection`` - Get branch protection settings.
* ``get_contents`` - Get repository or file contents.
* ``get_issue`` - Retrieve information about a particular issue. Note: You
  only need to specify authentication token in the config if you use this
  action with a private repository.
* ``list_issues`` - List all the issues for a particular repo (includes pull
  requests since pull requests are just a special type of issues).
* ``list_pulls`` - List all pull requests for a particular repo.
* ``merge_pull`` - Merge the provided pull request.
* ``review_pull`` - Create a review for the provided pull request.
* ``update_branch_protection`` - Update branch protection settings.
* ``update_file`` - Update existing file.

## Rules

### github.deployment_event_webhook

To enable this rule, run the following on the CLI (with a valid ST2 auth token):

```bash
st2 rule enable github.deploy_pack_on_deployment_event
```

Then you should add a web hook in github sending deployment events to the following URL:

`https://<st2-server>/api/v1/webhooks/github_deployment_event?st2-api-key=<ST2-API-KEY>`

By default the enviroment is set to production, you can change this in
your own `github.yaml`.

You can then create a deployment via ChatOps with the following
command:

```
@hubot github deployment create me/my_st2_pack description Lets get the feature to production
```

### Limitations

- You need to have logged an OAuth key with StackStorm (via `github.store_oauth_token`).
- If using with GitHub.com your ST2 server needs to be contactable via the internet!
- Deployment Statuses will be logged as the creating user in GitHub.
- With StackStorm v2.1+ you should be able to deploy tags.
- Certain branch protection attributes are not supported by current Python GitHub module.
