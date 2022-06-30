from page_loader import downloader
from page_loader import custom_exception
from urllib.parse import urlparse, urljoin
import re
import os
import pathlib


def make_html_name(url_):
    netloc_with_path = downloader.get_netloc(url_) + downloader.get_path(url_)
    html_file_name = re.sub(r"(\.html)$|[\W_]", '-',
                            netloc_with_path).strip('-') + '.html'
    return html_file_name


def make_dir_name(url_):
    netloc_with_path = downloader.get_netloc(url_) + downloader.get_path(url_)
    local_files_dir_name = re.sub(r"[\W_]",
                                  '-', netloc_with_path).strip('-') + '_files'
    return local_files_dir_name


def normalize_download_folder(download_folder):
    if download_folder == 'cwd':
        download_folder = os.getcwd()
    path = pathlib.Path(download_folder)
    if not path.exists():
        error_message = f'The folder with name \"{download_folder}\"'\
                        f' does not exists. Exit.\n'
        raise custom_exception.FatalError(error_message)
    return download_folder


def get_extension(file_path: str) -> str:
    _, extension = os.path.splitext(file_path)
    return extension.lower()


def make_file_name(download_link):
    file_path = urlparse(download_link).netloc + urlparse(download_link).path
    file_extension = get_extension(file_path)
    file_name = re.sub(r"(\.\w*)$|[\W_]", '-', file_path).strip('-')
    file_name += file_extension if file_extension != '' else '.html'
    return file_name


def make_file_link(page_url, sub_page):
    if urlparse(page_url).netloc == urlparse(sub_page).netloc:
        return sub_page
    return urljoin(page_url, sub_page)
