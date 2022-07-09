#!/usr/bin/env python
import sys
from page_loader.cli import parse_args
from page_loader.custom_exception import CustomFileExistsError
from page_loader.custom_exception import CustomConnectionError
import logging
import page_loader.page_loader_engine as engine


def main():
    logging.basicConfig(level=logging.WARNING,
                        format='%(asctime)s %(levelname)s: %(message)s',
                        datefmt='%d/%m/%Y %I:%M:%S')

    args = parse_args()
    try:
        path = engine.download(args.url, args.output)
    except (CustomFileExistsError,
            CustomConnectionError) as error:
        logging.error(error)
        sys.exit(1)
    except Exception as error:
        logging.error(error)
        sys.exit(1)
    print(f'HTML has been downloaded as {path}')
    sys.exit(0)


if __name__ == '__main__':
    main()
