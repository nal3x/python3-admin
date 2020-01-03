import argparse

def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('path', help='path to json' )
    parser.add_argument('--export', action='store_true', help='exports')
    return parser
