from sagemaker.s3 import S3Downloader
from ast import literal_eval
import boto3
import csv
import json
import sagemaker
import pandas as pd
from sagemaker.s3 import S3Uploader,s3_path_join

# get the s3 bucket
sess = sagemaker.Session()
try:
    role = sagemaker.get_execution_role()
except ValueError:
    iam = boto3.client('iam')
    role = iam.get_role(RoleName='AmazonSageMaker-ExecutionRole-20200904T183057')['Role']['Arn']

sagemaker_session_bucket = sess.default_bucket()


print(sagemaker_session_bucket)


# dataset
dataset_csv_file="subsample.csv"


# uploads a given file to S3.
input_s3_path = s3_path_join("s3://",sagemaker_session_bucket,"batch_transform/input")
output_s3_path = s3_path_join("s3://",sagemaker_session_bucket,"batch_transform/output")
s3_file_uri = S3Uploader.upload(dataset_csv_file,input_s3_path)



# creating s3 uri for result file -> input file + .out
output_file = f"{dataset_csv_file}.out"
output_path = s3_path_join(output_s3_path,output_file)

# download file
S3Downloader.download(output_path,'.')

batch_transform_result = []
with open(output_file) as f:
    for line in f:
        # converts jsonline array to normal array
        line = "[" + line.replace("[","").replace("]",",") + "]"
        batch_transform_result = literal_eval(line) 
        
# print results 
print(batch_transform_result)
#out = pd.read_csv('/automl-cloud/subsample.csv.out')
#print(out)