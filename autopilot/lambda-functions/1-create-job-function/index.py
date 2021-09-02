import boto3, os
import json
from datetime import datetime

client = boto3.client('sagemaker')
iam = boto3.client('iam')

JOB_NAME = 'autoML' + str(round(datetime.now().timestamp()))
MAX_CANDIDATES = 5
MAX_TIME_TRAINING_JOB = 600
MAX_TIME_AUTOML_JOB = 3600
PROBLEM_TYPE = "BinaryClassification"
TARGET_ATTRIBUTE_NAME = "scam"
TARGET_METRIC = "AUC"
GENERATE_CANDIDATE_DEFINITIONS_ONLY = False
SAGEMAKER_ARN = iam.get_role(RoleName=os.environ['SageMakerRoleName'])['Role']['Arn']


def lambda_handler(event, context):
    print(SAGEMAKER_ARN)
    response = client.create_auto_ml_job(
        AutoMLJobName=JOB_NAME,
        AutoMLJobConfig={
            'CompletionCriteria': {
                'MaxCandidates': MAX_CANDIDATES,
                'MaxRuntimePerTrainingJobInSeconds': MAX_TIME_TRAINING_JOB,
                'MaxAutoMLJobRuntimeInSeconds': MAX_TIME_AUTOML_JOB
            }
        },
        InputDataConfig=[
            {
                'DataSource': {
                    'S3DataSource': {
                        'S3DataType': 'S3Prefix',
                        'S3Uri': 's3://' + event['bucket_name'] + '/' + event['file_key']
                    }
                },
                'CompressionType': 'None',
                'TargetAttributeName': TARGET_ATTRIBUTE_NAME
            },
        ],
        OutputDataConfig={
            'S3OutputPath': 's3://' + event['bucket_name'] + '/output/'
        },
        ProblemType=PROBLEM_TYPE,
        AutoMLJobObjective={
            'MetricName': TARGET_METRIC
        },
        GenerateCandidateDefinitionsOnly=GENERATE_CANDIDATE_DEFINITIONS_ONLY,
        RoleArn=SAGEMAKER_ARN
    )

    print('AutoML job created: ' + JOB_NAME)

    return {
        'statusCode': 200,
        'body': json.dumps('Job Created'),
        'auto_ml_job_name': JOB_NAME
    }
