"""Configuration module for hostess"""
import os

# Name used in analytics print outs
ORG_NAME = "MegaCrew"

# Client dictionary contains client name as the key with a CUR filter as the value
# Example:
#
#  {"Example Co.": {"Tags": {"Key": "client", "Values": ["example"]}}}
#
CLIENT_DICT = {}

if os.path.exists("config_private.py"):
    # Use config_private for your own personal settings - default to be git ignored.
    # Yup, intentionally using wildcard import to shadow the default values
    from config_private import *
