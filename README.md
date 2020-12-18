# Hostess

CLI tool to separate AWS hosting costs by client for a given date range.

## Development

This utility uses [asyncio](https://docs.python.org/3/library/asyncio.html), so Python 3+ is required to run it.

Below is an easy setup using [Pipenv](https://github.com/pypa/pipenv).

```bash
pipenv --python 3.8
pipenv install --dev
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
```
