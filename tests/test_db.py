import unittest
from tc_badges.badges import PotentialBadge
from tc_badges import db
from tc_badges.constants import *
from tc_badges.utils import slug, get_rank
from tc_badges.badges import PotentialBadge, Badge
from datetime import datetime
import json
import io


class TestDB(unittest.TestCase):

    @unittest.mock.patch('tc_badges.db.aws.get_client')
    def test_list_badges(self, get_client):
        slugs = ['badge', 'award-for-thing', 'you-got-this']
        list_objects_v2 = get_client.return_value.list_objects_v2
        list_objects_v2.return_value = {'Contents': [
            {'Key': "%s/%s.png" % (AVAILABLE_BADGE_PREFIX, slug)} for slug in slugs
        ]}
        self.assertEqual(db.get_available_badge_slugs(), slugs)
        list_objects_v2.called_with(Bucket=BUCKET_NAME, Prefix=AVAILABLE_BADGE_PREFIX)

    @unittest.mock.patch('tc_badges.db.aws.get_bucket')
    def test_create_badge_sets_bucket_props(self, get_bucket):
        badge = PotentialBadge("A Badge", None, BRONZE, "for this", 5)
        db.create_badge(badge)
        called_with = get_bucket.return_value.put_object.call_args[1]
        self.assertEqual(called_with['ContentType'], 'image/png')
        self.assertEqual(called_with['ACL'], 'public-read')
        self.assertEqual(called_with['Key'], '%s/%s.png' % (AVAILABLE_BADGE_PREFIX, slug(badge.name)))
        self.assertEqual(called_with['Body'], badge.img)
        self.assertEqual(called_with['Metadata'][NAME_META], badge.name)
        self.assertEqual(called_with['Metadata'][RANK_META], badge.rank.name)
        self.assertEqual(called_with['Metadata'][AWARD_FOR_META], badge.award_for)
        self.assertEqual(called_with['Metadata'][POINTS_META], badge.points)

    @unittest.mock.patch('tc_badges.db.aws.get_bucket')
    def test_create_badge_returns_badge(self, get_bucket):
        badge_to_create = PotentialBadge("A Badge", None, BRONZE, "for this", 5)
        badge = db.create_badge(badge_to_create)

        for prop in ['name', 'award_for', 'rank', 'points']:
            self.assertEqual(getattr(badge, prop), getattr(badge_to_create, prop))

        self.assertEqual(badge.key, "%s/%s.png" % (AVAILABLE_BADGE_PREFIX, slug(badge.name)))

    @unittest.mock.patch('tc_badges.db.aws.get_bucket')
    def test_get_badge(self, get_bucket):

        slug = 'a-badge'
        url = "%s/%s/%s.png" % (URL_BASE, AVAILABLE_BADGE_PREFIX, slug)
        badge = PotentialBadge("A Badge", None, BRONZE, "something", 2)
        rank = BRONZE
        points = 3
        get_bucket.return_value.get_object.return_value = {
            'Body': None,
            'Metadata': {
                RANK_META: badge.rank.name,
                AWARD_FOR_META: badge.award_for,
                POINTS_META: str(badge.points),
                NAME_META: badge.name
            }
        }
        got_badge = db.get_badge(slug)

        get_bucket.return_value.get_object.assert_called_once_with(url)

        for prop in ['name', 'award_for', 'rank', 'points']:
            self.assertEqual(getattr(got_badge, prop), getattr(badge, prop))

    @unittest.mock.patch('tc_badges.db.aws.get_bucket')
    def test_award_badge(self, get_bucket):

        # Set up
        slug = "a-badge"
        reason = "for thing"
        date = datetime.now()
        user = "a@a.com"
        uid = db.get_id(user)
        key = "%s/%s/%s.json" % (AWARDED_PREFIX, uid, slug)
        points = 300
        badge = Badge('A badge', GOLD, "some thing", 200, 'path/to/%s.png' % slug)

        db.award_badge(badge,  user, reason, date, points)

        def test_expected(points):
            expected_payload = {
                'badge': badge.key,
                'reason': reason,
                'points': points,
                'date': date.isoformat()
            }
            called_with = get_bucket.return_value.put_object.call_args[1]
            self.assertEqual(called_with['ContentType'], 'application/json')
            self.assertEqual(called_with['ACL'], 'public-read')
            self.assertEqual(called_with['Key'], key)
            sent_payload = json.dumps(json.loads(called_with['Body'].decode('utf-8')), sort_keys=True)
            self.assertEqual(sent_payload, json.dumps(expected_payload, sort_keys=True))

        # test with specified points
        db.award_badge(badge,  user, reason, date, points)
        test_expected(points)

        # test with default points
        db.award_badge(badge,  user, reason, date)
        test_expected(badge.points)

    @unittest.mock.patch('tc_badges.db.aws.get_bucket')
    @unittest.mock.patch('tc_badges.db.aws.get_client')
    def test_get_awards(self, get_client, get_bucket):
        awards = [
            ('award-one', 'gold', 500, 'for a thing', datetime.now().isoformat()),
            ('award-two', 'bronze', 3, 'for a thing 2', datetime.now().isoformat()),
            ('award-three', 'silver', 52, 'for a thing 3', datetime.now().isoformat())
        ]
        user = "a@a.com"
        userid = db.get_id(user)

        list_objects_v2 = get_client.return_value.list_objects_v2
        list_objects_v2.return_value = {'Contents': [{'Key': "%s/%s/%s.json" % (AWARDED_PREFIX, userid, award[0])} for award in awards]}

        obj = None

        def s3_object(key):
            obj = list(filter((lambda a: a[0] in key), awards))[0]

            def get():
                return {'Body': io.BytesIO(json.dumps({
                    BADGE_META: obj[0],
                    RANK_META: obj[1],
                    POINTS_META: obj[2],
                    REASON_META: obj[3],
                    DATE: obj[4]
                }).encode('utf-8'))}
            return namedtuple('Object', ['get'])(get)

        get_bucket.return_value.Object.side_effect = s3_object

        got_awards = db.get_awards(user)

        list_objects_v2.assert_called_with(Bucket=BUCKET_NAME, Prefix="%s/%s" % (AWARDED_PREFIX, userid))

        for i, award in enumerate(awards):
            got = got_awards[i]
            self.assertEqual(got.badge, award[0])
            self.assertEqual(got.rank, get_rank(award[1]))
            self.assertEqual(got.points, award[2])
            self.assertEqual(got.reason, award[3])
            self.assertEqual(got.date, award[4])
