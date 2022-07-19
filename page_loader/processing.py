from urllib.parse import urlparse
import re
import os
import pathlib


def make_html_name(page_url: str) -> str:
    """
    :param page_url: the url of the original page needed to be downloaded
    :return: formatted name for HTML file
    """
    netloc_with_path = urlparse(page_url).netloc + urlparse(page_url).path
    html_file_name = re.sub(r"(\.html)$|[\W_]", '-',
                            netloc_with_path).strip('-') + '.html'
    return html_file_name


def make_dir_name(page_url: str) -> str:
    """
    :param page_url: the url of the original page needed to be downloaded
    :return: formatted name for directory for local files
    """
    netloc_with_path = urlparse(page_url).netloc + urlparse(page_url).path
    local_files_dir_name = re.sub(r"[\W_]",
                                  '-', netloc_with_path).strip('-') + '_files'
    return local_files_dir_name


def normalize_download_folder(download_folder: str) -> str:
    """
    :param download_folder: path where HTML file should be downloaded
    :return: checks if path exists and return path where HTML file should be
        downloaded. Returns current working directory if not specified.
    """
    if download_folder == 'cwd':
        download_folder = os.getcwd()
    path = pathlib.Path(download_folder)
    if not path.exists():
        error_message = f'The folder with name \"{download_folder}\"'\
                        f' does not exists. Exit.\n'
        raise FileExistsError(error_message)
    return download_folder


def get_extension(file_path: str) -> str:
    """
    :param file_path: url netloc with path
    :return: file extension
    """
    _, extension = os.path.splitext(file_path)
    return extension.lower()


def make_file_name(download_link: str) -> str:
    """
    :param download_link: URL of the file
    :return: the name of file
    """
    file_path = urlparse(download_link).netloc + urlparse(download_link).path
    file_extension = get_extension(file_path)
    file_name = re.sub(r"(\.\w*)$|[\W_]", '-', file_path).strip('-')
    file_name += file_extension if file_extension != '' else '.html'
    return file_name
