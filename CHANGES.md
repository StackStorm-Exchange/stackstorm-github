# Changelog

## 1.3.0

* Add new ``github.get_branch_protection`` action which allows user to retrieve protection settings set on branch.
* Add new ``github.update_branch_protection`` action which allows user to update protection settings for branch.
* Add new ``github.delete_branch_protection`` action which allows user to delete protection from branch.

## 1.2.0

__IMPORTANT__: Configuration scheme changed to mark token and password as secret, if you were using st2 datastore, you might need to encrypt the values!

* Allow passing base64 encoded content to update and create file actions.
* Bug fix where author/committer information wasn't correctly passed for file_create/update actions. Updated parameters' description with expected format should you want to add committer and/or author.
* Add new ``github.get_contents`` action which allows user to retrieve file and repository contents.
* Add new ``github.create_file`` action which allows user to create new files in repositories.
* Add new ``github.update_file`` action which allows user to update existing files in repositories.
* Bump libs version in requirements.txt

## 1.1.0

* Add new ``github.get_pull`` action which allows user to retrieve details about
  a specific PR.

## 1.0.0

* Clean up `enterprise_url` params, fixing github enterprise support

## 0.8.4

* Version bump to fix tagging issues, no code changes

## 0.8.3

* Added pull request list/review/merge actions

## 0.8.2

* Strip whitespace from tokens when being stored by a user (Fixes: #14).

## 0.8.1

* Make `repository_sensor` section in config schema optional

## 0.8.0

* Added missing repository\_sensor section to `config.schema.yaml`
* Added example configuration

## 0.7.1

* Update sensor to use ``base_url`` option.

## 0.7.0

* Updated action `runner_type` from `run-python` to `python-script`

## v0.6.3

* Update the parameters for `pack.install` as they have changed.

## v0.6.2

* Remove `immutable: true` from deploy\_payload the parameter in
  deployment\_event action.

## v0.6.1

* Add context parameter to github.add\_status action

## v0.6.0

* Add deployment event webhook.
* Add deployment event workflow to trigger packs.install.
* Add new action check\_deployment\_env env.
* Add deployment\_environment config option.

## v0.5.0

* Migrate config.yaml to config.schema.yaml.
* Add actions and aliases managing releases (list, create, latest).
* Add actions and aliases for managing deployments.
* Add action and aliases for sorting a user scoped GitHub oauth token
  for GitHub.com and GitHub Enterprise.

## v0.4.0

* Add support for Github enterprise by allowing user to provide ``base_url`` option in the config.
  This option can point to a custom URL for the Github Enterprise installations.

## v0.1.0

* Initial release
