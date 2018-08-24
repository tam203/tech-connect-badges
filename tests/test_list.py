import unittest
from unittest.mock import patch
from tc_badges.constants import GOLD
from tc_badges.badges import Badge


class TestCreate(unittest.TestCase):
    @patch("tc_badges.db.get_awards")
    def test_award_badge(self, get_awards):
        raise NotImplemented("To Do")
