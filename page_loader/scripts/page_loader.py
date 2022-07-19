#!/usr/bin/env python
import sys
from page_loader.cli import parse_args
import logging
import page_loader.page_loader_engine as engine


def main():
    logging.basicConfig(level=logging.WARNING,
                        format='%(asctime)s %(levelname)s: %(message)s',
                        datefmt='%d/%m/%Y %I:%M:%S')

    args = parse_args()
    try:
        path = engine.download(args.url, args.output)
        print(f'HTML has been downloaded as {path}')
    except Exception as error:
        logging.error(error)
        sys.exit(1)


if __name__ == '__main__':
    main()
