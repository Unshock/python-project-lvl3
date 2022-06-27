#!/usr/bin/env python
import sys
from page_loader.cli import parse_args, FatalError

import logging
import page_loader.loader_engine as le


def main():
    logging.basicConfig(level=logging.WARNING,
                        format='%(asctime)s %(levelname)s: %(message)s',
                        datefmt='%d/%m/%Y %I:%M:%S')
    args = parse_args()
    try:
        print(le.loader_engine(args.url, args.output))
    except FatalError as e:
        logging.error(e)
        sys.exit(1)
    sys.exit(0)


if __name__ == '__main__':
    main()
