import pytest
import os


FIXTURES_FOLDER = 'fixtures'
URLS_FOLDER = 'fixtures/urls_and_results'


@pytest.fixture
def make_response_1():
    response = os.path.join(os.path.dirname(__file__),
                            FIXTURES_FOLDER, 'hexlet_co_response.txt')
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
