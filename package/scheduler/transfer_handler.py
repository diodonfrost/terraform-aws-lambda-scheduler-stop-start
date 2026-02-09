"""AWS Transfer (SFTP) server scheduler."""

from typing import Dict, Iterator, List, Optional

import boto3
from botocore.exceptions import ClientError

from .decorators import skip_on_dry_run
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

    def list_resources(self, aws_tags: List[Dict]) -> Iterator[str]:
        """List Transfer server ARNs matching the given tags."""
        yield from self.tag_api.get_resources("transfer:server", aws_tags)

    def stop(self, aws_tags: List[Dict]) -> None:
        """Stop AWS Transfer servers with defined tags."""
        for server_arn in self.list_resources(aws_tags):
            self._process_server(server_arn.split("/")[-1], "stop")

    def start(self, aws_tags: List[Dict]) -> None:
        """Start AWS Transfer servers with defined tags."""
        for server_arn in self.list_resources(aws_tags):
            self._process_server(server_arn.split("/")[-1], "start")

    @skip_on_dry_run
    def _process_server(self, server_id: str, action: str) -> None:
        """Process a Transfer server with the specified action."""
        try:
            if action == "start":
                self.transfer.start_server(ServerId=server_id)
            else:
                self.transfer.stop_server(ServerId=server_id)
            print(f"{action.capitalize()} Transfer server {server_id}")
        except ClientError as exc:
            transfer_exception("Transfer server", server_id, exc)
