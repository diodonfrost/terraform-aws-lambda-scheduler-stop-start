# -*- coding: utf-8 -*-

"""Exception function for all aws scheduler."""

import logging


def ec2_exception(resource_name: str, resource_id: str, exception) -> None:
    """Exception raised during execution of ec2 scheduler.

    Log instance, spot instance and autoscaling groups exceptions
    on the specific aws resources.

    :param str resource_name:
        Aws resource name
    :param str resource_id:
        Aws resource id
    :param str exception:
        Human readable string describing the exception
    """
    error_codes = ["UnsupportedOperation", "IncorrectInstanceState"]
    if exception.response["Error"]["Code"] in error_codes:
        logging.warning(
            "%s %s: %s", resource_name, resource_id, exception,
        )
    else:
        logging.error(
            "Unexpected error on %s %s: %s",
            resource_name,
            resource_id,
            exception,
        )


def rds_exception(resource_name: str, resource_id: str, exception) -> None:
    """Exception raised during execution of rds scheduler.

    Log rds exceptions on the specific aws resources.

    :param str resource_name:
        Aws resource name
    :param str resource_id:
        Aws resource id
    :param str exception:
        Human readable string describing the exception
    """
    error_codes = [
        "InvalidDBClusterStateFault",
        "InvalidDBInstanceState",
        "InvalidParameterCombination",
    ]
    if exception.response["Error"]["Code"] in error_codes:
        logging.warning(
            "%s %s: %s", resource_name, resource_id, exception,
        )
    else:
        logging.error(
            "Unexpected error on %s %s: %s",
            resource_name,
            resource_id,
            exception,
        )
