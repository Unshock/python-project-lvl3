from urllib.parse import urlparse
import re
import os


def make_dir_name(page_url: str) -> str:
    """
    :param page_url: the url of the original page needed to be downloaded
    :return: formatted name for directory for local files
    """
    path = urlparse(page_url).path or '/'
    netloc_with_path = urlparse(page_url).netloc + path
    local_files_dir_name = re.sub(r"[\W_]", '-',
                                  netloc_with_path).strip('-') + '_files'
    return local_files_dir_name


def get_extension(file_path: str) -> str:
    """
    :param file_path: url netloc with path
    :return: file extension
    """
    _, extension = os.path.splitext(file_path)
    return extension.lower()


def make_file_name(download_url: str) -> str:
    """
    :param download_link: URL of the file
    :return: the name of file
    """
    path = urlparse(download_url).path or '/'
    file_path = urlparse(download_url).netloc + path
    file_extension = get_extension(file_path)
    file_name = re.sub(r"(\.\w*)$|[\W_]", '-', file_path).strip('-')
    file_name += file_extension if file_extension != '' else '.html'
    return file_name
