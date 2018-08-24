#!/usr/bin/env python3

import argparse
import boto3
import re
import datetime

from tc_badges.constants import DATE, RANK_META, AWARD_FOR_META, SPECIFIC_AWARD_REASON_META, NAME_META, BUCKET_NAME, AVAILABLE_BADGE_PREFIX, AWARDED_PREFIX
from tc_badges.utils import get_id

s3 = boto3.resource('s3')
s3Client = boto3.client('s3')
DATE_FORMAT = "%Y-%m-%d"


def list_badges():
    items = s3Client.list_objects_v2(
        Bucket=BUCKET_NAME,
        Prefix=AVAILABLE_BADGE_PREFIX)
    return list(map(lambda item: item['Key'].split('/')[-1][:-4], items['Contents']))


def valid_date(s):
    try:
        return datetime.datetime.strptime(s, "%Y-%m-%d")
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(s)
        raise argparse.ArgumentTypeError(msg)


def award_badge(user, badge_slug, reason, date):
    target_badge_key = "{prefix}/{slug}.png".format(
        prefix=AVAILABLE_BADGE_PREFIX, slug=badge_slug)
    badge = s3.Bucket(BUCKET_NAME).Object(target_badge_key).get()
    meta = badge['Metadata']
    meta[SPECIFIC_AWARD_REASON_META] = reason
    meta[DATE] = date
    key = '{prefix}/{user}/{slug}.png'.format(
        prefix=AWARDED_PREFIX, user=get_id(user), slug=badge_slug)

    # s3.Bucket(BUCKET_NAME).put_object(
    #     Key=key,
    #     Body=badge['Body'].read(),
    #     ContentType='image/png',
    #     Metadata=meta,
    #     ACL='public-read'
    # )


def main(args=None):
    parser = argparse.ArgumentParser(description='Create a new badge')

    parser.add_argument('badge',
                        choices=list_badges(),
                        help='the name of the badge object in s3 minus the .png')

    parser.add_argument('user',
                        help='The email address of the person to award this too')

    parser.add_argument('reason',
                        help='The reason for the specific award')

    parser.add_argument('--date', metavar='YYY-MM-DD', default=datetime.datetime.now().strftime(DATE_FORMAT),
                        help='The date awarded. Defaults to current date.')

    args = parser.parse_args(args)

    award_badge(args.user, args.badge, args.reason, args.date)


if __name__ == "__main__":
    main()
