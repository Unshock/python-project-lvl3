import os
import tempfile
import pytest
import responses
from page_loader.exception import CustomConnectionError
from page_loader import downloader
from page_loader import page_loader_engine
from page_loader import url


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

TEST_URL = "https://page-loader.hexlet.repl.co/page/"


# Testing through the main download func
def test_loader_engine(requests_mock, page_files_dataset):

    for file in page_files_dataset:

        file_data = file["file_data"]
        file_link = file["file_link"]
        file_name = file["file_name"]

        if file_name.endswith(".png"):
            requests_mock.get(file_link, content=file_data)
        else:
            requests_mock.get(file_link, text=file_data)

    with open(ORIGINAL_HTML_PATH, 'r') as get_expected:
        requests_mock.get(TEST_URL, text=get_expected.read())

    with tempfile.TemporaryDirectory() as temp_dir:
        os.chdir(temp_dir)
        with tempfile.TemporaryDirectory(dir=temp_dir,
                                         suffix='_inner_dir') as inner_temp_dir:
            result = page_loader_engine.download(TEST_URL, inner_temp_dir)
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
                for elem_name in file_directory_content:
                    elem_path = os.path.join(inner_temp_dir,
                                             DOWNLOADED_FILES_DIR_NAME,
                                             elem_name)
                    file_dict = next((x for x in page_files_dataset
                                      if x["file_name"] == elem_name), None)
                    if elem_path.endswith('.png'):
                        with open(elem_path, 'rb') as el:
                            assert el.read() == file_dict['file_data']
                    else:
                        with open(elem_path, 'r') as el:
                            assert el.read() == file_dict['file_data']


# Testing through the main download func
def test_engine_undefined_path(requests_mock, page_files_dataset):

    for file in page_files_dataset:

        file_data = file["file_data"]
        file_link = file["file_link"]
        file_name = file["file_name"]

        if file_name.endswith(".png"):
            requests_mock.get(file_link, content=file_data)
        else:
            requests_mock.get(file_link, text=file_data)

    with open(ORIGINAL_HTML_PATH, 'r') as get_expected:
        requests_mock.get(TEST_URL, text=get_expected.read())

    with tempfile.TemporaryDirectory() as temp_dir:
        os.chdir(temp_dir)
        result = page_loader_engine.download(TEST_URL)
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
            for elem_name in file_directory_content:
                elem_path = os.path.join(temp_dir,
                                         DOWNLOADED_FILES_DIR_NAME,
                                         elem_name)

                file_dict = next((file for file in page_files_dataset
                                  if file["file_name"] == elem_name), None)

                if elem_path.endswith('.png'):
                    with open(elem_path, 'rb') as el:
                        assert el.read() == file_dict['file_data']
                else:
                    with open(elem_path, 'r') as el:
                        assert el.read() == file_dict['file_data']


# Check of the custom answer for no permission call for download
def test_no_permission(requests_mock):
    with open(ORIGINAL_HTML_PATH, 'r') as get_expected:
        requests_mock.get(TEST_URL, text=get_expected.read())
    with tempfile.TemporaryDirectory() as temp_dir:
        os.chdir(temp_dir)
        os.chmod(temp_dir, 0o111)
        with pytest.raises(PermissionError) as error:
            page_loader_engine.download(TEST_URL)
        assert f'You don\'t have access to the directory \'{temp_dir}\'.' \
               f' Exit.\n' in str(error.value)


# Testing through the main download func
@responses.activate
def test_bad_status_code():
    responses.add(responses.GET, TEST_URL, status=400)
    with tempfile.TemporaryDirectory() as temp_dir:
        os.chdir(temp_dir)
        with pytest.raises(CustomConnectionError) as error:
            page_loader_engine.download(TEST_URL, temp_dir)
        assert 'Request has failed with status code=400. Exit.\n' in\
               str(error.value)


# Testing through the main download func
def test_bad_url():
    with tempfile.TemporaryDirectory() as temp_dir:
        os.chdir(temp_dir)
        bad_url = "https://page-loader.hexlet.re3pl.co/page/"
        with pytest.raises(CustomConnectionError) as error:
            page_loader_engine.download(bad_url, temp_dir)
        assert f'Connection to {bad_url} failed.' \
               f' Exit.\n' in str(error.value)


@responses.activate
def test_download_file_with_bad_file_path():
    PIC_URL = "https://page-loader.hexlet.repl.co/page/assets/professions/" \
              "nodejs.png"
    responses.add(responses.GET, PIC_URL, status=404)
    with tempfile.TemporaryDirectory() as temp_dir:
        os.chdir(temp_dir)
        result = downloader.download_file(PIC_URL)
        assert result is None
        assert len(os.listdir(temp_dir)) == 0


# Testing through the main download func
def test_no_such_directory():
    with tempfile.TemporaryDirectory() as temp_dir:
        os.chdir(temp_dir)
        with pytest.raises(FileExistsError) as error:
            unexisting_dir = temp_dir + '/no_such'
            page_loader_engine.download(TEST_URL, unexisting_dir)
        assert f'The folder with name \"{unexisting_dir}\"'\
               f' does not exists. Exit.\n' in str(error.value)


def test_make_html_name_1():
    assert url.make_file_name(TEST_URL) == \
           "page-loader-hexlet-repl-co-page.html"


def test_make_html_name_2():
    assert url.make_file_name("https://github.com/Unshock?tab=repositories")\
           == "github-com-Unshock.html"


def test_make_html_name_3():
    assert url.make_file_name("https://www.youtube.com/watch?v=5qap5aO4i9A")\
           == "www-youtube-com-watch.html"


def test_make_html_name_4():
    assert url.make_file_name("https://developer.mozilla.org/ru/docs/Learn/"
                              "HTML/Introduction_to_HTML.html") == \
           "developer-mozilla-org-ru-docs-Learn-HTML-Introduction-to-HTML.html"
