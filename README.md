## AWS Serverless Contact Form Project
Overview

This project is a serverless contact form application built on AWS. It allows users to submit their name, email, and message through a web form, storing submissions in DynamoDB and making the data available for analysis via QuickSight. The project leverages serverless architecture for scalability, security, and low maintenance.

## Features

Responsive contact form built with HTML and CSS.

Serverless backend using AWS Lambda and API Gateway.

Form submissions are:

Stored in DynamoDB.

Published to Amazon SNS for alerts.

Saved as JSON files in S3 for integration with QuickSight dashboards.

CloudWatch metrics track form submission counts.

Fully automated DynamoDB → S3 → QuickSight workflow for analytics.

Clean, modern UI with subtle animations.

## Architecture
Frontend: Static HTML/CSS form.

Backend: Lambda function triggered via API Gateway.

Data Storage: DynamoDB table for structured form data.

Analytics: S3 bucket receives JSON files from DynamoDB streams; QuickSight visualizes the data.

Notifications: SNS topic sends alerts for each new submission.

Monitoring: CloudWatch logs and metrics track usage and errors.

## Technologies Used
AWS Lambda

Amazon API Gateway

Amazon DynamoDB

Amazon S3

Amazon SNS

Amazon CloudWatch

Amazon QuickSight

HTML/CSS/JavaScript

## How It Works

User opens the contact form webpage.

Submission triggers a POST request to API Gateway → Lambda.

Lambda stores the data in DynamoDB, publishes to SNS, and saves a JSON file in S3.

DynamoDB Streams ensure data flows to S3 for QuickSight dashboards.

CloudWatch metrics track submission count in real time Deployment

Lambda deployed with IAM permissions to access DynamoDB, SNS, and S3.

API Gateway configured as HTTP endpoint for the frontend form.

S3 bucket configured as data lake for QuickSight analytics.

## Author

Deion Jose Tulcidas 
