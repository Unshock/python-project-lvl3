import logging
import re
import requests
import os
import pathlib
from urllib.parse import urlparse
from bs4 import BeautifulSoup


def make_name(url_, type='html'):
    result = re.sub(r"^(https?:\/\/)|(\.html)$|[\W_]", '-', url_).strip('-')
    result += '.html' if type == 'html' else '_files'
    return result


def make_html_name(url_):
    netloc_with_path = get_netloc(url_) + get_path(url_)
    result = re.sub(r"(\.html)$|[\W_]", '-',
                    netloc_with_path).strip('-') + '.html'
    return result


def make_dir_name(url_):
    netloc_with_path = get_netloc(url_) + get_path(url_)
    result = re.sub(r"[\W_]", '-', netloc_with_path).strip('-') + '_files'
    return result


def get_extension(file_path: str) -> str:
    _, extension = os.path.splitext(file_path)
    return extension.lower()


def create_files_dir(page_url, download_folder):
    dir_name = make_dir_name(page_url)
    dir_path = os.path.join(download_folder, dir_name)
    try:
        os.mkdir(dir_path)
    except FileExistsError:
        error_message = f'directory \'{dir_path}\' already exists.' \
                        f' Can\'t be created. Exit.\n'
        logging.error(error_message)
        raise SystemExit(error_message)
    return dir_name, dir_path


def make_file_name(page_url, sub_page):
    file_url = page_url.strip('/') + sub_page
    print('fileurl', file_url)
    if get_netloc(sub_page) == '':
        file_path = get_netloc(file_url) + get_path(file_url)
    else:
        file_path = get_netloc(sub_page) + get_path(sub_page)
    print('filepath', file_path)
    file_extension = get_extension(file_path)
    result = re.sub(r"(\.\w*)$|[\W_]", '-', file_path).strip('-')
    result += file_extension if file_extension != '' else '.html'
    return result


def make_file_name2(download_link):
    # file_url = page_url.strip('/') + sub_page
    # if get_netloc(sub_page) == '':
    #     file_path = get_netloc(file_url) + get_path(file_url)
    # else:
    #     file_path = get_netloc(sub_page) + get_path(sub_page)
    file_path = get_netloc(download_link) + get_path(download_link)
    file_extension = get_extension(file_path)
    result = re.sub(r"(\.\w*)$|[\W_]", '-', file_path).strip('-')
    result += file_extension if file_extension != '' else '.html'
    return result


def get_url_response(url_):
    response = requests.get(url_)
    return response.text


def get_netloc(page_url):
    return urlparse(page_url).netloc


def get_path(page_url):
    return urlparse(page_url).path


def write_in_file(file_path, content):
    try:
        with open(file_path, 'wb') as new_file:
            new_file.write(content)
    except PermissionError:
        error_message = f'Access to \'{file_path}\' is denied. Exit.\n'
        logging.error(error_message)
        raise SystemExit(error_message)
    return new_file.name


def download(url_, download_folder='cwd'):  # noqa: C901
    if download_folder == 'cwd':
        download_folder = os.getcwd()
    file_name = make_html_name(url_)

    try:
        response = requests.get(url_)
        response.raise_for_status()
    except requests.exceptions.ConnectionError:
        error_message = f'Connection to {url_} failed. Exit.\n'
        logging.error(error_message)
        raise SystemExit(error_message)
    except requests.exceptions.HTTPError as trouble:
        response = trouble.response
        status_code = response.status_code
        error_message = f'Request has failed with status code={status_code}.' \
                        f' Exit.\n'
        logging.error(error_message)
        raise SystemExit(error_message)

    beautiful_response = BeautifulSoup(response.text, 'html.parser')
    file_path = pathlib.Path(download_folder, file_name)

    try:
        file_path.touch(exist_ok=False)
    except FileExistsError:
        error_message = f'File \'{file_path}\' already exists. Exit.\n'
        logging.error(error_message)
        raise SystemExit(error_message)

    try:
        with open(file_path, 'w') as new_file:
            try:
                new_file.write(beautiful_response.prettify())
            except PermissionError:
                error_message = f'Access to \'{file_path}\' is denied. Exit.\n'
                logging.error(error_message)
                raise SystemExit(error_message)
    except FileNotFoundError:
        error_message = f'Directory {download_folder} is not found. Exit.\n'
        logging.error(error_message)
        raise SystemExit(error_message)

    return new_file.name, download_folder


def make_file_link(page_url, sub_page):
    scheme = urlparse(page_url).scheme
    page_netloc = get_netloc(page_url)
    sub_page_netloc = get_netloc(sub_page)
    path = urlparse(sub_page).path

    if page_netloc == sub_page_netloc:
        return f'{scheme}://{sub_page_netloc}{path}'
    return f'{scheme}://{page_netloc}{path}'


def make_file_link2(page_url, sub_page):
    scheme = urlparse(page_url).scheme
    page_netloc = get_netloc(page_url)
    sub_page_netloc = get_netloc(sub_page)
    page_path = urlparse(page_url).path
    sub_page_path = urlparse(sub_page).path

    if page_netloc == sub_page_netloc:
        return f'{scheme}://{sub_page_netloc}{sub_page_path}'
    if sub_page[0] == '/':
        return f'{scheme}://{page_netloc}{sub_page_path}'
    if sub_page[0] != '/':
        return f'{scheme}://{page_netloc}{page_path}{sub_page}'
    raise ValueError('ERROR')


def download_file(page_url, sub_page, dir_path):
    file_name = make_file_name(page_url, sub_page)
    file_link = make_file_link(page_url, sub_page)

    logging.info(f'trying to download file: \'{file_link}\''
                 f' with name \'{file_name}\'')

    try:
        response = requests.get(file_link)
        response.raise_for_status()
    except (requests.exceptions.HTTPError,
            requests.exceptions.ConnectionError) as trouble:
        response = trouble.response
        status_code = response.status_code
        logging.error(f'file \'{file_link}\''
                      f' can\'t be downloaded, status code: '
                      f'{status_code}. Returns None.')
        return None

    file_path = pathlib.Path(dir_path, file_name)

    try:
        with open(file_path, 'wb') as new_file:
            new_file.write(response.content)
    except PermissionError:
        error_message = f'Access to \'{file_path}\' is denied. Exit.\n'
        logging.error(error_message)
        raise SystemExit(error_message)

    logging.info(f'file \'{file_name}\' downloaded in \'{dir_path}\'')
    return new_file.name


def download_file_alt(file_link, file_name, dir_path):

    logging.info(f'trying to download file: \'{file_link}\''
                 f' with name \'{file_name}\'')

    try:
        response = requests.get(file_link)
        response.raise_for_status()
    except (requests.exceptions.HTTPError,
            requests.exceptions.ConnectionError) as trouble:
        response = trouble.response
        status_code = response.status_code
        logging.error(f'file \'{file_link}\''
                      f' can\'t be downloaded, status code: '
                      f'{status_code}. Returns None.')
        return None

    file_path = pathlib.Path(dir_path, file_name)

    try:
        with open(file_path, 'wb') as new_file:
            new_file.write(response.content)
    except PermissionError:
        error_message = f'Access to \'{file_path}\' is denied. Exit.\n'
        logging.error(error_message)
        raise SystemExit(error_message)

    logging.info(f'file \'{file_name}\' downloaded in \'{dir_path}\'')
    return new_file.name


def has_files(page_url, html):
    tags = ['img', 'link', 'script']
    result = []
    for tag in tags:
        check_result = return_files_or_none(page_url, html, tag)
        if check_result is not None:
            result.extend(check_result)
    return result if len(result) > 0 else None


def return_files_or_none(page_url, html, tag):
    attributes_dict = {
        'link': 'href',
        'img': 'src',
        'script': 'src'
    }
    soup = BeautifulSoup(html, features='html.parser')
    result = []
    for link_tag in soup.find_all(tag):
        link = link_tag.get(attributes_dict[tag])
        if link is None:
            continue
        if is_valid_file_path(page_url, link):
            result.append(link)
    return result if len(result) > 0 else None


def is_valid_file_path(page_url, file_path):
    if get_netloc(page_url) == get_netloc(file_path):
        return True
    if not get_netloc(file_path):
        if str(get_path(file_path)).startswith('/'):
            return True
        else:
            logging.warning(
                f'file {file_path} is not valid and won\'t be downloaded')
            return False
    return False


def is_valid_file_path2(page_url, link):
    if get_netloc(link) != '':
        return False if get_netloc(page_url) != get_netloc(link) else True
    return False if link == '' else True


def has_files2(html):
    tags_and_attributes = {
        'link': 'href',
        'img': 'src',
        'script': 'src'
    }
    soup = BeautifulSoup(html, features='html.parser')
    result = []
    for tag in tags_and_attributes.keys():
        for attribute_value in soup.find_all(tag):
            if attribute_value:
                pass
    return result if len(result) > 0 else None


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
            if link is None or not is_valid_file_path2(page_url, link):
                continue
            download_link = make_file_link2(page_url, link)
            file_name = make_file_name2(download_link)
            result.append(
                {
                    'attribute_value': link,
                    'name': file_name,
                    'link': download_link
                }
            )
    print(result)
    return result if len(result) > 0 else None


# def return_links_or_none(page_url, html):
#     soup = BeautifulSoup(html, features='html.parser')
#     result = []
#     for link_tag in soup.find_all('link'):
#         link = link_tag.get('href')
#         if is_valid_file_path(page_url, link) is True:
#             result.append(link)
#     return result if len(result) > 0 else None
#
#
# def return_pics_or_none(page_url, html):
#     soup = BeautifulSoup(html, features='html.parser')
#     result = []
#     for img_tag in soup.find_all('img'):
#         pic = img_tag.get('src')
#         if is_valid_file_path(page_url, pic) is True:
#             result.append(pic)
#     return result if len(result) > 0 else None
#
#
# def return_scripts_or_none(page_url, html):
#     soup = BeautifulSoup(html, features='html.parser')
#     result = []
#     for script_tag in soup.find_all('script'):
#         script = script_tag.get('src')
#         #print(script)
#         if is_valid_file_path(page_url, script) is True:
#             result.append(script)
#     return result if len(result) > 0 else None


# def is_link_of_path(string: str):
#    return 'Link' if 'http'.startswith(string) else 'Path'


def substitution(html_path, sub_page_to_replace, full_file_name):
    with open(html_path, 'r') as html:
        x = html.read()
    with open(html_path, 'w') as html:
        x = x.replace(f'"{sub_page_to_replace}"', f'"{full_file_name}"')
        html.write(x)
    logging.info(f'name {sub_page_to_replace} replaced with {full_file_name}')


# t = download('https://en.wikipedia.org/wiki/Finland_me
# n%27s_national_ice_hockey_team')[0]
# h = has_pics(open(t).read())
# substitution(h, t)
