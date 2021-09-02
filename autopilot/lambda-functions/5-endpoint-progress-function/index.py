import boto3

sm = boto3.client('sagemaker')


def lambda_handler(event, context):
    response = sm.describe_endpoint(
        EndpointName=event['ep_name']
    )

    if response['EndpointStatus'] in ('Deleting', 'Failed'):
        state = 'failed'
        body = 'Endpoint creation failed'

    elif response['EndpointStatus'] == 'InService':
        state = 'complete'
        body = 'Endpoint creation succeeded'

    else:
        state = 'creating'
        body = 'Endpoint creation in progress'

    return {
        'statusCode': 200,
        'body': body,
        'state': state,
        'ep_name': event['ep_name']
    }
