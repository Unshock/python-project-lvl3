import re
import requests
import os
import pathlib
from bs4 import BeautifulSoup


def make_name(url_, type='html'):
    result = re.sub(r"^(https?:\/\/)|(\.html)$|[\W_]", '-', url_).strip('-')
    result += '.html' if type == 'html' else '_files'
    return result


def make_dir_name(url_):
    result = re.sub(r"^(https?:\/\/)|(\.html)$|[\W_]", '-', url_).strip('-')
    result += '_files'
    return result


def make_file_name(url_):
    extension = re.findall(r"(\.\w+)$", url_)[0]
    result = re.sub(r"(\.\w*)$|[\W_]", '-', url_).strip('-')
    result += extension
    return result


def get_url_response(url_):
    response = requests.get(url_)
    return response.text


def download(url_, download_folder='cwd'):
    if download_folder == 'cwd':
        download_folder = os.getcwd()
    file_name = make_name(url_, type='html')
    response = requests.get(url_)
    beautiful_response = BeautifulSoup(response.text, 'html.parser')
    file_path = pathlib.Path(download_folder, file_name)
    with open(file_path, 'w') as new_file:
        new_file.write(beautiful_response.prettify())
    return new_file.name, download_folder


def download_file(page_url, sub_page, dir_path):
    file_name = make_file_name(sub_page)
    response = requests.get(page_url + sub_page)
    file_path = pathlib.Path(dir_path, file_name)
    with open(file_path, 'wb') as new_file:
        new_file.write(response.content)
    return new_file.name


def has_files(html):
    list_of_checks = [
        return_pics_or_none,
    ]
    result = []
    for file in list_of_checks:
        check_result = file(html)
        if check_result is not None:
            result.extend(check_result)
    return result if len(result) > 0 else None


def has_pics(html):
    result = re.findall(r"(?<=img[\W\w]src=\")\S*(?=\")", html)
    return result if len(result) > 0 else None


def return_pics_or_none(html):
    soup = BeautifulSoup(html, features='html.parser')
    result = []
    for imgtag in soup.find_all('img'):
        result.append(imgtag['src'])
    return result if len(result) > 0 else None


def is_link_of_path(string: str):
    return 'Link' if 'http'.startswith(string) else 'Path'


def substitution(links, html_path, dir_name):
    with open(html_path, 'r') as html:
        x = html.read()
    with open(html_path, 'w') as html:
        for link in links:
            x = x.replace(link, os.path.join(dir_name, make_file_name(link)))
        html.write(x)


# t = download('https://page-loader.hexlet.repl.co/')[0]
# h = has_pics(open(t).read())
# substitution(h, t)
