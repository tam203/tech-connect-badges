import unittest
from tc_badges import create
from unittest.mock import patch
from tc_badges.badges import PotentialBadge
from tc_badges.constants import GOLD
import os.path


class TestCreate(unittest.TestCase):

    @patch("sys.exit")
    def test_cant_give_to_many_points_for_rank(self, exit):
        for points, rank in [(10, 'gold'), (-1, 'bronze'), (0, 'bronze'), (20, 'bronze'), (9, 'silver'), (101, 'silver')]:
            args = ["some.png", "a badge", rank, "cause they rock",  "--points=%d" % points]
            with self.assertRaises(ValueError):
                create.parse_args(args)

    @patch("tc_badges.db.create_badge")
    def test_creates_badge(self, mock_create_badge):
        name = 'name'
        points = 550
        given_for = 'stuff etc'
        rank = GOLD
        image_path = os.path.join(os.path.dirname(__file__), 'test_img.png')
        with open(image_path, 'rb') as img:
            expected_badge = PotentialBadge(name, img.read(), rank, given_for, points)

        create.create_badge(image_path, name, rank, given_for, points)
        mock_create_badge.assert_called_once()
        got_badge = mock_create_badge.call_args[0][0]

        for prop in ['name', 'img', 'award_for', 'rank', 'points']:
            self.assertEqual(getattr(got_badge, prop), getattr(expected_badge, prop))
