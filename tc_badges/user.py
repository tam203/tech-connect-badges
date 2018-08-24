from tc_badges.constants import *
from tc_badges import db


def get_stats(user):
    awards = db.get_awards(user)
    total_points = sum(a.points for a in awards)
    ranks = set(a.rank for a in awards)
    if GOLD in ranks:
        best_rank = GOLD
    elif SILVER in ranks:
        best_rank = SILVER
    elif BRONZE in ranks:
        best_rank = BRONZE
    else:
        best_rank = None

    return namedtuple('Stats', ['total_points', 'best_rank', 'total_badges'])(total_points, best_rank, len(awards))
