"""AWS Transfer (SFTP) server scheduler."""

from typing import Dict, List, Literal, Optional

import boto3
from botocore.exceptions import ClientError

from .exceptions import transfer_exception
from .filter_resources_by_tags import FilterByTags


class TransferScheduler:
    """AWS Transfer (SFTP) server scheduler for controlling servers."""

    def __init__(self, region_name: Optional[str] = None) -> None:
        """Initialize Transfer scheduler.

        Args:
            region_name: AWS region name. Uses default configuration if not specified.
        """
        self.transfer = (
            boto3.client("transfer", region_name=region_name)
            if region_name
            else boto3.client("transfer")
        )
        self.tag_api = FilterByTags(region_name=region_name)

    def stop(self, aws_tags: List[Dict]) -> None:
        """Stop AWS Transfer servers with defined tags.

        Args:
            aws_tags: AWS tags to filter resources.
                Example: [{'Key': 'Environment', 'Values': ['Dev']}]
        """
        self._process_servers(aws_tags, action="stop")

    def start(self, aws_tags: List[Dict]) -> None:
        """Start AWS Transfer servers with defined tags.

        Args:
            aws_tags: AWS tags to filter resources.
                Example: [{'Key': 'Environment', 'Values': ['Dev']}]
        """
        self._process_servers(aws_tags, action="start")

    def _process_servers(
        self, aws_tags: List[Dict], action: Literal["start", "stop"]
    ) -> None:
        """Process Transfer servers with the specified action.

        Args:
            aws_tags: AWS tags to filter resources.
            action: Action to perform ("start" or "stop").
        """
        for server_arn in self.tag_api.get_resources("transfer:server", aws_tags):
            server_id = server_arn.split("/")[-1]
            try:
                if action == "start":
                    self.transfer.start_server(ServerId=server_id)
                    print(f"Start Transfer server {server_id}")
                else:
                    self.transfer.stop_server(ServerId=server_id)
                    print(f"Stop Transfer server {server_id}")
            except ClientError as exc:
                transfer_exception("Transfer server", server_id, exc)
