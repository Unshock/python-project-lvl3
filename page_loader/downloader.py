import logging
import requests
import os
import pathlib
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from page_loader.custom_exception import FatalError
from page_loader import string_processing


def create_local_files_dir(page_url, download_folder):
    dir_name = string_processing.make_dir_name(page_url)
    dir_path = os.path.join(download_folder, dir_name)
    try:
        os.mkdir(dir_path)
    except FileExistsError:
        error_message = f'Directory \'{dir_path}\' already exists.' \
                        f' Can\'t be created. Exit.\n'
        raise FatalError(error_message)
    return dir_name, dir_path


def get_netloc(page_url):
    netloc = urlparse(page_url).netloc
    return netloc


def get_path(page_url):
    return urlparse(page_url).path


def download_html(url_, download_folder):  # noqa: C901
    print(url_, download_folder)
    file_name = string_processing.make_html_name(url_)

    try:
        response = requests.get(url_, timeout=20)
        response.raise_for_status()
    except (requests.exceptions.ConnectionError,
            requests.exceptions.ReadTimeout):
        error_message = f'Connection to {url_} failed. Exit.\n'
        raise FatalError(error_message)
    except requests.exceptions.HTTPError as trouble:
        response = trouble.response
        status_code = response.status_code
        error_message = f'Request has failed with status code={status_code}.' \
                        f' Exit.\n'
        raise FatalError(error_message)

    beautiful_response = BeautifulSoup(response.text, 'html.parser')
    file_path = pathlib.Path(download_folder, file_name)

    try:
        file_path.touch(exist_ok=False)
    except FileExistsError:
        error_message = f'File \'{file_path}\' already exists. Exit.\n'
        raise FatalError(error_message)

    try:
        with open(file_path, 'w') as new_file:
            try:
                new_file.write(beautiful_response.prettify())
            except PermissionError:
                error_message = f'Access to \'{file_path}\' is denied. Exit.\n'
                raise FatalError(error_message)
    except FileNotFoundError:
        error_message = f'Directory {download_folder} is not found. Exit.\n'
        raise FatalError(error_message)
    return os.path.abspath(new_file.name)


def download_file(file_link, file_name, dir_path):

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

    try:
        with open(file_path, 'wb') as new_file:
            new_file.write(response.content)
    except PermissionError:
        error_message = f'Access to \'{file_path}\' is denied. Exit.\n'
        raise FatalError(error_message)

    logging.info(f'File \'{file_name}\' downloaded in \'{dir_path}\'')
    return new_file.name


def is_valid_file_path(page_url, link):
    page_url_netloc = get_netloc(page_url)
    link_netloc = get_netloc(link)

    if link_netloc:
        return True if page_url_netloc == link_netloc else False
    return True if link else False


def make_list_of_files(page_url, html):
    tags_and_attributes = {
        'link': 'href',
        'img': 'src',
        'script': 'src'
    }
    soup = BeautifulSoup(html, features='html.parser')
    result = []
    for tag in tags_and_attributes.keys():
        for link_tag in soup.find_all(tag):
            link = link_tag.get(tags_and_attributes[tag])
            if link is None or not is_valid_file_path(page_url, link):
                continue
            download_link = string_processing.make_file_link(page_url, link)
            file_name = string_processing.make_file_name(download_link)
            result.append({
                'attribute_value': link,
                'name': file_name,
                'link': download_link
            })
    return result if len(result) > 0 else None
