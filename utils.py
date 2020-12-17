"""
hostess helper classes and functions
"""
import locale


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
