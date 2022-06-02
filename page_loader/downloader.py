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
    result = re.sub(r"(\.html)$|[\W_]", '-', netloc_with_path).strip('-') + '.html'
    return result


def make_dir_name(url_):
    netloc_with_path = get_netloc(url_) + get_path(url_)
    result = re.sub(r"[\W_]", '-', netloc_with_path).strip('-') + '_files'
    return result


def get_extension(file_path: str) -> str:
    _, extension = os.path.splitext(file_path)
    return extension.lower()


def make_file_name(page_url, sub_page):
    page_netloc = get_netloc(page_url)
    file_path = page_netloc + sub_page
    file_extension = get_extension(file_path)
    #print('url', page_url, 'sub', sub_page)
    #print(re.findall(r"(\.\w+)$", sub_page))
    #extension = re.findall(r"(\.\w+)$", sub_page)
    #extension = re.findall(r"(\.\w+)$", sub_page)[0]
    #if len(extension) == 0:
    #    new_url = page_url + sub_page
    #    print('new_url', new_url)
    #    result = make_name(new_url)
    #    print('res', result)
    #    return result
    result = re.sub(r"(\.\w*)$|[\W_]", '-', file_path).strip('-')
    result += file_extension if file_extension != '' else '.html'
    print(result)
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
    response = requests.get(page_url + sub_page)
    file_path = pathlib.Path(dir_path, file_name)
    with open(file_path, 'wb') as new_file:
        new_file.write(response.content)
    return new_file.name


def has_files(html):
    list_of_checks = [
        return_pics_or_none,
        return_links_or_none,
    ]
    result = []
    for check in list_of_checks:
        check_result = check(html)
        if check_result is not None:
            result.extend(check_result)
    return result if len(result) > 0 else None


def has_pics(html):
    result = re.findall(r"(?<=img[\W\w]src=\")\S*(?=\")", html)
    return result if len(result) > 0 else None


def return_links_or_none(html):
    soup = BeautifulSoup(html, features='html.parser')
    result = []
    #print(soup.find_all('img'))
    for link_tag in soup.find_all('link'):
        link = link_tag['href']
        if re.search(r"^\/\w+", link):
        #if not re.search(r"^(https?:)?\/\/", link) and link != '':
            result.append(link)
    #print(result)
    return result if len(result) > 0 else None


def return_pics_or_none(html):
    soup = BeautifulSoup(html, features='html.parser')
    result = []
    print(soup.find_all('img'))
    for img_tag in soup.find_all('img'):
        pic = img_tag['src']
        if re.search(r"^\/\w+", pic):
        #if not re.search(r"^(https?:)?\/\/", pic) and pic != '':
            result.append(pic)
    print(result)
    return result if len(result) > 0 else None


def is_link_of_path(string: str):
    return 'Link' if 'http'.startswith(string) else 'Path'


def substitution(links, html_path, dir_name, page_url):
    print('LINKI', links)
    with open(html_path, 'r') as html:
        x = html.read()
    with open(html_path, 'w') as html:
        for link in links:
            x = x.replace(link, os.path.join(dir_name, make_file_name(page_url, link)))
        html.write(x)


# t = download('https://en.wikipedia.org/wiki/Finland_me
# n%27s_national_ice_hockey_team')[0]
# h = has_pics(open(t).read())
# substitution(h, t)
