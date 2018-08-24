import unittest
from tc_badges import utils
from tc_badges.constants import GOLD, SILVER, BRONZE


class TestUtils(unittest.TestCase):

    def test_get_rank(self):
        self.assertIs(utils.get_rank('gold'), GOLD)
        self.assertIs(utils.get_rank('silver'), SILVER)
        self.assertIs(utils.get_rank('bronze'), BRONZE)

        self.assertIs(utils.get_rank('Bronze'), BRONZE)
        self.assertIs(utils.get_rank('BRONZE'), BRONZE)
        self.assertIs(utils.get_rank('broNZe'), BRONZE)

        with self.assertRaises(ValueError):
            utils.get_rank('someOther')
