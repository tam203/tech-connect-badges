from tc_badges.constants import URL_BASE, AVAILABLE_BADGE_PREFIX, BUCKET_NAME


class PotentialBadge():
    def __init__(self, name, img, rank, award_for, points=None):

        points = points if points else (rank.max_points + rank.min_points) / 2
        if not (rank.min_points <= points <= rank.max_points):
            raise ValueError("Point value %s invalid. Must be between %s and %s for badge"
                             " rank %s" % (points, rank.min_points, rank.max_points, rank.name))
        self.name = name
        self.img = img
        self.rank = rank
        self.award_for = award_for
        self.points = points


class Badge():
    def __init__(self, name, rank, awarded_for, points, key):
        self.name = name
        self.rank = rank
        self.award_for = awarded_for
        self.points = points
        self.key = key

    @property
    def slug(self):
        return self.key.split('.png')[0].split('/')[-1]


class Award():
    def __init__(self, badge, rank, reason, points, date):
        self.badge = badge
        self.rank = rank
        self.reason = reason
        self.points = points
        self.date = date

    @property
    def image(self):
        return "%s/%s/%s/%s.png" % (URL_BASE, BUCKET_NAME, AVAILABLE_BADGE_PREFIX, self.badge)
