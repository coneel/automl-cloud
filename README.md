# Final Project - Autopilot Machine Learning Housing Price Predictor


![CloudDiagram](https://user-images.githubusercontent.com/68971919/164986388-71c3b92b-b872-41d6-b901-2388479a3d61.jpg)


## Overview
In this project we used Sagemaker Autopilot to create and deploy a model to predict housing prices. The model can predict on new data, store these predictions in S3, and automatically email the predictions to you. 

## Project Infrastructure:
This project was primarily housed in the AWS Cloud9 enviroment connected to Github via SSH key. I have set up a makefile to download python packages needed to run the lambda function such as boto3, pylint, Pandas, Sagemaker, datetime and xlrd. The makefile also is used to lint the code, and identify any bugs in the process. This helps with automating the data pipeline. Within the actions of GitHub, I have set it up so that it automatically lints before it can push to github. 

## Code
Autopilot is accessed via Sagemaker studio and allows you to enter the desired parameter, and response varaible you want to measure. From there, autopilot handles all data preprocessing and expiramentation. It runs over 250 different models and selects the best one depending on the metric selected. 

The model can be accessed via cloud9 using the sagemaker SDK. This allows you to bring in the best mode, and run a batch transform job on new data to make predictions. Predictions can be interacted with in cloud9 leveraging the results.py file. Additionally, a lambda function was utilized to run when predictions are generated to pull the results from the s3 bucket where they are housed, and send them to your email. 

### Noteable Functions

sendCSV.py - Lambda function to access the bucket where the predictions are sent to. It parses through the CSV and extracts the predictions and uses SNS to send them to a specified email list. 

mml.py - Interacts with the Sagemaker SDK to retreive the model and make predictions. Takes local CSV of values to predict on, and sends them to S3 where they can be accessed by the model. Starts a batch job to generate predictions, and sends these predictions to the S3 bucket.

results.py - allows you to pull in the results from the s3 bucket to interact with them if desired. 

## Future plans
I would like to potentially incorporate an additional component that scrapes a website to give a quick blurb about daily news associated with each of the stocks. However, I have not find a great website that allows scraping for this portion of it. I would also like to create a front in interface that allows anyone to upload their portfolio and preferred message settings to receive their own messages. 
