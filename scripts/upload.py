"""
Upload data/leaderboard.json to Scaleway Object Storage.

Usage:
    uv run python scripts/upload.py

Required environment variables:
    SCW_ACCESS_KEY   — Scaleway IAM access key (needs ObjectStorageFullAccess)
    SCW_SECRET_KEY   — Scaleway IAM secret key

Optional environment variables:
    S3_BUCKET        — bucket name (default: leaderboard)
    S3_KEY           — object key   (default: leaderboard.json)
"""
import os
import pathlib

import boto3
from dotenv import load_dotenv

load_dotenv()

ENDPOINT = "https://s3.nl-ams.scw.cloud"
REGION = "nl-ams"

bucket = os.environ.get("S3_BUCKET", "leaderboard")
key = os.environ.get("S3_KEY", "leaderboard.json")
src = pathlib.Path("data/leaderboard.json")

if not src.exists():
    raise FileNotFoundError(f"{src} not found — run 'dvc repro' first")

s3 = boto3.client(
    "s3",
    endpoint_url=ENDPOINT,
    region_name=REGION,
    aws_access_key_id=os.environ["SCW_ACCESS_KEY"],
    aws_secret_access_key=os.environ["SCW_SECRET_KEY"],
)

s3.upload_file(
    str(src),
    bucket,
    key,
    ExtraArgs={
        "ACL": "public-read",
        "ContentType": "application/json",
        "CacheControl": "max-age=300",
    },
)

public_url = f"https://{bucket}.s3.nl-ams.scw.cloud/{key}"
print(f"Uploaded {src} → s3://{bucket}/{key}")
print(f"Public URL: {public_url}")
