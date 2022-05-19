import re
import requests
import os
import pathlib


def make_file_name(url_):
    result = re.sub(r"^(https?:\/\/)|(\.html)$|[\W_]", '-', url_).strip('-')
    result += '.html'
    return result


def get_url_response(url_):
    response = requests.get(url_)
    return response.text


def download(url_, path='cwd'):
    if path == 'cwd':
        path = os.getcwd()
    file_name = make_file_name(url_)
    text_response = get_url_response(url_)
    file_path = pathlib.Path(path, file_name)
    with open(file_path, 'w') as new_file:
        new_file.write(text_response)
    return new_file.name
