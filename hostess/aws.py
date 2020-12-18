"""
hostess AWS utilities for pulling cost and usage reports
"""
import boto3

from hostess.config import ORG_NAME

SESSION = boto3.Session()


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
