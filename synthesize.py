import boto3
import os
import sys

def synthesize_speech(text, output_file, voice_id="Joanna"):
    polly = boto3.client("polly", region_name=os.environ["AWS_REGION"])
    response = polly.synthesize_speech(
        Text=text,
        OutputFormat="mp3",
        VoiceId=voice_id,
        Engine="neural",
    )
    with open(output_file, "wb") as f:
        f.write(response["AudioStream"].read())
    print(f"[polly] Audio written to {output_file}")

def upload_to_s3(local_path, bucket, s3_key):
    s3 = boto3.client("s3")
    s3.upload_file(local_path, bucket, s3_key)
    print(f"[s3] Uploaded to s3://{bucket}/{s3_key}")

if __name__ == "__main__":
    environment = os.environ.get("ENVIRONMENT", "beta")
    bucket = os.environ.get("S3_BUCKET_NAME")

    with open("speech.txt", "r", encoding="utf-8") as f:
        content = f.read().strip()

    if not content:
        print("[error] speech.txt is empty.")
        sys.exit(1)

    local_output = "output.mp3"
    s3_key = f"polly-audio/{environment}.mp3"

    synthesize_speech(content, local_output)

    if bucket:
        upload_to_s3(local_output, bucket, s3_key)
    else:
        print(f"[info] No S3_BUCKET_NAME set — dry run only.")