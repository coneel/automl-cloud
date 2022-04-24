from sagemaker import AutoML
import sagemaker
import boto3
import csv
import json
import sagemaker
from sagemaker.s3 import S3Uploader,s3_path_join

# get the s3 bucket
sess = sagemaker.Session()
try:
    role = sagemaker.get_execution_role()
except ValueError:
    iam = boto3.client('iam')
    role = iam.get_role(RoleName='AmazonSageMaker-ExecutionRole-20200904T183057')['Role']['Arn']

sagemaker_session_bucket = sess.default_bucket()

# datset files
dataset_csv_file="subsample.csv"

# Autopilot info
autopilot_experiment_name = "autopilot-experiment-1"
automl = AutoML.attach(auto_ml_job_name=autopilot_experiment_name)


# uploads a given file to S3.
input_s3_path = s3_path_join("s3://",sagemaker_session_bucket,"batch_transform/input")
output_s3_path = s3_path_join("s3://",sagemaker_session_bucket,"batch_transform/output")
s3_file_uri = S3Uploader.upload(dataset_csv_file,input_s3_path)

print(f"{dataset_csv_file} uploaded to {s3_file_uri}")


hub = {
    'HF_MODEL_ID':'cardiffnlp/twitter-roberta-base-sentiment',
    'HF_TASK':'text-classification'
}

# create Hugging Face Model Class
best_candidate = automl.describe_auto_ml_job()['BestCandidate']
best_candidate_name = best_candidate['CandidateName']

model = automl.create_model(name=best_candidate_name, 
	                    candidate=best_candidate 
	                    )

#create Transformer to run our batch job
batch_job = model.transformer(
    instance_count=1,
    instance_type='ml.m5.xlarge',
    output_path=output_s3_path, # we are using the same s3 path to save the output with the input
    strategy='SingleRecord')

# starts batch transform job and uses s3 data as input
batch_job.transform(
    data=s3_file_uri,
    content_type='text/csv',    
    split_type='Line')