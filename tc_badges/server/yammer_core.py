from flask import g, request
from urllib.request import urlopen, Request
import json
import os


def client_id():
    return os.environ.get('CLIENT_ID')


def client_secret():
    return os.environ.get('CLIENT_SECRET')


def api_request(url):
    token = g.user['access_token']['token']
    request = Request(url, headers={'Authorization': 'Bearer %s' % token})
    return json.load(urlopen(request))


def authenticate(code):
    url = "https://www.yammer.com/oauth2/access_token.json?client_id={client_id}&client_secret={client_secret}&code={code}".format(
        client_id=client_id(), client_secret=client_secret(), code=code)

    print(url)
    g.user = json.load(urlopen(url))
