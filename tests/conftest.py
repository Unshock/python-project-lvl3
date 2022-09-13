import pytest
import os
from urllib.parse import urlparse


FIXTURES_FOLDER = 'fixtures'
EXPECTED_FOLDER_FILES = 'fixtures/expected/' \
                        'page-loader-hexlet-repl-co-page_files'
PAGE_CONTENT_FOLDER = 'fixtures/page_structure'
MAIN_HTML_FILE = 'page-loader-hexlet-repl-co-page.html'


@pytest.fixture(scope="module")
def page_files_dataset():

    list_of_files = ['page-loader-hexlet-repl-co-page-assets-application.css',
                     'page-loader-hexlet-repl-co-page-assets-'
                     'professions-nodejs.png',
                     'page-loader-hexlet-repl-co-page-packs-js-script1.js',
                     'page-loader-hexlet-repl-co-page-packs-js-script2.js',
                     'page-loader-hexlet-repl-co-script3.js',
                     'page-loader-hexlet-repl-co-page-courses.html'
                     ]

    dataset_dict = {}
    for file_name in list_of_files:
        file_path = os.path.join(os.path.dirname(__file__),
                                 EXPECTED_FOLDER_FILES,
                                 file_name)
        if file_name[-3:] == "png":
            with open(file_path, 'rb') as file:
                dataset_dict[file_name] = file.read()
        else:
            with open(file_path) as file:
                dataset_dict[file_name] = file.read()
    return dataset_dict


class FakeResponse:
    def __init__(self, response):
        self.response = response

    @property
    def content(self):
        return self.response

    @property
    def text(self):
        return str(self.response)


def fake_loader(true_file_url, *, exit_ability=False):
    fake_page_url = os.path.join(os.path.dirname(__file__),
                                 PAGE_CONTENT_FOLDER)
    true_sub_page = urlparse(true_file_url).path

    if exit_ability:
        path = os.path.join(os.path.dirname(__file__),
                            FIXTURES_FOLDER,
                            MAIN_HTML_FILE)
        with open(path, 'r') as file:
            fake_response = FakeResponse(file.read())
            return fake_response
    elif true_sub_page[0] == '/':
        path = fake_page_url + true_sub_page
    else:
        path = f'{fake_page_url}/{true_sub_page}'

    with open(path, 'rb') as file:
        fake_response = FakeResponse(file.read())
        return fake_response
