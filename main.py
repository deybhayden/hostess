#!/usr/bin/env python
"""
CLI Tool to print out AWS hosting costs separated by client tag.
"""
import argparse
import asyncio
import concurrent.futures
import locale

from rich.console import Console
from rich.table import Table

from config import ORG_NAME, CLIENTS
from utils import Client, create_cost_and_usage_function


async def get_cost_and_usage_for_clients(executor):
    """Non-blocking function to grab cost and usage data for tagged clients in AWS."""
    loop = asyncio.get_event_loop()
    blocking_tasks = []

    cur_func = create_cost_and_usage_function(
        Client(ORG_NAME, order=-1), ARGS.start_date, ARGS.end_date
    )
    blocking_tasks.append(loop.run_in_executor(executor, cur_func))

    for order, client in enumerate(CLIENTS):
        if ARGS.client and client.name != ARGS.client:
            continue

        client.order = order
        cur_func = create_cost_and_usage_function(
            client, ARGS.start_date, ARGS.end_date
        )
        blocking_tasks.append(loop.run_in_executor(executor, cur_func))

    completed, _pending = await asyncio.wait(blocking_tasks)
    results = [t.result() for t in completed]
    return results


def main():
    """Loop through Client tags for the given date range and print results."""
    console = Console()
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Client")
    table.add_column("Total Cost", justify="right")
    table.add_column("Hosting Fee", justify="right")
    table.add_column("Margin", justify="right")

    executor = concurrent.futures.ThreadPoolExecutor(max_workers=10)
    event_loop = asyncio.get_event_loop()

    results = event_loop.run_until_complete(get_cost_and_usage_for_clients(executor))
    grand_total, tagged_total, gap = "", 0, 0

    for result in sorted(results, key=lambda r: r.order):
        # If the result is for the entire organization, it is considered
        # the grand total for the time period and the hosting margin is calculated
        # based on that total.
        if result.name == ORG_NAME and result.order == -1:
            grand_total = result.get_formatted_total_costs()
            gap = result.total_costs
        else:
            tagged_total += result.total_costs
            gap -= result.total_costs

            if ARGS.verbose:
                table.add_row(
                    result.name,
                    result.get_formatted_total_costs(),
                    result.get_formatted_hosting_fee(),
                    result.get_formatted_margin(),
                )
            else:
                console.print(result.get_formatted_total_costs())

    if ARGS.verbose:
        console.print(table)
        if not ARGS.client:
            # Print summary AWS cost total for date range - included avg & untagged costs
            tagged_average = locale.currency(tagged_total / len(CLIENTS), grouping=True)
            formatted_gap = locale.currency(gap, grouping=True)
            console.print(f"{ORG_NAME} - Total: {grand_total}", style="bold green")
            console.print(
                f"{ORG_NAME} - Tagged Average: {tagged_average}", style="bold yellow"
            )
            console.print(
                f"{ORG_NAME} - Untagged Gap: {formatted_gap}", style="bold red"
            )


if __name__ == "__main__":
    locale.setlocale(locale.LC_ALL, "")
    PARSER = argparse.ArgumentParser(
        description="Print out per-client AWS hosting cost details."
    )
    PARSER.add_argument(
        "-s", "--start-date", help="The Start Date - format YYYY-MM-DD", required=True
    )
    PARSER.add_argument(
        "-e", "--end-date", help="The End Date - format YYYY-MM-DD", required=True
    )
    PARSER.add_argument("-c", "--client", help="Report on a single Client")
    PARSER.add_argument(
        "-v",
        "--verbose",
        help="Display client names and organization metrics in printed results",
        action="store_true",
    )
    ARGS = PARSER.parse_args()
    main()
