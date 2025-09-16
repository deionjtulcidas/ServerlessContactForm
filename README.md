## Real-Time Serverless Contact Form

This project is a serverless contact management system built to handle form submissions in real time. It leverages AWS Lambda, API Gateway, DynamoDB, SNS, and CloudWatch to capture submissions, send instant notifications, and monitor performance. Submissions are securely stored in DynamoDB, and email notifications are sent via SNS.

I implemented least-privilege IAM roles and optional KMS encryption to follow security best practices. CloudWatch dashboards track latency, execution duration, and errors, ensuring reliability and observability. The system is fully automated and reproducible using Terraform and GitHub Actions, making it production-ready while serving as a polished portfolio/demo project.

## Key Highlights:

End-to-end serverless architecture using AWS services

Real-time notifications and monitoring

Secure and reliable design with IAM and optional encryption

Automated deployments with Terraform + GitHub Actions

## Additional Features:

Spam protection using reCAPTCHA

Multi-channel notifications via Slack and SNS

Analytics dashboard using DynamoDB Streams + QuickSight

Monitoring with CloudWatch for latency, errors, and performance under high traffic (10k+ requests/sec)

Security with IAM least-privilege roles and KMS encryption

Automated deployments using Terraform and GitHub Actions for reproducible and production-ready operations
