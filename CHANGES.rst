# Changelog

## 0.7.1

* Update sensor to use ``base_url`` option. 

## 0.7.0

* Updated action `runner_type` from `run-python` to `python-script`

## v0.6.3

* Update the parameters for `pack.install` as they have changed.

## v0.6.2

* Remove `immutable: true` from deploy_payload the parameter in
  deployment_event action.

## v0.6.1

* Add context parameter to github.add_status action

## v0.6.0

* Add deployment event webhook.
* Add deployment event workflow to trigger packs.install.
* Add new action check_deployment_env env.
* Add deployment_environment config option.

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
