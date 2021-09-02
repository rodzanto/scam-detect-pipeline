import boto3
sm = boto3.client('sagemaker')
def lambda_handler(event, context):
    best_candidate = sm.describe_auto_ml_job(AutoMLJobName=event['auto_ml_job_name'])["BestCandidate"]
    best_candidate_name = best_candidate["CandidateName"]
    print("\n")
    print("CandidateName: " + best_candidate_name)
    print(
        "FinalAutoMLJobObjectiveMetricName: "
        + best_candidate["FinalAutoMLJobObjectiveMetric"]["MetricName"]
    )
    print(
        "FinalAutoMLJobObjectiveMetricValue: "
        + str(best_candidate["FinalAutoMLJobObjectiveMetric"]["Value"])
    )
    return {
        'statusCode': 200,
        'body': 'Best candidate selected.',
        'best_candidate_name':best_candidate_name,
        'best_candidate':best_candidate["InferenceContainers"]
    }
