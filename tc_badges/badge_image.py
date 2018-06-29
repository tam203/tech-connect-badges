from PIL import Image
from urllib import request
from io import BytesIO
from tc_badges.utils import get_users_badge_keys, get_id, key_to_url
from flask import send_file
from flask import Flask
import io


def img_from_url(url):
    file = BytesIO(request.urlopen(url).read())
    return Image.open(file)


def add_badge(img, b_img, b_number):
    x_off = b_number * b_img.width
    y_off = 0
    while (x_off > img.width - b_img.width):
        x_off = 0
        y_off += b_img.height

    img.paste(b_img, (x_off, y_off), b_img)


def process_img(img_url="https://pbs.twimg.com/profile_images/2686801698/ede6590742131c7700de5a058d94f742_400x400.jpeg"):

    base = img_from_url(img_url)

    ref_size = max(base.width, base.height)
    b_size = ref_size / 5

    for i, img_url in enumerate(map(key_to_url, get_users_badge_keys(get_id('theo.mccaie2@informaticslab.co.uk')))):
        b_img = img_from_url(img_url)
        b_img.thumbnail((b_size, b_size))
        add_badge(base, b_img, i)

    im_data = io.BytesIO()
    base.save(im_data, format='PNG')
    im_data.seek(0)
    return im_data


app = Flask(__name__)


@app.route('/')
def badged_image():
    return send_file(process_img(), mimetype='image/png')
