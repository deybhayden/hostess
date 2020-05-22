#!/usr/bin/env python
"""
CLI Tool to print out AWS hosting costs separated by client tag.
"""
import argparse
import asyncio
import concurrent.futures
import locale

import boto3

from config import ORG_NAME, CLIENT_DICT
from utils import Client

locale.setlocale(locale.LC_ALL, "")

SESSION = boto3.Session()


def get_cost_and_usage_total(metrics):
    """Returns Total dollar amount from Cost & Usage metrics response dict."""
    return float(metrics["ResultsByTime"][0]["Total"]["UnblendedCost"]["Amount"])


def create_cost_and_usage_function(client):
    """Creates a client-specific cost and usage reporting function to run in the executor.
    Returns the ClientTotal namedtuple containing results."""

    explorer = SESSION.client("ce")

    def get_client_cur():
        if client.name == ORG_NAME:
            metrics = explorer.get_cost_and_usage(
                TimePeriod={"Start": ARGS.start_date, "End": ARGS.end_date},
                Granularity="MONTHLY",
                Metrics=["UnblendedCost"],
            )
            client.total = get_cost_and_usage_total(metrics)
        elif client.cur_filter:
            metrics = explorer.get_cost_and_usage(
                TimePeriod={"Start": ARGS.start_date, "End": ARGS.end_date},
                Granularity="MONTHLY",
                Metrics=["UnblendedCost"],
                Filter=client.cur_filter,
            )
            client.total = get_cost_and_usage_total(metrics)
        else:
            client.total = 0

        return client

    return get_client_cur


async def get_cost_and_usage_for_clients(executor):
    """Non-blocking function to grab cost and usage data for tagged clients in AWS."""
    loop = asyncio.get_event_loop()
    blocking_tasks = []

    cur_func = create_cost_and_usage_function(Client(ORG_NAME, order=-1))
    blocking_tasks.append(loop.run_in_executor(executor, cur_func))

    for order, (name, cur_filter) in enumerate(CLIENT_DICT.items()):
        client = Client(name, order, cur_filter)
        cur_func = create_cost_and_usage_function(client)
        blocking_tasks.append(loop.run_in_executor(executor, cur_func))

    completed, _pending = await asyncio.wait(blocking_tasks)
    results = [t.result() for t in completed]
    return results


def main():
    """Loop through Client tags for the given date range and print results."""
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=10)
    event_loop = asyncio.get_event_loop()

    results = event_loop.run_until_complete(get_cost_and_usage_for_clients(executor))
    grand_total, tagged_total, hosting_margin = "", 0, 0

    for result in sorted(results, key=lambda r: r.order):
        if result.name == ORG_NAME and result.order == -1:
            grand_total = result.get_formatted_total()
            hosting_margin = result.total
        else:
            tagged_total += result.total
            hosting_margin -= result.total

            if ARGS.verbose:
                print(result.name, result.get_formatted_total())
            else:
                print(result.get_formatted_total())

    if ARGS.verbose:
        print()
        tagged_average = locale.currency(tagged_total / len(CLIENT_DICT), grouping=True)
        formatted_margin = locale.currency(hosting_margin, grouping=True)
        print(f"{ORG_NAME} - Total: {grand_total}")
        print(f"{ORG_NAME} - Tagged Average: {tagged_average}")
        print(f"{ORG_NAME} - Hosting Margin: {formatted_margin}")


if __name__ == "__main__":
    PARSER = argparse.ArgumentParser(
        description="Print out per-client AWS hosting cost details."
    )
    PARSER.add_argument(
        "-s", "--start-date", help="The Start Date - format YYYY-MM-DD", required=True
    )
    PARSER.add_argument(
        "-e", "--end-date", help="The End Date - format YYYY-MM-DD", required=True
    )
    PARSER.add_argument(
        "-v",
        "--verbose",
        help="Display client names and organization metrics in printed results",
        action="store_true",
    )
    ARGS = PARSER.parse_args()
    main()
