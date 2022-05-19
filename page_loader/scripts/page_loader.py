#!/usr/bin/env python
from page_loader import cli
from page_loader.downloader import generator


def main():
    args = cli.parse_args()
    print(generator(args.url, args.output))


if __name__ == '__main__':
    main()
