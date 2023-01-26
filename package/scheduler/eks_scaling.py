import botocore
import boto3
import os

cluster_name = os.environ['cluster_name']
min_size = int(os.environ['min_size'])
desired_size = int(os.environ['desired_size'])
max_size = int(os.environ['max_size'])

client = boto3.client('eks')

def lambda_handler(event, context):

    list_nodegroups = client.list_nodegroups(
        clusterName = cluster_name
    )

    def update_nodegroup(nodegroup_name):
        
        update = client.update_nodegroup_config(
            clusterName = cluster_name,
            nodegroupName = nodegroup_name,
            scalingConfig = {
                'minSize': min_size,
                'desiredSize': desired_size,
                'maxSize': max_size
            }
        )

        status_code = update['ResponseMetadata']['HTTPStatusCode']

        if status_code == 200:
            status = "OK"
        else: 
            status = "ERROR"

        return nodegroup_name + ": " + str(status_code) + " (" + status + ")"

    return_codes = []

    for n in list_nodegroups['nodegroups']:

        return_codes.append(update_nodegroup(n))

    return return_codes
