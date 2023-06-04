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
    info_codes = ["IncorrectInstanceState"]
    warning_codes = [
        "UnsupportedOperation",
        "IncorrectInstanceState",
        "InvalidParameterCombination",
    ]

    if exception.response["Error"]["Code"] in info_codes:
        logging.info(
            "%s %s: %s",
            resource_name,
            resource_id,
            exception,
        )
    elif exception.response["Error"]["Code"] in warning_codes:
        logging.warning(
            "%s %s: %s",
            resource_name,
            resource_id,
            exception,
        )
    else:
        logging.error(
            "Unexpected error on %s %s: %s",
            resource_name,
            resource_id,
            exception,
        )


def ecs_exception(resource_name: str, resource_id: str, exception) -> None:
    """Exception raised during execution of ecs scheduler.

    Log instance, spot instance and autoscaling groups exceptions
    on the specific aws resources.

    :param str resource_name:
        Aws resource name
    :param str resource_id:
        Aws resource id
    :param str exception:
        Human readable string describing the exception
    """
    info_codes = ["ClusterNotFoundException"]
    warning_codes = [
        "ServiceNotActiveException",
        "ServiceNotFoundException",
        "InvalidParameterException",
    ]

    if exception.response["Error"]["Code"] in info_codes:
        logging.info(
            "%s %s: %s",
            resource_name,
            resource_id,
            exception,
        )
    elif exception.response["Error"]["Code"] in warning_codes:
        logging.warning(
            "%s %s: %s",
            resource_name,
            resource_id,
            exception,
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
    info_codes = ["InvalidParameterCombination", "DBClusterNotFoundFault"]
    warning_codes = ["InvalidDBClusterStateFault", "InvalidDBInstanceState"]

    if exception.response["Error"]["Code"] in info_codes:
        logging.info(
            "%s %s: %s",
            resource_name,
            resource_id,
            exception,
        )
    elif exception.response["Error"]["Code"] in warning_codes:
        logging.warning(
            "%s %s: %s",
            resource_name,
            resource_id,
            exception,
        )
    else:
        logging.error(
            "Unexpected error on %s %s: %s",
            resource_name,
            resource_id,
            exception,
        )


def cloudwatch_exception(resource_name: str, resource_id: str, exception):
    """Exception raised during execution of Cloudwatch scheduler.

    Log Cloudwatch exceptions on the specific aws resources.

    :param str resource_name:
        Aws resource name
    :param str resource_id:
        Aws resource id
    :param str exception:
        Human readable string describing the exception
    """
    logging.error(
        "Unexpected error on %s %s: %s",
        resource_name,
        resource_id,
        exception,
    )
