import json, boto3, os

sm = boto3.client('sagemaker')
iam = boto3.client('iam')
SAGEMAKER_ARN = iam.get_role(RoleName=os.environ['SageMakerRoleName'])['Role']['Arn']


def lambda_handler(event, context):
    best_candidate = event["best_candidate"]
    best_candidate_name = event["best_candidate_name"]
    ep_name = best_candidate_name + "-ep"
    epc_name = best_candidate_name + "-epC"

    model_name = best_candidate_name + "-model"
    model_arn = sm.create_model(
        Containers=best_candidate,
        ModelName=model_name,
        ExecutionRoleArn=SAGEMAKER_ARN
    )

    ep_config = sm.create_endpoint_config(
        EndpointConfigName=epc_name,
        ProductionVariants=[
            {
                "InstanceType": "ml.m5.2xlarge",
                "InitialInstanceCount": 1,
                "ModelName": model_name,
                "VariantName": "main",
            }
        ],
    )

    create_endpoint_response = sm.create_endpoint(EndpointName=ep_name,
                                                  EndpointConfigName=epc_name)
    print(create_endpoint_response)

    return {
        'statusCode': 200,
        'body': 'Endpoint for best candidate initiated.',
        'ep_name': ep_name
    }
