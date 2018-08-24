from tc_badges.server.yammer_core import api_request
from collections import namedtuple
from operator import attrgetter
from flask import jsonify
from datetime import datetime

import logging
logger = logging.getLogger(__name__.split('.')[0])

TC_GROUP_POSTS = "https://www.yammer.com/api/v1/messages/in_group/11965929.json"


class Message():
    def __init__(self, yammer_msg):
        self.likes = yammer_msg['liked_by']['count']
        self.sender_id = yammer_msg['sender_id']
        self.text = yammer_msg['body']['plain']
        self.web_url = yammer_msg['web_url']


def most_post_since(args):
    from_date = args.get('from_date', None)
    to_date = args.get('to_date', None)
    from_date = datetime.strptime(from_date + " 00:00:00 +0000", "%Y-%m-%d %M:%H:%S %z") if from_date else None
    to_date = datetime.strptime(to_date + " 23:59:59 +0000", "%Y-%m-%d %M:%H:%S %z") if to_date else None

    messages = (Message(m) for m in get_posts(from_date=from_date, to_date=to_date))
    ordered_by_likes = list(sorted(messages, key=attrgetter('likes'), reverse=True))
    most_liked = [m for m in ordered_by_likes if m.likes == ordered_by_likes[0].likes]
    logging.info("Most liked: %s", most_liked)
    return jsonify(most_liked)


def get_posts(from_date=None, to_date=None, max_times=15):
    older_available = True
    older_than = None
    i = 0
    while older_available and i < max_times:
        i += 1
        url = TC_GROUP_POSTS if not older_than else TC_GROUP_POSTS + '?older_than=' + str(older_than)

        logger.info("Fetch messages from url: %s", url)

        posts = api_request(url)

        for msg in posts['messages']:
            post_date = datetime.strptime(msg['created_at'], "%Y/%m/%d %H:%M:%s %z")
            if(post_date > from_date):
                # TODO: fihish making from and to date work
                continue
            yield msg

        older_available = posts['meta']['older_available']
        if len(posts['messages']) == 0 or not older_available:
            break

        older_than = posts['messages'][-1]['id']
