from sagemaker import AutoML
import sagemaker
import boto3

autopilot_experiment_name = "autopilot-experiment-1"
automl = AutoML.attach(auto_ml_job_name=autopilot_experiment_name)

batch_output = 's3://automl-output-preds'
batch_input = 's3://batch-input-bucket/subsample.csv'
#batch_input = 'boston-housing-dataset'


sess = sagemaker.Session()
try:
    role = sagemaker.get_execution_role()
except ValueError:
    iam = boto3.client('iam')
    role = iam.get_role(RoleName='AmazonSageMaker-ExecutionRole-20200904T183057')['Role']['Arn']
sagemaker_session_bucket = sess.default_bucket()

print(role)


best_candidate = automl.describe_auto_ml_job()['BestCandidate']
best_candidate_name = best_candidate['CandidateName']

model = automl.create_model(name=best_candidate_name, 
	                    candidate=best_candidate 
	                    )

all_candidates = automl.list_candidates(sort_by='FinalObjectiveMetricValue', 
                                         sort_order="Descending", 
			                 max_results=100)
			               
			               
#print(all_candidates)

transformer = model.transformer(instance_count=1, 
				 instance_type='ml.m5.xlarge',
				 assemble_with='Line',
				 output_path=batch_output)
				 
transformer.transform(data=batch_input,
                      split_type='Line',
		      content_type='text/csv',
		      wait=False)