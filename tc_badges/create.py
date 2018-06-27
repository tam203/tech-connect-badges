import argparse
import boto3

from tc_badges.utils import slug
from tc_badges.constants import RANK_META, AWARD_FOR_META, NAME_META, BUCKET_NAME, AVAILABLE_BADGE_PREFIX

s3 = boto3.resource('s3')


def make_key(name):
    return "{prefix}/{slug}.png".format(prefix=AVAILABLE_BADGE_PREFIX, slug=slug(name))


def create_badge(image_data, name, rank, description):
    s3.Bucket(BUCKET_NAME).put_object(
        Key=make_key(name),
        Body=image_data,
        Metadata={
            RANK_META: rank,
            AWARD_FOR_META: description,
            NAME_META: name
        }
    )


def main(args=None):
    parser = argparse.ArgumentParser(description='Create a new badge')

    parser.add_argument('image', type=argparse.FileType('rb'),
                        help='path to the 512 by 512 PNG that is the visual part of the badge')

    parser.add_argument('name',
                        help='The badge name')

    parser.add_argument('rank', choices=['bronze', 'silver', 'gold'],
                        help='The badge rank/value')

    parser.add_argument('description',
                        help='Why people are awarded the badge')

    args = parser.parse_args(args)
    create_badge(args.image.read(), args.name, args.rank, args.description)


if __name__ == "__main__":
    main()
