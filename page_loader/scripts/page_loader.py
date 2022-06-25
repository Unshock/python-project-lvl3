#!/usr/bin/env python
import sys
from page_loader import cli
from page_loader.loader_engine import loader_engine
import logging
from page_loader.downloader import MyException


def main():
    logging.basicConfig(level=logging.WARNING,
                        format='%(asctime)s %(levelname)s: %(message)s',
                        datefmt='%d/%m/%Y %I:%M:%S')
    args = cli.parse_args()
    try:
        print(loader_engine(args.url, args.output))
    except MyException():
        sys.exit(1)

if __name__ == '__main__':
    main()
