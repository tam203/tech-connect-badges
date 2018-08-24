from flask import g, send_file
from tc_badges.badge_image import badge_image


def create_badged_profile_image(args=None):
    user = g.user
    email = user['user']['email']
    mugshot = user['user']['mugshot_url_template'].replace(
        '{width}', '500').replace('{height}', '500')
    return send_file(badge_image(email, mugshot), mimetype='image/png')
