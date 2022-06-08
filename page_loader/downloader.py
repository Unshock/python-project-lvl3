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
    os.mkdir(dir_path)
    return dir_name, dir_path


def make_file_name(page_url, sub_page):
    file_url = page_url.strip('/') + sub_page
    if get_netloc(sub_page) == '':
        file_path = get_netloc(file_url) + get_path(file_url)
    else:
        file_path = get_netloc(sub_page) + get_path(sub_page)
    file_extension = get_extension(file_path)
    #  print('url', page_url, 'sub', sub_page)
    #  print(re.findall(r"(\.\w+)$", sub_page))
    #  extension = re.findall(r"(\.\w+)$", sub_page)
    #  extension = re.findall(r"(\.\w+)$", sub_page)[0]
    #  if len(extension) == 0:
    #    new_url = page_url + sub_page
    #    print('new_url', new_url)
    #    result = make_name(new_url)
    #    print('res', result)
    #    return result
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


def download(url_, download_folder='cwd'):
    if download_folder == 'cwd':
        download_folder = os.getcwd()
    file_name = make_html_name(url_)
    response = requests.get(url_)
    beautiful_response = BeautifulSoup(response.text, 'html.parser')
    file_path = pathlib.Path(download_folder, file_name)
    with open(file_path, 'w') as new_file:
        new_file.write(beautiful_response.prettify())
    return new_file.name, download_folder


def make_file_link(scheme, netloc, path):
    return f'{scheme}://{netloc}{path}'


def download_file(page_url, sub_page, dir_path):
    file_name = make_file_name(page_url, sub_page)
    scheme = urlparse(page_url).scheme
    page_netloc = get_netloc(page_url)
    sub_page_netloc = get_netloc(sub_page)
    path = urlparse(sub_page).path

    if page_netloc == sub_page_netloc:
        file_link = make_file_link(scheme, sub_page_netloc, path)
    else:
        file_link = make_file_link(scheme, page_netloc, path)

    logging.info(f'trying to download file: {file_link} with name {file_name}')
    try:
        response = requests.get(file_link)
    except Exception:
        logging.error(f'file {file_link}'
                      f' can\'t be downloaded, return None!')
        return None
    file_path = pathlib.Path(dir_path, file_name)
    with open(file_path, 'wb') as new_file:
        new_file.write(response.content)
    logging.info(f'file {file_name} downloaded in {dir_path}')
    return new_file.name


def has_files(page_url, html):
    tags = ['img', 'link', 'script']
    result = []
    for tag in tags:
        check_result = return_files_or_none(page_url, html, tag)
        if check_result is not None:
            result.extend(check_result)
    return result if len(result) > 0 else None


def is_valid_file_path(page_url, file_path):
    if get_netloc(page_url) == get_netloc(file_path):
        return True
    if not get_netloc(file_path):
        # print(file_path)
        # print(get_path(file_path))
        if str(get_path(file_path)).startswith('/'):
            return True
        else:
            logging.warning(
                f'file {file_path} is not valid and won\'t be downloaded')
            return False
    return False


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
        if is_valid_file_path(page_url, link) is True:
            result.append(link)
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


def is_link_of_path(string: str):
    return 'Link' if 'http'.startswith(string) else 'Path'


def substitution(html_path, sub_page_to_replace, full_file_name):
    # print('LINKI', links)
    with open(html_path, 'r') as html:
        x = html.read()
    with open(html_path, 'w') as html:
        x = x.replace(sub_page_to_replace, full_file_name)
        html.write(x)
    logging.info(f'name {sub_page_to_replace} replaced with {full_file_name}')


# t = download('https://en.wikipedia.org/wiki/Finland_me
# n%27s_national_ice_hockey_team')[0]
# h = has_pics(open(t).read())
# substitution(h, t)
