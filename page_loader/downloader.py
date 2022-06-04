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


def download_file(page_url, sub_page, dir_path):
    file_name = make_file_name(page_url, sub_page)
    try:
        response = requests.get(page_url.strip('/') + sub_page)
    except Exception:
        return None
    file_path = pathlib.Path(dir_path, file_name)
    with open(file_path, 'wb') as new_file:
        new_file.write(response.content)
    return new_file.name


def has_files(page_url, html):
    list_of_checks = [
        return_pics_or_none,
        return_links_or_none,
        return_scripts_or_none,
    ]
    result = []
    for check in list_of_checks:
        check_result = check(page_url, html)
        if check_result is not None:
            result.extend(check_result)
    return result if len(result) > 0 else None


def is_valid_file_path(page_url, file_path):
    if get_netloc(page_url) == get_netloc(file_path):
        return True
    if not get_netloc(file_path):
        return True if get_path(file_path) else False
    return False


def return_links_or_none(page_url, html):
    soup = BeautifulSoup(html, features='html.parser')
    result = []
    for link_tag in soup.find_all('link'):
        link = link_tag['href']
        if is_valid_file_path(page_url, link):
            result.append(link)
    return result if len(result) > 0 else None


def return_pics_or_none(page_url, html):
    soup = BeautifulSoup(html, features='html.parser')
    result = []
    for img_tag in soup.find_all('img'):
        pic = img_tag['src']
        if is_valid_file_path(page_url, pic):
            result.append(pic)
    return result if len(result) > 0 else None


def return_scripts_or_none(page_url, html):
    soup = BeautifulSoup(html, features='html.parser')
    result = []
    for script_tag in soup.find_all('script'):
        script = script_tag.get('src')
        print(script)
        if script and is_valid_file_path(page_url, script):
            print(is_valid_file_path(page_url, script))
            result.append(script)
    return result if len(result) > 0 else None


def is_link_of_path(string: str):
    return 'Link' if 'http'.startswith(string) else 'Path'


def substitution(html_path, sub_page_to_replace, full_file_name):
    # print('LINKI', links)
    with open(html_path, 'r') as html:
        x = html.read()
    with open(html_path, 'w') as html:
        x = x.replace(sub_page_to_replace, full_file_name)
        html.write(x)


# t = download('https://en.wikipedia.org/wiki/Finland_me
# n%27s_national_ice_hockey_team')[0]
# h = has_pics(open(t).read())
# substitution(h, t)
