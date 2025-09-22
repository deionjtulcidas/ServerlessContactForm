AWS Serverless Contact Form
Overview

This project is a fully serverless contact form application built on AWS. It allows users to submit their name, email, and message through a responsive web form, with all submissions processed and stored using AWS managed services. The architecture is designed for scalability, low operational overhead, and real-time monitoring.

Features

Responsive frontend built with HTML, CSS, and JavaScript.

Serverless backend powered by API Gateway and AWS Lambda.

Form submissions are automatically:

Stored in DynamoDB for persistence.

Saved as JSON objects in S3 for long-term storage and analytics.

Published to Amazon SNS for real-time alerts.

Counted with CloudWatch custom metrics for monitoring.

GitHub Actions CI/CD pipeline deploys static assets to S3.

Modern UI with a clean design and subtle animations.

Architecture

Frontend: Static HTML/CSS/JS contact form hosted in S3.

Backend: Lambda function triggered by API Gateway endpoint.

Storage: DynamoDB (structured data) + S3 (analytics data).

Notifications: SNS topic sends alerts on each submission.

Monitoring: CloudWatch tracks logs, metrics, and errors.

(Future enhancement) Integration with Athena + QuickSight for dashboarding.

Technologies Used

AWS Lambda

Amazon API Gateway

Amazon DynamoDB

Amazon S3

Amazon SNS

Amazon CloudWatch

GitHub Actions

HTML/CSS/JavaScript

How It Works

User fills out and submits the contact form.

A POST request is sent to API Gateway, which invokes a Lambda function.

Lambda:

Stores the submission in DynamoDB.

Writes a JSON copy to S3.

Publishes an alert to SNS.

Emits a custom CloudWatch metric.

Submissions can be viewed in DynamoDB, S3, or monitored in CloudWatch.
