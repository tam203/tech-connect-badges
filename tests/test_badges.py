import unittest
from tc_badges.badges import PotentialBadge, Badge, Award
from tc_badges.constants import *
from datetime import datetime


class TestBadges(unittest.TestCase):

    def test_automatic_point_assignment(self):
        rank = GOLD
        badge = PotentialBadge("badge1", None, rank, None)
        expect_points = (rank.min_points + rank.max_points) / 2
        self.assertEqual(badge.points, expect_points)

    def test_out_of_range_point_assignment(self):
        rank = SILVER
        with self.assertRaises(ValueError):
            PotentialBadge("b2", None, rank, None, points=200)

    def test_get_slug_from_badge(self):
        slug = 'a-badge'
        badge = Badge("a badge", GOLD, "something", 102, 'this/is/the/%s.png' % slug)
        self.assertEqual(badge.slug, slug)

    def test_award(self):
        award = ('award-one', GOLD, 'for a thing', 500, datetime.now().isoformat())
        got_award = Award(*award)
        self.assertEqual(got_award.badge, award[0])
        self.assertEqual(got_award.rank, award[1])
        self.assertEqual(got_award.reason, award[2])
        self.assertEqual(got_award.points, award[3])
        self.assertEqual(got_award.date, award[4])
        self.assertEqual(got_award.image, "%s/%s/%s/%s.png" % (URL_BASE, BUCKET_NAME, AVAILABLE_BADGE_PREFIX, award[0]))
