import argparse
import boto3
from PIL import Image
from tc_badges.utils import slug, key_to_url
from tc_badges.constants import RANK_META, AWARD_FOR_META, NAME_META, BUCKET_NAME, AVAILABLE_BADGE_PREFIX
import io

s3 = boto3.resource('s3')


def make_key(name):
    return "{prefix}/{slug}.png".format(prefix=AVAILABLE_BADGE_PREFIX, slug=slug(name))


def create_badge(image_file, name, rank, description):

    # Check image type and size and format if needed
    im = Image.open(image_file)
    if(im.width != 512 or im.height != 512 or im.format != 'PNG'):
        print('Resizing')
        im = im.resize((512, 512))
        im_data = io.BytesIO()
        im.save(im_data, format='PNG')
        im_data.seek(0)
    else:
        im_data = open(image_file, 'rb')

    key = make_key(name)
    s3.Bucket(BUCKET_NAME).put_object(
        Key=key,
        Body=im_data.read(),
        ContentType='image/png',
        ACL='public-read',
        Metadata={
            RANK_META: rank,
            AWARD_FOR_META: description,
            NAME_META: name
        }
    )
    print("Created badge {name} see {url}".format(
        name=name, url=key_to_url(key)))


def main(args=None):
    parser = argparse.ArgumentParser(description='Create a new badge')

    parser.add_argument('image',
                        help='path to the 512 by 512 PNG that is the visual part of the badge')

    parser.add_argument('name',
                        help='The badge name')

    parser.add_argument('rank', choices=['bronze', 'silver', 'gold'],
                        help='The badge rank/value')

    parser.add_argument('description',
                        help='Why people are awarded the badge')

    args = parser.parse_args(args)
    create_badge(args.image, args.name, args.rank, args.description)


if __name__ == "__main__":
    main()
