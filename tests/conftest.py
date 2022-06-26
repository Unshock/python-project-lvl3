import pytest
import os
from urllib.parse import urlparse
import pathlib
from page_loader.downloader import get_path


FIXTURES_FOLDER = 'fixtures'
EXPECTED_FOLDER = 'fixtures/expected'
URLS_FOLDER = 'fixtures/urls_and_results'
PAGE_CONTENT_FOLDER = 'fixtures/page_files'


@pytest.fixture
def make_html_response():
    response_path = os.path.join(os.path.dirname(__file__),
                                 FIXTURES_FOLDER, 'hexlet_co_response.html')
    return response_path


@pytest.fixture
def make_expected_html():
    response_path = os.path.join(os.path.dirname(__file__),
                                 EXPECTED_FOLDER,
                                 'hexlet_co_response_with_files.html')
    return response_path


@pytest.fixture
def make_response_3():
    response = os.path.join(os.path.dirname(__file__),
                            FIXTURES_FOLDER, 'site-com-blog-about.html')
    return response


@pytest.fixture
def make_response_4():
    response = os.path.join(os.path.dirname(__file__),
                            FIXTURES_FOLDER,
                            'site-com-blog-about2.html')
    return response


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
def make_pic_path():
    path = os.path.join(os.path.dirname(__file__),
                        URLS_FOLDER,
                        'url1_with_pic.txt')
    with open(path) as url_1:
        url = url_1.read()
        return get_path(url)


@pytest.fixture
def make_url_transformed_1():
    path = os.path.join(os.path.dirname(__file__), URLS_FOLDER,
                        'url1_transform.txt')
    with open(path) as url_1:
        return url_1.read()


@pytest.fixture
def make_url_transformed_2():
    path = os.path.join(os.path.dirname(__file__), URLS_FOLDER,
                        'url2_transform.txt')
    with open(path) as url_2:
        return url_2.read()


@pytest.fixture
def make_url_transformed_3():
    path = os.path.join(os.path.dirname(__file__), URLS_FOLDER,
                        'url3_transform.txt')
    with open(path) as url_3:
        return url_3.read()


@pytest.fixture
def make_url_transformed_4():
    path = os.path.join(os.path.dirname(__file__), URLS_FOLDER,
                        'url4_transform.txt')
    with open(path) as url_4:
        return url_4.read()


@pytest.fixture
def make_url_1_bad():
    path = os.path.join(os.path.dirname(__file__), URLS_FOLDER, 'url1_bad.txt')
    with open(path) as url_1:
        return url_1.read()


@pytest.fixture
def make_pic_name():
    return 'page-loader-hexlet-repl-co-assets-professions-nodejs.png'


@pytest.fixture
def make_file_dir_name():
    return 'page-loader-hexlet-repl-co_files'


@pytest.fixture
def make_url_dir_name():
    return 'https://page-loader.hexlet.repl.co/'


@pytest.fixture
def make_files():
    application_path = os.path.join(os.path.dirname(__file__),
                                    PAGE_CONTENT_FOLDER,
                                    'assets/application.css')
    png_path = os.path.join(os.path.dirname(__file__),
                            PAGE_CONTENT_FOLDER,
                            'assets/professions/nodejs.png')
    script_path = os.path.join(os.path.dirname(__file__),
                               PAGE_CONTENT_FOLDER,
                               'packs/js/script.js')
    script_path2 = os.path.join(os.path.dirname(__file__),
                                PAGE_CONTENT_FOLDER,
                                'packs/js/script2.js')
    courses_path = os.path.join(os.path.dirname(__file__),
                                PAGE_CONTENT_FOLDER,
                                'courses')
    dict_ = {}
    with open(application_path) as application:
        dict_['page-loader-hexlet-repl-co-assets-application.css'] =\
            application.read()
    with open(png_path, 'rb') as png:
        dict_['page-loader-hexlet-repl-co-assets-professions-nodejs.png'] =\
            png.read()
    with open(script_path) as script:
        dict_['page-loader-hexlet-repl-co-packs-js-script.js'] = script.read()
    with open(script_path2) as script2:
        dict_['page-loader-hexlet-repl-co-packs-js-script2.js'] = script2.read()
    with open(courses_path) as courses:
        dict_['page-loader-hexlet-repl-co-courses.html'] = courses.read()
    return dict_


@pytest.fixture
def make_png():
    png_path = os.path.join(os.path.dirname(__file__), PAGE_CONTENT_FOLDER,
                            'assets/professions/nodejs.png')
    dict_ = {}
    with open(png_path, 'rb') as png:
        dict_['page-loader-hexlet-repl-co-assets-professions-nodejs.png'] =\
            png.read()
    return dict_


def fake_loader(true_file_url, file_name, dir_path):
    fake_page_url = os.path.join(os.path.dirname(__file__),
                                 'fixtures/page_files')
    true_sub_page = urlparse(true_file_url).path
    with open(fake_page_url + true_sub_page, 'rb') as file:
        response = file.read()
        file_path = pathlib.Path(dir_path, file_name)
        with open(file_path, 'wb') as new_file:
            new_file.write(response)
        return new_file.name


def fake_loader2(true_file_url, file_name, dir_path):
    return []
