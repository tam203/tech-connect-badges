#!/usr/bin/env python3

import argparse
import re
import datetime

from tc_badges.constants import *
from tc_badges import db


DATE_FORMAT = "%Y-%m-%d"


def valid_date(s):
    try:
        return datetime.datetime.strptime(s, "%Y-%m-%d")
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(s)
        raise argparse.ArgumentTypeError(msg)


def award_badge(user, slug, reason, date=None):
    badge = db.get_badge(slug)
    db.award_badge(badge, user, reason, date)


def main(args=None):
    parser = argparse.ArgumentParser(description='Create a new badge')

    parser.add_argument('badge',
                        choices=db.get_available_badge_slugs(),
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
