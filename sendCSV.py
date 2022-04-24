import json
import csv
import boto3
import botocore
import os
from os import listdir
import json




DOWNLOAD_BUCKET = 'sagemaker-us-east-1-512201658062'


def lambda_handler(event, context):
    # TODO implement
    s3csvName = event['Records'][0]['s3']['object']['key'].split('/')[-1]
    s3csvName = "batch_transform/output/" + s3csvName
    local_path = download_csv_from_s3(s3csvName, DOWNLOAD_BUCKET)
    f = open(local_path)
    csv_f = csv.reader(f)   
    data = []
    nested_json = []

    for row in csv_f:
        for el in row:
            nested_json.append(el)
            data.append('<data>' + el + '</data>' + os.linesep)
    f.close()
    map = {};
    map = {"data": nested_json}
    nf = open('/tmp/output.xml', 'a');
    str_output = "<?xml version=\"1\" encoding=\"UTF-8\" ?>" + os.linesep + "<sampleData>";
    nf.write("<?xml version=\"1\" encoding=\"UTF-8\" ?>" + os.linesep + "<sampleData>")
    for row in data:
        str_output += row
        nf.write(row)
    str_output += '</sampleData>'
    nf.write('\\n</sampleData>')
    nf.close()
        
    
    return {
        "xml_output": str_output,
        "jsonOuput": json.dumps(map)
    }
    
    
    
def download_csv_from_s3(path, bucket=DOWNLOAD_BUCKET):
    """Downloads mp4 locally from the s3 bucket"""
    s3 = boto3.resource('s3')
    if not os.path.exists('/tmp'):
        os.makedirs('/tmp')
    local_dir = "/tmp"

    filename = path.split("/")[-1]
    local_path = os.path.join(local_dir,filename)
    try:
        s3.Bucket(bucket).download_file(str(path), str(local_path))
        # print("files in temp: " + glob.glob("/tmp/*"))
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The object does not exist.")
        else:
            raise

    return local_path
