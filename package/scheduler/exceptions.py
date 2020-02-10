# -*- coding: utf-8 -*-

"""Exception function for all aws scheduler."""

import logging


def ec2_exception(resource_name, resource_id, exception):
    """Exception raised during execution of ec2 scheduler.

    Log ec2 exceptions on the specific aws resources

    :param str resource_name:
        Aws resource name
    :param str resource_id:
        Aws resource id
    :param str exception:
        Exception message
    """
    error_code = exception.response["Error"]["Code"]
    if error_code == "UnsupportedOperation":
        logging.warning(
            "%s %s: %s", resource_name, resource_id, exception,
        )
    elif error_code == "IncorrectInstanceState":
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
