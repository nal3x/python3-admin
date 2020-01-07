import argparse
from hr import users, inventory

def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('path',
            help='path to import or export json user data' )
    parser.add_argument('--export', action='store_true',
            help='exports the users of a system to json format')
    return parser

def main():

    args = create_parser().parse_args()
    if args.export:
        inventory.dump(args.path) #TODO: extend to specify which users
    else:
        user_dicts = inventory.parse(args.path)
        users.sync_system(user_dicts)
