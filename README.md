# Hostess

CLI tool to separate AWS hosting costs by client for a given date range.

## Installation

This script uses [asyncio](https://docs.python.org/3/library/asyncio.html), so Python 3+ is required to run it.

```bash
# ...set up a virtualenv and activate it...
pip install -r requirements.txt
```

## Usage

The example below uses [AWS SSO CLI credentials](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-sso.html) to federate access to AWS accounts.

```bash
# you'll need awscli v2, your SSO URL & region and to have set that all up correctly
aws configure sso
aws sso login --profile my_profile
./main.py -s 2020-04-01 -e 2020-05-01 -v
```
