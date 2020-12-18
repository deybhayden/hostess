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

if "HOSTESS_CONFIG" in os.environ:
    # Set the $HOSTESS_CONFIG variable to the filepath to use a custom
    # Python config file for your own personal settings.
    #
    # Below recipe is pulled from Python Docs - Python 3.5+ support only
    # https://docs.python.org/3/library/importlib.html#importing-a-source-file-directly
    import importlib.util
    import sys

    spec = importlib.util.spec_from_file_location(
        "hostess.config", os.environ["HOSTESS_CONFIG"]
    )
    module = importlib.util.module_from_spec(spec)
    sys.modules["hostess.config"] = module
    spec.loader.exec_module(module)
