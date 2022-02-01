# Hostess

CLI tool to separate AWS hosting costs by client for a given date range.

## Development

This utility uses [asyncio](https://docs.python.org/3/library/asyncio.html), so Python 3+ is required to run it.

Below is an easy setup using [Pipenv](https://github.com/pypa/pipenv).

```bash
pipenv --python 3.10.2
pipenv install --dev
```

:warning: This tool supports Python 3.8+ and up.

### Private Configuration

By default, there is an empty `hostess.config` Python file that contains example config variables and possible values. You can override these defaults by setting the `$HOSTESS_CONFIG` environment variable to the filepath of your own organization's client configuration. Below example uses [direnv](https://direnv.net/) to set per directory environment variables.

```bash
mkdir -p ~/code
cd ~/code
gh repo clone deybhayden/hostess
cd hostess/
# example assumes a Python file is located at ~/.config/hostess/config.py
echo "export HOSTESS_CONFIG=\"$HOME/.config/hostess/config.py\"" > .envrc
direnv allow
```

## Usage

The example below uses [AWS SSO CLI credentials](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-sso.html) to federate access to AWS accounts.

```bash
# you'll need awscli v2, your SSO URL & region and to have set that all up correctly
aws configure sso
aws sso login --profile my_profile
pipenv shell
pipenv install -e .
hostess -s 2020-04-01 -e 2020-05-01 -v
# write a month of results to CSV to import into a spreadsheet
hostess -s 2021-07-01 -e 2021-08-01 -f july.csv
```
