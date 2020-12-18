#!/usr/bin/env python
"""
CLI Tool to print out AWS Cost Explorer Dimension values.
"""
import argparse
from pprint import pprint

import boto3


SESSION = boto3.Session()


def main():
    """
    Print AWS GetDimensionValues()
    """
    explorer = SESSION.client("ce")
    values = explorer.get_dimension_values(
        Dimension=ARGS.dimension,
        TimePeriod={"Start": ARGS.start_date, "End": ARGS.end_date},
    )

    pprint(values)


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
        "-d",
        "--dimension",
        help="Display client names and organization metrics in printed results",
        choices=[
            "AZ",
            "INSTANCE_TYPE",
            "LINKED_ACCOUNT",
            "LINKED_ACCOUNT_NAME",
            "OPERATION",
            "PURCHASE_TYPE",
            "REGION",
            "SERVICE",
            "SERVICE_CODE",
            "USAGE_TYPE",
            "USAGE_TYPE_GROUP",
            "RECORD_TYPE",
            "OPERATING_SYSTEM",
            "TENANCY",
            "SCOPE",
            "PLATFORM",
            "SUBSCRIPTION_ID",
            "LEGAL_ENTITY_NAME",
            "DEPLOYMENT_OPTION",
            "DATABASE_ENGINE",
            "CACHE_ENGINE",
            "INSTANCE_TYPE_FAMILY",
            "BILLING_ENTITY",
            "RESERVATION_ID",
            "RESOURCE_ID",
            "RIGHTSIZING_TYPE",
            "SAVINGS_PLANS_TYPE",
            "SAVINGS_PLAN_ARN",
            "PAYMENT_OPTION",
        ],
        required=True,
    )
    ARGS = PARSER.parse_args()
    main()
