import unittest
from tc_badges import award
from unittest.mock import patch
from tc_badges.badges import PotentialBadge
from tc_badges.constants import GOLD
from datetime import datetime
import os.path
from tc_badges.badges import Badge


class TestCreate(unittest.TestCase):
    @patch("tc_badges.db.award_badge")
    @patch("tc_badges.db.get_badge")
    def test_award_badge(self, get_badge, award_badge):

        badge = Badge("this badge", GOLD, "Something or other", 200, 'path/to/badge.png')
        user = "a@o.com"
        reason = r"'cause cool"
        date = datetime.now()

        get_badge.return_value = badge

        award.award_badge(user, badge.slug, reason)
        award_badge.assert_called_with(badge, user, reason, None)

        award.award_badge(user, badge.slug, reason, date)
        award_badge.assert_called_with(badge, user, reason, date)
