"""Configuration module for hostess"""
import os

# Name used in analytics print outs
ORG_NAME = "MegaCrew"

# utils.Client object list containing client names as well as an optional CUR filter
# Example:
#
# CLIENTS = [
#     Client("Example Co.", cur_filter={"Tags": {"Key": "client", "Values": ["example"]}}})
# ]
#
CLIENTS = []

if os.path.exists("config_private.py"):
    # Use config_private for your own personal settings - default to be git ignored.
    # Yup, intentionally using wildcard import to shadow the default values
    from config_private import *
