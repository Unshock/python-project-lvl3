#!/usr/bin/env python
from page_loader import cli
from page_loader.loader_engine import loader_engine


def main():
    args = cli.parse_args()
    print(loader_engine(args.url, args.output))


if __name__ == '__main__':
    main()
