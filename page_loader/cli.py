import argparse


def parse_args(*args):
    parser = argparse.ArgumentParser(description='Downloads page')
    parser.add_argument('url', metavar='url')
    parser.add_argument('--output', '-o', metavar='OUTPUT',
                        default='cwd', help='set output directory')
    return parser.parse_args(*args)
