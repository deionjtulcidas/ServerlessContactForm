import json
import os
import boto3
import time

dynamodb = boto3.client('dynamodb')
cloudwatch = boto3.client('cloudwatch')
sns = boto3.client('sns')

SNS_TOPIC_ARN = "arn:aws:sns:us-east-1:318312871504:ServerlessAppAlerts"  

def lambda_handler(event, context):
    try:
        mypage = page_router(event['httpMethod'], event['queryStringParameters'], event['body'])
        return mypage
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

def page_router(httpmethod, querystring, formbody):
    if httpmethod == 'GET':
        try:
            with open('contactus.html', 'r') as htmlFile:
                htmlContent = htmlFile.read()
            return {
                'statusCode': 200,
                'headers': {"Content-Type": "text/html"},
                'body': htmlContent
            }
        except Exception as e:
            return {
                'statusCode': 500,
                'body': json.dumps({'error': str(e)})
            }

    elif httpmethod == 'POST':
        try:
            insert_record(formbody)

            # Record a metric for successful submission
            record_metric("MessagesStored", 1)

            # Send an SNS alert for new submission
            sns.publish(
                TopicArn=SNS_TOPIC_ARN,
                Subject="New Contact Form Submission",
                Message=f"New message received:\n{formbody}"
            )

            with open('success.html', 'r') as htmlFile:
                htmlContent = htmlFile.read()
            return {
                'statusCode': 200,
                'headers': {"Content-Type": "text/html"},
                'body': htmlContent
            }
        except Exception as e:
            return {
                'statusCode': 500,
                'body': json.dumps({'error': str(e)})
            }

def insert_record(formbody):
    formbody = formbody.replace("=", "' : '")
    formbody = formbody.replace("&", "', '")
    formbody = "INSERT INTO deionstable value {'" + formbody + "'}"

    response = dynamodb.execute_statement(Statement=formbody)
    return response

def record_metric(metric_name, value):
    cloudwatch.put_metric_data(
        Namespace='ServerlessContactApp',
        MetricData=[{
            'MetricName': metric_name,
            'Value': value,
            'Unit': 'Count',
            'Timestamp': time.time()
        }]
    )
