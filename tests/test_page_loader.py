import os
import tempfile
import pytest
import responses
from page_loader.exception import CustomConnectionError
from page_loader import downloader
from page_loader import page_loader_engine
from page_loader import url
from tests.conftest import fake_loader

FIXTURES_FOLDER = 'fixtures'
EXPECTED_FOLDER = 'fixtures/expected'
EXPECTED_FOLDER_FILES = 'fixtures/expected/' \
                        'page-loader-hexlet-repl-co-page_files'
URLS_FOLDER = 'fixtures/urls_and_results'
PAGE_CONTENT_FOLDER = 'fixtures/page_structure'
MAIN_HTML_FILE = 'page-loader-hexlet-repl-co-page.html'

ORIGINAL_HTML_PATH = os.path.join(os.path.dirname(__file__),
                                  FIXTURES_FOLDER,
                                  MAIN_HTML_FILE)


EXPECTED_HTML_PATH = os.path.join(os.path.dirname(__file__),
                                  EXPECTED_FOLDER,
                                  MAIN_HTML_FILE)

PICTURE_NAME = "page-loader-hexlet-repl-co-page-assets-professions-nodejs.png"
DOWNLOADED_FILES_DIR_NAME = "page-loader-hexlet-repl-co-page_files"


# Testing through the main download func
def test_loader_engine(requests_mock, make_url_1, make_files):
    with open(ORIGINAL_HTML_PATH, 'r') as get_expected:
        requests_mock.get(make_url_1, text=get_expected.read())
    with tempfile.TemporaryDirectory() as temp_dir:
        os.chdir(temp_dir)
        with tempfile.TemporaryDirectory(dir=temp_dir,
                                         suffix='_inner_dir') as inner_temp_dir:
            result = page_loader_engine.download(make_url_1,
                                                 inner_temp_dir,
                                                 file_loader=fake_loader)
            result = open(result)
            with open(EXPECTED_HTML_PATH, 'r') as result_expected:
                directory_content = os.listdir(inner_temp_dir)
                file_directory_content = os.listdir(os.path.join(
                    inner_temp_dir,
                    DOWNLOADED_FILES_DIR_NAME))

                assert result_expected.read() == result.read()
                assert len(directory_content) == 2
                assert len(file_directory_content) == 6
                assert DOWNLOADED_FILES_DIR_NAME in directory_content
                assert MAIN_HTML_FILE in directory_content
                assert PICTURE_NAME in file_directory_content
                for elem in file_directory_content:
                    elem_path = os.path.join(inner_temp_dir,
                                             DOWNLOADED_FILES_DIR_NAME,
                                             elem)
                    if elem_path.endswith('.png'):
                        with open(elem_path, 'rb') as el:
                            assert el.read() == make_files[elem]
                    else:
                        with open(elem_path, 'r') as el:
                            assert el.read() == make_files[elem]


# Testing through the main download func
def test_engine_undefined_path(requests_mock, make_url_1, make_files):
    with open(ORIGINAL_HTML_PATH, 'r') as get_expected:
        requests_mock.get(make_url_1, text=get_expected.read())
    with tempfile.TemporaryDirectory() as temp_dir:
        os.chdir(temp_dir)
        result = page_loader_engine.download(make_url_1,
                                             file_loader=fake_loader)
        result = open(result)
        with open(EXPECTED_HTML_PATH, 'r') as result_expected:
            directory_content = os.listdir(temp_dir)
            file_directory_content = os.listdir(os.path.join(
                                                temp_dir,
                                                DOWNLOADED_FILES_DIR_NAME))
            assert result_expected.read() == result.read()
            assert len(directory_content) == 2
            assert len(file_directory_content) == 6
            assert DOWNLOADED_FILES_DIR_NAME in directory_content
            assert MAIN_HTML_FILE in directory_content
            assert PICTURE_NAME in file_directory_content
            for elem in file_directory_content:
                elem_path = os.path.join(temp_dir,
                                         DOWNLOADED_FILES_DIR_NAME,
                                         elem)
                if elem_path.endswith('.png'):
                    with open(elem_path, 'rb') as el:
                        assert el.read() == make_files[elem]
                else:
                    with open(elem_path, 'r') as el:
                        assert el.read() == make_files[elem]


# Добавил в библиотеку кастомный ответ, в случае отсутствия разрешения на
# скачивание в директорию. Тут его проверяю.
def test_no_permission(requests_mock, make_url_1):
    with open(ORIGINAL_HTML_PATH, 'r') as get_expected:
        requests_mock.get(make_url_1, text=get_expected.read())
    with tempfile.TemporaryDirectory() as temp_dir:
        os.chdir(temp_dir)
        os.chmod(temp_dir, 0o111)
        with pytest.raises(PermissionError) as error:
            page_loader_engine.download(make_url_1,
                                        file_loader=fake_loader)
        assert f'You don\'t have access to the directory \'{temp_dir}\'.' \
               f' Exit.\n' in str(error.value)


# Testing through the main download func
@responses.activate
def test_bad_status_code(make_url_1):
    responses.add(responses.GET, make_url_1, status=400)
    with tempfile.TemporaryDirectory() as temp_dir:
        os.chdir(temp_dir)
        with pytest.raises(CustomConnectionError) as error:
            page_loader_engine.download(make_url_1, temp_dir)
        assert 'Request has failed with status code=400. Exit.\n' in\
               str(error.value)


# Testing through the main download func
def test_bad_url(make_url_1_bad):
    with tempfile.TemporaryDirectory() as temp_dir:
        os.chdir(temp_dir)
        with pytest.raises(CustomConnectionError) as error:
            page_loader_engine.download(make_url_1_bad, temp_dir)
        assert f'Connection to {make_url_1_bad} failed.' \
               f' Exit.\n' in str(error.value)


@responses.activate
def test_download_file_with_bad_file_path(make_url_1_with_pic):
    responses.add(responses.GET, make_url_1_with_pic, status=404)
    with tempfile.TemporaryDirectory() as temp_dir:
        os.chdir(temp_dir)
        result = downloader.download_file(make_url_1_with_pic)
        assert result is None
        assert len(os.listdir(temp_dir)) == 0


# Testing through the main download func
def test_no_such_directory(make_url_1):
    with tempfile.TemporaryDirectory() as temp_dir:
        os.chdir(temp_dir)
        with pytest.raises(FileExistsError) as error:
            unexisting_dir = temp_dir + '/no_such'
            page_loader_engine.download(make_url_1, unexisting_dir)
        assert f'The folder with name \"{unexisting_dir}\"'\
               f' does not exists. Exit.\n' in str(error.value)


def test_make_html_name_1(make_url_1, make_url_expected_1):
    assert url.make_file_name(make_url_1) == make_url_expected_1


def test_make_html_name_2(make_url_2, make_url_expected_2):
    assert url.make_file_name(make_url_2) == make_url_expected_2


def test_make_html_name_3(make_url_3, make_url_expected_3):
    assert url.make_file_name(make_url_3) == make_url_expected_3


def test_make_html_name_4(make_url_4, make_url_expected_4):
    assert url.make_file_name(make_url_4) == make_url_expected_4
