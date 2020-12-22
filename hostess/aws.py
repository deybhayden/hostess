"""
hostess AWS utilities for pulling cost and usage reports
"""
import boto3

from hostess.config import ORG_NAME


def get_cost_and_usage_total(metrics):
    """Returns Total dollar amount from Cost & Usage metrics response dict."""
    return float(metrics["ResultsByTime"][0]["Total"]["UnblendedCost"]["Amount"])


class AWSSession:
    """Utility class to organize Boto3 calls for a given date range."""

    def __init__(self, start_date, end_date):
        self.boto_session = boto3.Session()
        self.start_date = start_date
        self.end_date = end_date

    def get_tag_values(self, tag, value_prefix):
        """For the given tag, return a list of all values that begin with the different
        prefixes in AWS Cost Explorer for start & end dates."""
        explorer = self.boto_session.client("ce")
        values = []
        next_token = None
        get_tags_kwargs = {
            "SearchString": value_prefix,
            "TimePeriod": {"Start": self.start_date, "End": self.end_date},
            "TagKey": tag,
        }

        while True:
            if next_token:
                get_tags_kwargs["NextPageToken"] = next_token

            response = explorer.get_tags(**get_tags_kwargs)
            values += response["Tags"]

            if "NextPageToken" in response:
                next_token = response["NextPageToken"]
            else:
                break

        return values

    def create_cost_and_usage_function(self, client):
        """Creates a client-specific cost and usage reporting function to run in the executor.
        Returns the ClientTotal namedtuple containing results."""
        explorer = self.boto_session.client("ce")

        def get_client_cur():
            if client.name == ORG_NAME:
                metrics = explorer.get_cost_and_usage(
                    TimePeriod={"Start": self.start_date, "End": self.end_date},
                    Granularity="MONTHLY",
                    Metrics=["UnblendedCost"],
                )
                client.total_costs = get_cost_and_usage_total(metrics)
            elif client.cur_filter:
                # Ensure all tagged values are captured for the date range
                self.update_tag_values(client)
                metrics = explorer.get_cost_and_usage(
                    TimePeriod={"Start": self.start_date, "End": self.end_date},
                    Granularity="MONTHLY",
                    Metrics=["UnblendedCost"],
                    Filter=client.cur_filter,
                )
                client.total_costs = get_cost_and_usage_total(metrics)
            else:
                client.total_costs = 0

            return client

        return get_client_cur

    def update_tag_values(self, client):
        """For the passed date range, find all valid Tags Values and
        update the client.cur_filter with the values."""
        updated = False
        for key in client.cur_filter:
            if key == "Tags":
                self._update_tag_object(client.cur_filter[key])
                updated = True
            elif key in ("And", "Or"):
                # Go a level deeper and search for Tags
                for obj in client.cur_filter[key]:
                    if "Tags" in obj:
                        self._update_tag_object(obj["Tags"])
                        updated = True
                        break

            if updated:
                break

    def _update_tag_object(self, tag_object):
        """For the given Tags Filter object, update the values list with all
        tagged values in the AWSSession date range."""
        new_values = []
        for value in tag_object["Values"]:
            new_values += self.get_tag_values(tag_object["Key"], value)

        if new_values:
            # Only update values if it's a non-empty list to avoid a Boto error
            tag_object["Values"] = new_values
