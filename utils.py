"""
hostess helper classes and functions
"""
import locale

import boto3

from config import ORG_NAME

SESSION = boto3.Session()


class Client(object):
    """Client helper class to organize client details and AWS totals."""

    def __init__(self, name, order=0, cur_filter=None, hosting_fee=0, total_costs=0):
        self.name = name
        self.order = order
        self.cur_filter = cur_filter
        self.hosting_fee = hosting_fee
        self.total_costs = total_costs

    def get_formatted_total_costs(self):
        """Returns a locale appropriate currency formatted total costs string."""
        return locale.currency(self.total_costs, grouping=True)

    def get_formatted_hosting_fee(self):
        """Returns a locale appropriate currency formatted hosting fee string."""
        return locale.currency(self.hosting_fee, grouping=True)

    def get_formatted_margin(self):
        """Returns a locale appropriate currency formatted hosting margin string."""
        return locale.currency(self.hosting_fee - self.total_costs, grouping=True)


def get_cost_and_usage_total(metrics):
    """Returns Total dollar amount from Cost & Usage metrics response dict."""
    return float(metrics["ResultsByTime"][0]["Total"]["UnblendedCost"]["Amount"])


def create_cost_and_usage_function(client, start_date, end_date):
    """Creates a client-specific cost and usage reporting function to run in the executor.
    Returns the ClientTotal namedtuple containing results."""

    explorer = SESSION.client("ce")

    def get_client_cur():
        if client.name == ORG_NAME:
            metrics = explorer.get_cost_and_usage(
                TimePeriod={"Start": start_date, "End": end_date},
                Granularity="MONTHLY",
                Metrics=["UnblendedCost"],
            )
            client.total_costs = get_cost_and_usage_total(metrics)
        elif client.cur_filter:
            metrics = explorer.get_cost_and_usage(
                TimePeriod={"Start": start_date, "End": end_date},
                Granularity="MONTHLY",
                Metrics=["UnblendedCost"],
                Filter=client.cur_filter,
            )
            client.total_costs = get_cost_and_usage_total(metrics)
        else:
            client.total_costs = 0

        return client

    return get_client_cur
