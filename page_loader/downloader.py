import re
import requests
import os
import pathlib


def make_html_name(url_):
    result = re.sub(r"^(https?:\/\/)|(\.html)$|[\W_]", '-', url_).strip('-')
    result += '.html'
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


def download(url_, path='cwd'):
    if path == 'cwd':
        path = os.getcwd()
    file_name = make_html_name(url_)
    text_response = get_url_response(url_)
    file_path = pathlib.Path(path, file_name)
    with open(file_path, 'w') as new_file:
        new_file.write(text_response)
    return new_file.name, path


def download_file(url_, link_to_file, dir):
    file_name = make_file_name(link_to_file)
    response = requests.get(url_ + link_to_file)
    file_path = pathlib.Path(dir, file_name)
    with open(file_path, 'wb') as new_file:
        new_file.write(response.content)
    return new_file.name


def has_pics(html):
    result = re.findall(r"(?<=img src=\")\S*(?=\")", html)
    return result if len(result) > 0 else False


def is_link_of_path(string):
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
