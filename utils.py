"""
hostess helper classes and functions
"""
import locale


class Client(object):
    """Client helper class to organize client details and AWS totals."""

    def __init__(self, name, order=0, cur_filter=None, total=0):
        self.name = name
        self.order = order
        self.cur_filter = cur_filter
        self.total = total

    def get_formatted_total(self):
        """Returns a locale appropriate currency formatted total string."""
        return locale.currency(self.total, grouping=True)
