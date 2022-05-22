import os
from page_loader import downloader
import tempfile


def test_generator_1(requests_mock, make_url_1, make_response_1):
    with open(make_response_1, 'r') as expected:
        expected = expected.read()
    requests_mock.get(make_url_1, text=expected)
    with tempfile.TemporaryDirectory() as temp_dir:
        os.chdir(temp_dir)
        result = downloader.download(make_url_1)[0]
        with open(result, 'r') as result:
            assert expected == result.read()


def test_generator_2(requests_mock, make_url_1, make_response_1):
    with open(make_response_1, 'r') as expected:
        expected = expected.read()
    requests_mock.get(make_url_1, text=expected)
    with tempfile.TemporaryDirectory() as temp_dir:
        os.chdir(temp_dir)
        with tempfile.TemporaryDirectory(dir=temp_dir,
                                         suffix='_inner_dir') as inner_temp_dir:
            result = downloader.download(make_url_1, inner_temp_dir)[0]
            with open(result, 'r') as result:
                assert expected == result.read()


def test_make_html_name_1(make_url_1, make_url_transformed_1):
    assert downloader.make_html_name(make_url_1) == make_url_transformed_1


def test_make_html_name_2(make_url_2, make_url_transformed_2):
    assert downloader.make_html_name(make_url_2) == make_url_transformed_2


def test_make_html_name_3(make_url_3, make_url_transformed_3):
    assert downloader.make_html_name(make_url_3) == make_url_transformed_3


def test_make_html_name_4(make_url_4, make_url_transformed_4):
    assert downloader.make_html_name(make_url_4) == make_url_transformed_4
