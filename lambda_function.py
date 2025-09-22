import os
import json
import boto3
import uuid
from datetime import datetime, timezone

dynamodb = boto3.resource("dynamodb")
s3 = boto3.client("s3")
sns = boto3.client("sns")
cw = boto3.client("cloudwatch")

TABLE_NAME = os.environ.get("TABLE_NAME")               
S3_BUCKET = os.environ.get("S3_BUCKET")                  
SNS_TOPIC_ARN = os.environ.get("SNS_TOPIC_ARN")          
METRIC_NAMESPACE = os.environ.get("METRIC_NAMESPACE", "ContactForm")

CORS_HEADERS = {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
}

def resp(status: int, body: dict | str):
    if not isinstance(body, str):
        body = json.dumps(body)
    return {"statusCode": status, "headers": CORS_HEADERS, "body": body}

def parse_json_body(event):
    """Support both REST (v1) and HTTP API (v2) payloads."""
    body = event.get("body")
    if body is None:
        return None
    if event.get("isBase64Encoded"):
        import base64
        body = base64.b64decode(body).decode("utf-8")
    if isinstance(body, (bytes, bytearray)):
        body = body.decode("utf-8")
    try:
        return json.loads(body)
    except Exception as e:
        print("Failed to parse JSON body:", repr(e))
        return None

def method(event):
    # REST API (v1)
    if "httpMethod" in event:
        return event["httpMethod"]
    # HTTP API (v2)
    if "requestContext" in event and "http" in event["requestContext"]:
        return event["requestContext"]["http"].get("method", "")
    return ""

# main

def lambda_handler(event, context):
    # Log the raw incoming event for debugging
    print("EVENT:", json.dumps(event))

    m = method(event)
    print("HTTP Method:", m)

    # CORS
    if m == "OPTIONS":
        return resp(204, "")

    # health check
    if m == "GET":
        return resp(200, {"message": "Contact Page API is live"})

    if m != "POST":
        return resp(405, {"error": "Method Not Allowed"})

    # validate env
    missing_env = [k for k in ["TABLE_NAME", "S3_BUCKET", "SNS_TOPIC_ARN"] if not os.environ.get(k)]
    if missing_env:
        print("Missing environment variables:", missing_env)
        return resp(500, {"error": f"Missing env vars: {', '.join(missing_env)}"})

    data = parse_json_body(event)
    print("Parsed body:", data)

    if not data:
        return resp(400, {"error": "Invalid or missing JSON body"})

    # validation
    for field in ("fname", "lname", "email", "message"):
        if not str(data.get(field, "")).strip():
            return resp(400, {"error": f"Missing field: {field}"})

    # normalize 
    submission_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc)
    iso = now.isoformat()
    s3_key = f"submission_{now.strftime('%Y%m%d%H%M%S%f')}.json"

    item = {
        "id": submission_id,
        "createdAt": iso,
        "fname": data["fname"].strip(),
        "lname": data["lname"].strip(),
        "email": data["email"].strip(),
        "message": data["message"].strip(),
        "source": "contactus.html",
        "ip": (event.get("requestContext", {}).get("identity", {}).get("sourceIp")
               or event.get("headers", {}).get("X-Forwarded-For", "")),
        "userAgent": event.get("headers", {}).get("User-Agent", ""),
    }

    print("Prepared item:", item)

    try:
        # DynamoDB
        table = dynamodb.Table(TABLE_NAME)
        table.put_item(Item=item)
        print("DynamoDB write success")

        # S3 (analytics)
        s3.put_object(
            Bucket=S3_BUCKET,
            Key=s3_key,
            Body=json.dumps(item).encode("utf-8"),
            ContentType="application/json"
        )
        print("S3 write success:", s3_key)

        # SNS
        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Subject="New Contact Form Submission",
            Message=json.dumps(
                {"id": submission_id, "createdAt": iso, "email": item["email"], "fname": item["fname"], "lname": item["lname"]},
                indent=2
            )
        )
        print("SNS publish success")

        # CloudWatch metric
        cw.put_metric_data(
            Namespace=METRIC_NAMESPACE,
            MetricData=[{
                "MetricName": "MessagesStored",
                "Timestamp": now,
                "Unit": "Count",
                "Value": 1.0,
                "Dimensions": [{"Name": "Pipeline", "Value": "ContactForm"}]
            }]
        )
        print("CloudWatch metric published")

        return resp(200, {"message": "Success", "id": submission_id})

    except Exception as e:
        # Detailed error logging
        print("ERROR during processing:", repr(e))
        return resp(500, {"error": "Internal error", "details": str(e)})
