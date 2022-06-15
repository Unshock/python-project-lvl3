import os
from page_loader import downloader
from page_loader import loader_engine
import tempfile
from tests.conftest import fake_loader
import logging
import pytest


LOGGER = logging.getLogger(__name__)


def test_download_1(requests_mock, make_url_1, make_response_1):
    with open(make_response_1, 'r') as expected:
        expected = expected.read()
    requests_mock.get(make_url_1, text=expected)
    with tempfile.TemporaryDirectory() as temp_dir:
        os.chdir(temp_dir)
        result = downloader.download(make_url_1)[0]
        with open(result, 'r') as result:
            assert expected == result.read()


def test_download_2(requests_mock, make_url_1, make_response_1):
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


def test_loader_engine(requests_mock, make_url_1,
                       make_response_1, make_response_2,
                       make_file_dir_name, make_pic_name,
                       make_files):
    with open(make_response_1, 'r') as get_expected:
        requests_mock.get(make_url_1, text=get_expected.read())
    with tempfile.TemporaryDirectory() as temp_dir:
        os.chdir(temp_dir)
        with tempfile.TemporaryDirectory(dir=temp_dir,
                                         suffix='_inner_dir') as inner_temp_dir:
            result = loader_engine.loader_engine(make_url_1, inner_temp_dir,
                                                 file_loader=fake_loader)
            result = open(result)
            with open(make_response_2, 'r') as result_expected:
                directory_content = os.listdir(inner_temp_dir)
                file_directory_content = os.listdir(os.path.join(
                    inner_temp_dir,
                    make_file_dir_name))
                assert result_expected.read() == result.read()
                assert len(os.listdir(inner_temp_dir)) == 2
                assert make_file_dir_name in directory_content
                assert make_pic_name in file_directory_content
                for elem in file_directory_content:
                    elem_path = os.path.join(inner_temp_dir,
                                             make_file_dir_name,
                                             elem)
                    if elem_path.endswith('.png'):
                        with open(elem_path, 'rb') as el:
                            assert el.read() == make_files[elem]
                    else:
                        with open(elem_path, 'r') as el:
                            print(el)
                            assert el.read() == make_files[elem]


def test_permission_1(requests_mock, make_url_1, make_response_1):
    with open(make_response_1, 'r') as get_expected:
        requests_mock.get(make_url_1, text=get_expected.read())
    with tempfile.TemporaryDirectory() as temp_dir:
        os.chdir(temp_dir)
        os.chmod(temp_dir, 0o111)
        with pytest.raises(PermissionError):
            loader_engine.loader_engine(make_url_1, file_loader=fake_loader)


def test_make_html_name_1(make_url_1, make_url_transformed_1):
    assert downloader.make_html_name(make_url_1) == make_url_transformed_1


def test_make_html_name_2(make_url_2, make_url_transformed_2):
    assert downloader.make_html_name(make_url_2) == make_url_transformed_2


def test_make_html_name_3(make_url_3, make_url_transformed_3):
    assert downloader.make_html_name(make_url_3) == make_url_transformed_3


def test_make_html_name_4(make_url_4, make_url_transformed_4):
    assert downloader.make_html_name(make_url_4) == make_url_transformed_4
