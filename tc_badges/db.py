from tc_badges.constants import *
from tc_badges.utils import get_rank, slug
from hashlib import sha256
from tc_badges import aws
from tc_badges.badges import Badge, Award
import json


def get_id(email):
    email = email.lower().strip()
    return sha256(email.encode('utf-8')).hexdigest()[:6]


def get_available_badge_slugs():
    items = aws.get_client().list_objects_v2(
        Bucket=BUCKET_NAME,
        Prefix=AVAILABLE_BADGE_PREFIX)
    return list(map(lambda item: item['Key'].split('/')[-1][:-4], items['Contents']))


def get_awards(user):
    user_id = get_id(user)
    prefix = "%s/%s" % (AWARDED_PREFIX, user_id)
    items = aws.get_client().list_objects_v2(
        Bucket=BUCKET_NAME,
        Prefix=prefix)

    def to_award(result):
        s3_object = aws.get_bucket().Object(result['Key'])
        info = json.load(s3_object.get()['Body'])
        return Award(info[BADGE_META], get_rank(info[RANK_META]),  info[REASON_META], info[POINTS_META], info[DATE])
    return list(map(to_award, items['Contents']))


def create_badge(badge):
    key = "{prefix}/{slug}.png".format(prefix=AVAILABLE_BADGE_PREFIX, slug=slug(badge.name))
    aws.get_bucket().put_object(
        Key=key,
        Body=badge.img,
        ContentType='image/png',
        ACL='public-read',
        Metadata={
            RANK_META: badge.rank.name,
            AWARD_FOR_META: badge.award_for,
            NAME_META: badge.name,
            POINTS_META: badge.points
        }
    )
    return Badge(badge.name, badge.rank, badge.award_for, badge.points, key)


def get_badge(slug):
    url = "%s/%s/%s.png" % (URL_BASE, AVAILABLE_BADGE_PREFIX, slug)
    badge_object = aws.get_bucket().get_object(url)
    rank = get_rank(badge_object['Metadata'][RANK_META])
    return Badge(badge_object['Metadata'][NAME_META],
                 rank,
                 badge_object['Metadata'][AWARD_FOR_META],
                 float(badge_object['Metadata'][POINTS_META]),
                 slug)


def award_badge(badge, user, reason, date, points=None):
    points = points if points else badge.points
    uid = get_id(user)
    key = "%s/%s/%s.json" % (AWARDED_PREFIX, uid, badge.slug)
    payload = {
        REASON_META: reason,
        'date': date.isoformat(),
        'points': points,
        'badge': badge.key
    }
    aws.get_bucket().put_object(
        Key=key,
        Body=json.dumps(payload).encode('utf-8'),
        ContentType='application/json',
        ACL='public-read',
    )
