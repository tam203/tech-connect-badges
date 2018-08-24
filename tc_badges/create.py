import argparse
from PIL import Image
from tc_badges.constants import RANK_META, AWARD_FOR_META, NAME_META, BUCKET_NAME, AVAILABLE_BADGE_PREFIX, RANKS
import io
from tc_badges.badges import PotentialBadge
from tc_badges import db


def create_badge(image_file, name, rank, description, points=None):

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

    badge = PotentialBadge(name, im_data.read(), rank, description, points)
    badge = db.create_badge(badge)


def check_points(rank_name, points):
    rank = RANKS[rank_name]
    if not (rank.min_points <= points <= rank.max_points):
        raise ValueError("The point value {points} is not valid for rank {rank}({min}-{max})".format(
            points=points,
            min=rank.min_points,
            max=rank.max_points,
            rank=rank.name
        ))


def parse_args(args=None):
    parser = argparse.ArgumentParser(description='Create a new badge')

    parser.add_argument('image',
                        help='path to the 512 by 512 PNG that is the visual part of the badge')

    parser.add_argument('name',
                        help='The badge name')

    parser.add_argument('rank', choices=RANKS.keys(),
                        help='The badge rank/value')

    parser.add_argument('description',
                        help='Why people are awarded the badge')

    parser.add_argument('--points',  type=int,
                        help='The number of TC points for the badge')

    args = parser.parse_args(args)

    check_points(args.rank, args.points)

    return args


def main(args=None):
    args = parse_args(args)
    create_badge(args.image, args.name, args.rank, args.description)


if __name__ == "__main__":
    main()
