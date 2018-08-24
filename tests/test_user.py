import unittest
from tc_badges import user
from tc_badges.constants import GOLD, SILVER, BRONZE
from tc_badges.badges import Award
from datetime import datetime


class TestUtils(unittest.TestCase):

    @unittest.mock.patch('tc_badges.user.db.get_awards')
    def test_get_user_stats(self, get_awards):
        get_awards.return_value = [
            Award('...', GOLD, 'ff', 320, datetime.now().isoformat()),
            Award('...', SILVER, 'fff', 20, datetime.now().isoformat()),
            Award('...', SILVER, 'fff', 3, datetime.now().isoformat()),
        ]
        username = 'user@user.com'

        stats = user.get_stats(username)

        get_awards.assert_called_with(username)
        self.assertEquals(stats.total_points, 343)
        self.assertEquals(stats.best_rank, GOLD)
        self.assertEquals(stats.total_badges, 3)
