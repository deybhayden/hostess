"""Configuration module for hostess"""
import os

# Name used in analytics print outs
ORG_NAME = "MegaCrew"

# utils.Client object list containing client names as well as an optional CUR filter
# Example:
#
# CLIENTS = [
#     Client(
#         "Example Co.",
#         cur_filter={"Tags": {"Key": "client", "Values": ["example"]}},
#         hosting_fee=2400,
#     )
#     Client(
#         name="Second INC.",
#         cur_filter={
#             "Or": [
#                 {"Tags": {"Key": "client", "Values": ["second"]}},
#                 {
#                     "Dimensions": {
#                         "Key": "LINKED_ACCOUNT",
#                         "Values": ["123456789101", "234567890123", "345678901234"],
#                     }
#                 },
#             ]
#         },
#         hosting_fee=500
#     ),
#     Client(
#         name="Third Inc. S3 Costs",
#         cur_filter={
#             "And": [
#                 {"Tags": {"Key": "environment", "Values": ["third"]}},
#                 {
#                     "Dimensions": {
#                         "Key": "SERVICE",
#                         "Values": ["Amazon Simple Storage Service"],
#                     }
#                 },
#             ]
#         },
#         hosting_fee=1000
#     ),
# ]
#
CLIENTS = []

if os.path.exists("config_private.py"):
    # Use config_private for your own personal settings - default to be git ignored.
    # Yup, intentionally using wildcard import to shadow the default values
    from hostess.config_private import *
