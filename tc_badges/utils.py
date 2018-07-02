from hashlib import sha256
import re
import boto3
from tc_badges.constants import BUCKET_NAME, AWARDED_PREFIX, REGION


def get_id(email):
    email = email.lower().strip()
    return sha256(email.encode('utf-8')).hexdigest()[:6]


def slug(name):
    slug = re.sub('[ -]+', '_', name)
    slug = re.sub('\W', '', slug).lower().strip()
    return slug


def get_users_badge_keys(id):
    prefix = "{}/{}/".format(AWARDED_PREFIX, id)
    return [b['Key'] for b in boto3.client('s3').list_objects_v2(Bucket=BUCKET_NAME, Prefix=prefix).get('Contents', [])]


def key_to_url(key):
    return 'https://s3.{region}.amazonaws.com/tech-connect-badges/{key}'.format(region=REGION, key=key)
