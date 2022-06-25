#!/usr/bin/env python
from page_loader import cli
from page_loader.loader_engine import loader_engine
import logging


def main():
    logging.basicConfig(level=logging.WARNING,
                        format='%(asctime)s %(levelname)s: %(message)s',
                        datefmt='%d/%m/%Y %I:%M:%S')
    args = cli.parse_args()
    print(loader_engine(args.url, args.output))


if __name__ == '__main__':
    main()
