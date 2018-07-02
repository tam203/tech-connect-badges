from PIL import Image
from urllib.request import urlopen, Request
from io import BytesIO
from tc_badges.utils import get_users_badge_keys, get_id, key_to_url
from flask import Flask, send_file, request, abort
import io
import os
import json


def img_from_url(url):
    file = BytesIO(urlopen(url).read())
    return Image.open(file)


def add_badge(img, b_img, b_number):
    x_off = b_number * b_img.width
    y_off = 0
    while (x_off > img.width - b_img.width):
        x_off = 0
        y_off += b_img.height

    img.paste(b_img, (x_off, y_off), b_img)


def badge_image(user, user_image):

    base = img_from_url(user_image)

    ref_size = max(base.width, base.height)
    b_size = ref_size / 5

    for i, img_url in enumerate(map(key_to_url, get_users_badge_keys(get_id(user)))):
        b_img = img_from_url(img_url)
        b_img.thumbnail((b_size, b_size))
        add_badge(base, b_img, i)

    im_data = io.BytesIO()
    base.save(im_data, format='PNG')
    im_data.seek(0)
    return im_data


app = Flask(__name__)


def get_users_details(code):
    url = "https://www.yammer.com/oauth2/access_token.json?client_id={client_id}&client_secret={client_secret}&code={code}".format(
        client_id=os.environ.get('CLIENT_ID'), client_secret=os.environ.get('CLIENT_SECRET'), code=code)
    user_info = json.load(urlopen(url))
    return user_info


@app.route('/')
def badged_image():
    code = request.args.get('code', None)

    if(not code):
        abort(400, description="code was not supplied")

    user = get_users_details(code)

    user_info_request = Request('https://www.yammer.com/api/v1/users/current.json',
                                headers={'Authorization': 'Bearer %s' % user['access_token']['token']})

    email = user['user']['email']
    mugshot = user['user']['mugshot_url_template'].replace(
        '{width}', '500').replace('{height}', '500')

    user = urlopen(user_info_request)
    return send_file(badge_image(email, mugshot), mimetype='image/png')


if __name__ == '__main__':
    outfile = os.path.abspath('example-output.png')
    with open(outfile, 'wb') as fp:
        fp.write(badge_image('alastair.gemmell@metoffice.gov.uk',
                             'http://news.images.itv.com/image/file/662255/stream_img.jpg').read())
        print('take a look at %s' % outfile)
