import logging
import requests
import os
import pathlib
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
from page_loader.exception import CustomConnectionError
from page_loader import processing


def create_local_files_dir(page_url: str, download_folder: str) -> tuple:
    """
    :param page_url: the url of the original page needed to be downloaded
    :param download_folder: path where HTML file should be downloaded
    :return: created directory for local files and returns a tuple of the name
        of that directory and absolute path to the directory
    """
    dir_name = processing.make_dir_name(page_url)
    dir_path = os.path.join(download_folder, dir_name)
    try:
        os.mkdir(dir_path)
    except FileExistsError:
        error_message = f'Directory \'{dir_path}\' already exists.' \
                        f' Can\'t be created. Exit.\n'
        raise FileExistsError(error_message)

    return dir_name, dir_path


def download_html(page_url: str, download_folder: str) -> str:  # noqa: C901
    """
    :param page_url: the url of the original page needed to be downloaded
    :param download_folder: path where HTML file should be downloaded
    :return: downloads the HTML page of the specified page URL and saves it to
        file with special_name.html in the specified folder. Returns the
        absolute path to the downloaded HTML file.
    """
    html_file_name = processing.make_html_name(page_url)

    try:
        response = requests.get(page_url, timeout=20)
        response.raise_for_status()
    except (requests.exceptions.ConnectionError,
            requests.exceptions.ReadTimeout):
        error_message = f'Connection to {page_url} failed. Exit.\n'
        raise CustomConnectionError(error_message)
    except requests.exceptions.HTTPError as trouble:
        response = trouble.response
        status_code = response.status_code
        error_message = f'Request has failed with status code={status_code}.' \
                        f' Exit.\n'
        raise CustomConnectionError(error_message)

    beautiful_response = BeautifulSoup(response.text, 'html.parser')
    file_path = pathlib.Path(download_folder, html_file_name)

    try:
        file_path.touch(exist_ok=False)
    except FileExistsError:
        error_message = f'File \'{file_path}\' already exists. Exit.\n'
        raise FileExistsError(error_message)
    except PermissionError:
        error_message = f'You don\'t have access to the directory' \
                        f' \'{download_folder}\'. Exit.\n'
        raise PermissionError(error_message)

    with open(file_path, 'w') as new_file:
        new_file.write(beautiful_response.prettify())

    return os.path.abspath(new_file.name)


def download_file(file_link: str, file_name: str, dir_path: str):
    """
    :param file_link: web link to the file that should be downloaded
    :param file_name: the name of the file that should be used for saved file
    :param dir_path: path where file should be downloaded (directory with
        local files)
    :return: downloads file from the given URL, saves it with given name in the
        directory where local files should be in. Returns the relative path to
        the downloaded file from the HTML file. If response can't be got -
        returns None.
    """

    logging.info(f'Trying to download file: \'{file_link}\''
                 f' with name \'{file_name}\'')

    try:
        response = requests.get(file_link, timeout=20)
        response.raise_for_status()
    except (requests.exceptions.HTTPError,
            requests.exceptions.ConnectionError,
            requests.exceptions.ReadTimeout) as trouble:
        response = trouble.response
        status_code = response.status_code
        logging.warning(f'File \'{file_link}\''
                        f' can\'t be downloaded, status code: '
                        f'{status_code}. Skipped.\n')
        return None

    file_path = pathlib.Path(dir_path, file_name)

    with open(file_path, 'wb') as new_file:
        new_file.write(response.content)

    logging.info(f'File \'{file_name}\' downloaded in \'{dir_path}\'')
    return new_file.name


def is_valid_file_path(page_url: str, attribute_value: str) -> bool:
    """
    :param page_url: the url of the original page needed to be downloaded
    :param attribute_value: value of the attribute that can have file path
        (link) in one of considered tags ('img', 'link', 'script')
    :return: True if attribute value is not None and file link is local -
        domain and subdomain should be similar in page_url and attribute_value
    """
    page_url_netloc = urlparse(page_url).netloc
    attribute_value_netloc = urlparse(attribute_value).netloc

    if attribute_value_netloc:
        return page_url_netloc == attribute_value_netloc
    return True if attribute_value else False


def make_list_of_files(page_url: str, html: str) -> list or None:
    """
    :param page_url: the url of the original page needed to be downloaded
    :param html: data of the downloaded html file
    :return: checks for all considered tags in downloaded html ('img', 'link',
        'script') and their attributes that can have file paths. Return the list
        of the dictionaries for the found local file paths or None if there is
        no local files. That dictionary has original attribute value, web-link,
        and file name.
    """

    soup = BeautifulSoup(html, features='html.parser')
    tags = [*soup('script'), *soup('link'), *soup('img')]
    result = []

    for tag in tags:
        attribute_value = tag.get('href') or tag.get('src')

        if not is_valid_file_path(page_url, attribute_value):
            continue

        download_link = urljoin(page_url, attribute_value)
        file_name = processing.make_file_name(download_link)
        result.append({
            'attribute_value': attribute_value,
            'name': file_name,
            'link': download_link
        })

    return result if len(result) > 0 else None
