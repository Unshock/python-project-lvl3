import pytest
import os


FIXTURES_FOLDER = 'fixtures'


@pytest.fixture
def make_response_1():
    response = os.path.join(os.path.dirname(__file__),
                            FIXTURES_FOLDER, 'hexlet_co_response.txt')
    return response


@pytest.fixture
def make_url_1():
    url = 'https://page-loader.hexlet.repl.co/'
    return url
