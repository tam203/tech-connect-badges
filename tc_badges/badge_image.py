from PIL import Image
from urllib.request import urlopen
from io import BytesIO
import io
import os
from tc_badges.user import get_stats


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
    stats = get_stats(user)
    print(stats)

    for i, img_url in enumerate(map(key_to_url, get_users_badge_keys(get_id(user)))):
        b_img = img_from_url(img_url)
        b_img.thumbnail((b_size, b_size))
        add_badge(base, b_img, i)

    im_data = io.BytesIO()
    base.save(im_data, format='PNG')
    im_data.seek(0)
    return im_data


if __name__ == '__main__':
    outfile = os.path.abspath('example-output.png')
    with open(outfile, 'wb') as fp:
        fp.write(badge_image('theo.mccaie@metoffice.gov.uk',
                             'http://news.images.itv.com/image/file/662255/stream_img.jpg').read())
        print('take a look at %s' % outfile)
