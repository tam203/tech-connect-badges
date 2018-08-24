from flask import Flask, g, request, abort, send_file, redirect
from urllib.request import urlopen, Request
from urllib.parse import urlencode
import json
import os
from jinja2 import Environment, PackageLoader, select_autoescape

from tc_badges.server.analytics import most_post_since
from tc_badges.server.yammer_core import api_request, authenticate, client_id
from tc_badges.server.yammer_user import create_badged_profile_image

import logging
logger = logging.getLogger(__name__.split('.')[0])

j2env = Environment(
    loader=PackageLoader('tc_badges.yammer', 'templates'),
    autoescape=select_autoescape(['html'])
)

app = Flask(__name__)

actions = {
    'get-badged-image': create_badged_profile_image,
    'yammer-analytics': most_post_since
}


@app.route('/')
def index():
    code = request.args.get('code', None)
    if(not code):
        abort(400, description="code was not supplied")
    authenticate(code)

    action = request.args.get('action', None)

    if action not in actions:
        abort(400, description="action was not supplied")

    return actions[action](request.args)


@app.route('/yammer-redirect')
def yammer_oath_redirect():
    # base = "https://www.yammer.com/oauth2/authorize"  # ?client_id={}&response_type=code&redirect_uri=".format(client_id())
    callback = request.url_root.replace('http:', 'https:')  # When local dev running on ngrok we are on https but looks http. This is a fudge.
    callback += '?' + urlencode(list(request.args.items()))
    params = {
        "client_id": client_id(),
        "response_type": "code",
        "redirect_uri": callback
    }
    oauth_url = "https://www.yammer.com/oauth2/authorize?{query}".format(query=urlencode(params))
    logger.info("redirect to %s", oauth_url)
    return redirect(oauth_url, code=302)


@app.route('/quicklinks')
def quicklinks():
    template = j2env.get_template('quicklinks.jinja2')
    return template.render(client_id=client_id(), base_url=request.url_root)
