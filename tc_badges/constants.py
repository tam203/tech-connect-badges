import os
from collections import namedtuple

Rank = namedtuple('Rank', ['name', 'min_points', 'max_points'])
GOLD = Rank("gold", 100, 1000)
SILVER = Rank("silver", 10, 100)
BRONZE = Rank("bronze", 1, 10)
RANKS = {r.name: r for r in [BRONZE, SILVER, GOLD]}
BUCKET_NAME = os.environ['TC_BADGES_BUCKET']
AVAILABLE_BADGE_PREFIX = 'available'
RANK_META = 'rank'
AWARD_FOR_META = 'award-for'
POINTS_META = 'points'
REASON_META = 'reason'
NAME_META = 'name'
BADGE_META = 'badge'
SPECIFIC_AWARD_REASON_META = 'reason-awarded'
AWARDED_PREFIX = 'awarded'
DATE = 'date'
REGION = 'eu-west-2'
URL_BASE = "https://s3.eu-west-2.amazonaws.com/" + BUCKET_NAME
