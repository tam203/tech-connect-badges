import re
import boto3
from tc_badges.constants import *
from collections import namedtuple


def slug(name):
    slug = re.sub('[ -]+', '_', name)
    slug = re.sub(r'\W', '', slug).lower().strip()
    return slug


def get_rank(rank_name):
    try:
        return next(r for r in RANKS.values() if r.name.upper() == rank_name.upper())
    except StopIteration:
        raise ValueError("%s is not a valid rank" % rank_name)
