import logging
import os
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
from page_loader import naming


def handle_html(page_url: str, html: str):
    """
    :param page_url: the url of the original page needed to be downloaded
    :param html: data of the downloaded html file
    :return: handles HTML data and returns processed with BeautifulSoup HTML
        data. Aslo returns list_of_local files found in the HTML or None if no
        local files were found
    """
    beautiful_html = BeautifulSoup(html, 'html.parser')
    processed_html = beautiful_html.prettify()
    list_of_local_files = make_list_of_files(page_url, processed_html)

    logging.info('HTML file has been successfully handled')

    if list_of_local_files:
        processed_html = substitute(processed_html, list_of_local_files)

        logging.info('Handler has found and returned list of local files')
        return list_of_local_files, processed_html
    logging.warning('Handler hasn\'t found any local files '
                    'and returned \'None\'')
    return None, processed_html


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


def make_list_of_files(page_url: str, html) -> list or None:
    """
    :param page_url: the url of the original page needed to be downloaded
    :param html: data of the downloaded html file
    :return: checks for all considered tags in downloaded html ('img', 'link',
        'script') and their attributes that can have file paths. Return the list
        of the dictionaries for the found local file paths or None if there is
        no local files. That dictionary has original attribute value, web-link,
        file name, path file should be saved to.
    """
    beautiful_html = BeautifulSoup(html, 'html.parser')
    tags = [*beautiful_html('script'),
            *beautiful_html('link'),
            *beautiful_html('img')]

    result = []
    dir_name = naming.make_dir_name(page_url)
    for tag in tags:
        attribute_value = tag.get('href') or tag.get('src')

        if not is_valid_file_path(page_url, attribute_value):
            continue

        download_link = urljoin(page_url, attribute_value)
        file_name = naming.make_file_name(download_link)

        local_file_path = os.path.join(dir_name, file_name)

        result.append({
            'attribute_value': attribute_value,
            'name': file_name,
            'url': download_link,
            'file_path': local_file_path
        })

    return result if len(result) > 0 else None


def create_local_files_dir(page_url: str, download_folder: str) -> tuple:
    """
    :param page_url: the url of the original page needed to be downloaded
    :param download_folder: path where HTML file should be downloaded
    :return: created directory for local files and returns a tuple of the name
        of that directory and absolute path to the directory
    """
    dir_name = naming.make_dir_name(page_url)
    dir_path = os.path.join(download_folder, dir_name)
    try:
        os.mkdir(dir_path)
    except FileExistsError:
        error_message = f'Directory \'{dir_path}\' already exists.' \
                        f' Can\'t be created. Exit.\n'
        raise FileExistsError(error_message)

    return dir_name, dir_path


def substitute(html: str, list_of_local_files: list):
    """
    :param html: data of the downloaded html file
    :param list_of_local_files: the list of the dictionaries for
        the found local file paths in HTML
    :return: returns new HTML data where attribute values for local files
        replaced with local files' paths
    """
    for local_url in list_of_local_files:
        attribute_value = local_url['attribute_value']
        local_file_path = local_url['file_path']
        html = html.replace(f'"{attribute_value}"', f'"{local_file_path}"')

        logging.info(f'Name {attribute_value} replaced with {local_file_path}')
    return html
