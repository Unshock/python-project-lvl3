import logging
import requests
from page_loader.exception import CustomConnectionError


def download_file(url: str, main_html=False):
    """
    :param url: the url main page or file needed to be downloaded
    :param main_html: flag showing if file is main HTML we need to download
    :return: downloads and returns data of file. If main page, reacts to
        connection errors more strictly and closes the program.
    """

    logging.info(f'Start to download {url}')

    try:
        url_response = requests.get(url, timeout=20)
        url_response.raise_for_status()
        logging.info(f'File on the {url} was successfully downloaded')
        return url_response

    except (requests.exceptions.ConnectionError,
            requests.exceptions.ReadTimeout):

        if main_html:
            error_message = f'Connection to {url} failed. Exit.\n'
            raise CustomConnectionError(error_message)

        error_message = f'Connection to {url} failed. File is skipped.\n'
        logging.warning(error_message)
        return

    except requests.exceptions.HTTPError as trouble:
        response = trouble.response
        status_code = response.status_code
        if main_html:
            error_message = f'Request has failed with status code=' \
                            f'{status_code}. Exit.\n'
            raise CustomConnectionError(error_message)

        error_message = f'File \'{url}\' can\'t be downloaded, status code: ' \
                        f'{status_code}. Skipped.\n'
        logging.warning(error_message)
        return
