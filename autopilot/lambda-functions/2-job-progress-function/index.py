import boto3

sm = boto3.client('sagemaker')

def lambda_handler(event, context):
    if "Payload" in event:
        job_name = event['Payload']['auto_ml_job_name']
    else:
        job_name = event['auto_ml_job_name']

    print("Job Name: " + job_name)
    print("JobStatus - Secondary Status")
    print("------------------------------")

    describe_response = sm.describe_auto_ml_job(AutoMLJobName=job_name)
    print(describe_response["AutoMLJobStatus"] + " - " + describe_response["AutoMLJobSecondaryStatus"])
    job_run_status = describe_response["AutoMLJobStatus"]

    if job_run_status in ("Failed", "Stopped"):
        state = 'failed'
        body = 'Job failed.'
    elif job_run_status == "Completed":
        state = 'complete'
        body = 'Job completed.'
    else:
        state = 'running'
        body = 'Job in progress.'
    return {
        'statusCode': 200,
        'body': body,
        'auto_ml_job_name': job_name,
        'state': state
    }
