
import boto3
from tc_badges.constants import BUCKET_NAME


def get_bucket():
    s3 = boto3.resource('s3')
    return s3.Bucket(BUCKET_NAME)


def get_client():
    return boto3.client('s3')
