import os
from page_loader import downloader
import tempfile


def test_generator_1(requests_mock, make_url_1, make_response_1):
    with open(make_response_1, 'r') as expected:
        expected = expected.read()
    requests_mock.get(make_url_1, text=expected)
    with tempfile.TemporaryDirectory() as temp_dir:
        os.chdir(temp_dir)
        result = downloader.download(make_url_1)
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
            result = downloader.download(make_url_1, inner_temp_dir)
            with open(result, 'r') as result:
                assert expected == result.read()
