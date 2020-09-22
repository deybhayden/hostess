#!/usr/bin/env python
"""
CLI Tool to print out AWS hosting costs separated by client tag.
"""
import argparse
import asyncio
import concurrent.futures
import locale

import boto3
from rich.console import Console
from rich.table import Table

from config import ORG_NAME, CLIENTS
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

    for order, client in enumerate(CLIENTS):
        if ARGS.client and client.name != ARGS.client:
            continue

        client.order = order
        cur_func = create_cost_and_usage_function(client)
        blocking_tasks.append(loop.run_in_executor(executor, cur_func))

    completed, _pending = await asyncio.wait(blocking_tasks)
    results = [t.result() for t in completed]
    return results


def main():
    """Loop through Client tags for the given date range and print results."""
    console = Console()
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Client")
    table.add_column("Total", justify="right")

    executor = concurrent.futures.ThreadPoolExecutor(max_workers=10)
    event_loop = asyncio.get_event_loop()

    results = event_loop.run_until_complete(get_cost_and_usage_for_clients(executor))
    grand_total, tagged_total, hosting_margin = "", 0, 0

    for result in sorted(results, key=lambda r: r.order):
        # If the result is for the entire organization, it is considered
        # the grand total for the time period and the hosting margin is calculated
        # based on that total.
        if result.name == ORG_NAME and result.order == -1:
            grand_total = result.get_formatted_total()
            hosting_margin = result.total
        else:
            tagged_total += result.total
            hosting_margin -= result.total

            if ARGS.verbose:
                table.add_row(result.name, result.get_formatted_total())
            else:
                console.print(result.get_formatted_total())

    if ARGS.verbose:
        console.print(table)
        tagged_average = locale.currency(tagged_total / len(CLIENTS), grouping=True)
        formatted_margin = locale.currency(hosting_margin, grouping=True)
        console.print(f"{ORG_NAME} - Total: {grand_total}", style="bold green")
        console.print(
            f"{ORG_NAME} - Tagged Average: {tagged_average}", style="bold yellow"
        )
        console.print(
            f"{ORG_NAME} - Hosting Margin: {formatted_margin}", style="bold red"
        )


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
        "-c", "--client", help="Report on a single Client"
    )
    PARSER.add_argument(
        "-v",
        "--verbose",
        help="Display client names and organization metrics in printed results",
        action="store_true",
    )
    ARGS = PARSER.parse_args()
    main()
