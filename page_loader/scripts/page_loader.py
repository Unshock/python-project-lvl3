#!/usr/bin/env python
import sys
from page_loader.cli import parse_args
from page_loader.custom_exception import FatalError

import logging
import page_loader.page_loader_engine as le


def main():
    logging.basicConfig(level=logging.WARNING,
                        format='%(asctime)s %(levelname)s: %(message)s',
                        datefmt='%d/%m/%Y %I:%M:%S')
    args = parse_args()
    try:
        print(le.download(args.url, args.output))
    except FatalError as e:
        logging.error(e)
        sys.exit(1)
    sys.exit(0)


if __name__ == '__main__':
    main()
