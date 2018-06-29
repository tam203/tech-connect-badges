from tc_badges.utils import key_to_url, get_users_badge_keys, get_id
import argparse


def main(args=None):
    parser = argparse.ArgumentParser(description='List a users badges')

    parser.add_argument('user',
                        help='The email address of the person to award this too')

    args = parser.parse_args(args)

    for i, key in enumerate(get_users_badge_keys(get_id(args.user))):
        print("%3d %-25s %s" % (i, key.split('/')[-1][:-4], key_to_url(key)))


if __name__ == "__main__":
    main()
