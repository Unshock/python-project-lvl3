import os
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
from page_loader import url


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


def prepare_assets(page_url: str, page_html) -> tuple:
    """
    :param page_url: the url of the original page needed to be downloaded
    :param page_html: data of the downloaded html file
    :return: handles HTML data and returns list of local files found in the HTML
        and HTML data processed with BeautifulSoup

        To create the list of local files func checks for all considered tags
        in downloaded html ('img', 'link', 'script') and their attributes that
        can have file paths. Return the list of the dictionaries for the found
        local assets. That dictionary has original attribute url and file
        name.
    """

    ATTRIBUTE_MAPPING = {
        'script': 'src',
        'link': 'href',
        'img': 'src'
    }

    asset_dir_name = url.make_dir_name(page_url)

    page_html = BeautifulSoup(page_html, 'html.parser')
    tags = [*page_html('script'),
            *page_html('link'),
            *page_html('img')]

    assets = []

    for tag in tags:
        attribute_name = ATTRIBUTE_MAPPING[tag.name]

        attribute_value = tag.get(attribute_name)

        if not is_valid_file_path(page_url, attribute_value):
            continue

        download_link = urljoin(page_url, attribute_value)
        file_name = url.make_file_name(download_link)

        tag[attribute_name] = os.path.join(asset_dir_name, file_name)

        assets.append({
            'name': file_name,
            'url': download_link,
        })

    return page_html.prettify(), assets
