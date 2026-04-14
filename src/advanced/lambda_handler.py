import boto3
import json
import os
from datetime import datetime, timezone

def handler(event, context):
    try:
        body = json.loads(event.get("body", "{}"))
        text = body.get("text", "").strip()

        if not text:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Missing 'text' in request body."})
            }

        environment = os.environ["ENVIRONMENT"]
        bucket = os.environ["S3_BUCKET_NAME"]
        region = os.environ.get("AWS_REGION", "us-east-1")
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        s3_key = f"polly-audio/{environment}/{timestamp}.mp3"
        tmp_path = f"/tmp/{timestamp}.mp3"

        polly = boto3.client("polly", region_name=region)
        response = polly.synthesize_speech(
            Text=text,
            OutputFormat="mp3",
            VoiceId="Joanna",
            Engine="neural",
        )

        with open(tmp_path, "wb") as f:
            f.write(response["AudioStream"].read())

        s3 = boto3.client("s3")
        s3.upload_file(tmp_path, bucket, s3_key)

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Synthesis complete.",
                "s3_uri": f"s3://{bucket}/{s3_key}",
                "environment": environment,
                "timestamp": timestamp,
            })
        }
    except Exception as exc:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(exc)})
        }
