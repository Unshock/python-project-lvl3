import pytest
import os
from urllib.parse import urlparse
import pathlib
import urllib


FIXTURES_FOLDER = 'fixtures'
EXPECTED_FOLDER = 'fixtures/expected'
EXPECTED_FOLDER_FILES = 'fixtures/expected/' \
                        'page-loader-hexlet-repl-co-page_files'
URLS_FOLDER = 'fixtures/urls_and_results'
PAGE_CONTENT_FOLDER = 'fixtures/page_structure'


@pytest.fixture
def make_html_response():
    response_path = os.path.join(os.path.dirname(__file__),
                                 FIXTURES_FOLDER,
                                 'page-loader-hexlet-repl-co-page.html')
    return response_path


@pytest.fixture
def make_expected_html():
    response_path = os.path.join(os.path.dirname(__file__),
                                 EXPECTED_FOLDER,
                                 'page-loader-hexlet-repl-co-page.html')
    return response_path


@pytest.fixture
def make_url_1():
    path = os.path.join(os.path.dirname(__file__), URLS_FOLDER, 'url1.txt')
    with open(path) as url_1:
        return url_1.read()


@pytest.fixture
def make_url_2():
    path = os.path.join(os.path.dirname(__file__), URLS_FOLDER, 'url2.txt')
    with open(path) as url_2:
        return url_2.read()


@pytest.fixture
def make_url_3():
    path = os.path.join(os.path.dirname(__file__), URLS_FOLDER, 'url3.txt')
    with open(path) as url_3:
        return url_3.read()


@pytest.fixture
def make_url_4():
    path = os.path.join(os.path.dirname(__file__), URLS_FOLDER, 'url4.txt')
    with open(path) as url_4:
        return url_4.read()


@pytest.fixture
def make_url_1_with_pic():
    path = os.path.join(os.path.dirname(__file__),
                        URLS_FOLDER,
                        'url1_with_pic.txt')
    with open(path) as url_1:
        return url_1.read()


@pytest.fixture
def make_url_expected_1():
    path = os.path.join(os.path.dirname(__file__), URLS_FOLDER,
                        'url1_expected.txt')
    with open(path) as url_1:
        return url_1.read()


@pytest.fixture
def make_url_expected_2():
    path = os.path.join(os.path.dirname(__file__), URLS_FOLDER,
                        'url2_expected.txt')
    with open(path) as url_2:
        return url_2.read()


@pytest.fixture
def make_url_expected_3():
    path = os.path.join(os.path.dirname(__file__), URLS_FOLDER,
                        'url3_expected.txt')
    with open(path) as url_3:
        return url_3.read()


@pytest.fixture
def make_url_expected_4():
    path = os.path.join(os.path.dirname(__file__), URLS_FOLDER,
                        'url4_expected.txt')
    with open(path) as url_4:
        return url_4.read()


@pytest.fixture
def make_url_1_bad():
    path = os.path.join(os.path.dirname(__file__), URLS_FOLDER, 'url1_bad.txt')
    with open(path) as url_1:
        return url_1.read()


@pytest.fixture
def make_pic_name():
    return 'page-loader-hexlet-repl-co-page-assets-professions-nodejs.png'


@pytest.fixture
def make_file_dir_name():
    return 'page-loader-hexlet-repl-co-page_files'


@pytest.fixture
def make_html_name():
    return 'page-loader-hexlet-repl-co-page.html'


@pytest.fixture
def make_files():
    application_name = 'page-loader-hexlet-repl-co-page-assets-application.css'
    png_name = 'page-loader-hexlet-repl-co-page-assets-professions-nodejs.png'
    script_name1 = 'page-loader-hexlet-repl-co-page-packs-js-script1.js'
    script_name2 = 'page-loader-hexlet-repl-co-page-packs-js-script2.js'
    script_name3 = 'page-loader-hexlet-repl-co-script3.js'
    courses_name = 'page-loader-hexlet-repl-co-page-courses.html'

    application_path = os.path.join(os.path.dirname(__file__),
                                    EXPECTED_FOLDER_FILES,
                                    application_name)
    png_path = os.path.join(os.path.dirname(__file__),
                            EXPECTED_FOLDER_FILES,
                            png_name)
    script_path = os.path.join(os.path.dirname(__file__),
                               EXPECTED_FOLDER_FILES,
                               script_name1)
    script_path2 = os.path.join(os.path.dirname(__file__),
                                EXPECTED_FOLDER_FILES,
                                script_name2)
    script_path3 = os.path.join(os.path.dirname(__file__),
                                EXPECTED_FOLDER_FILES,
                                script_name3)
    courses_path = os.path.join(os.path.dirname(__file__),
                                EXPECTED_FOLDER_FILES,
                                courses_name)
    dict_ = {}
    with open(application_path) as application:
        dict_['page-loader-hexlet-repl-co-page-assets-application.css']\
            = application.read()
    with open(png_path, 'rb') as png:
        dict_['page-loader-hexlet-repl-co-page-assets-professions-nodejs.png']\
            = png.read()
    with open(script_path) as script:
        dict_['page-loader-hexlet-repl-co-page-packs-js-script1.js']\
            = script.read()
    with open(script_path2) as script2:
        dict_['page-loader-hexlet-repl-co-page-packs-js-script2.js']\
            = script2.read()
    with open(script_path3) as script3:
        dict_['page-loader-hexlet-repl-co-script3.js'] = script3.read()
    with open(courses_path) as courses:
        dict_['page-loader-hexlet-repl-co-page-courses.html'] = courses.read()
    return dict_


@pytest.fixture
def make_png():
    png_path = os.path.join(os.path.dirname(__file__), PAGE_CONTENT_FOLDER,
                            'assets/professions/nodejs.png')
    dict_ = {}
    with open(png_path, 'rb') as png:
        dict_['page-loader-hexlet-repl-co-page-assets-professions-nodejs.png']\
            = png.read()
    return dict_


def fake_loader(true_file_url, file_name, dir_path):
    fake_page_url = os.path.join(os.path.dirname(__file__),
                                 PAGE_CONTENT_FOLDER)
    true_sub_page = urlparse(true_file_url).path
    path = urllib.parse.urljoin(fake_page_url, true_sub_page)
    if true_sub_page[0] == '/':
        path = fake_page_url + true_sub_page
    else:
        path = f'{fake_page_url}/{true_sub_page}'
    with open(path, 'rb') as file:
        response = file.read()
        file_path = pathlib.Path(dir_path, file_name)
        with open(file_path, 'wb') as new_file:
            new_file.write(response)
        return os.path.abspath(new_file.name)
