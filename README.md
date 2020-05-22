# Hostess

CLI tool to separate AWS hosting costs by client for a given date range.

## Installation

This script uses [asyncio](https://docs.python.org/3/library/asyncio.html), so Python 3+ is required to run it.

```
$ ...set up a virtualenv and activate it...
$ pip install -r requirements.txt
```

## Usage

The example below uses [aws-okta](https://github.com/segmentio/aws-okta) to federate access to AWS accounts.

```
$ aws-okta exec root-admin -- ./main.py -s 2020-04-01 -e 2020-05-01 -v
```
