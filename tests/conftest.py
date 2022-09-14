import pytest
import os


FIXTURES_FOLDER = 'fixtures'
EXPECTED_FOLDER_FILES = 'fixtures/expected/' \
                        'page-loader-hexlet-repl-co-page_files'
PAGE_CONTENT_FOLDER = 'fixtures/page_structure'
MAIN_HTML_FILE = 'page-loader-hexlet-repl-co-page.html'


@pytest.fixture(scope="module")
def page_files_dataset():

    list_of_files = \
        [{"file_link": "https://page-loader.hexlet.repl.co"
                       "/page/packs/js/script1.js",
          "file_name": "page-loader-hexlet-repl-co-page-packs-js-script1.js"},
         {"file_link": "https://page-loader.hexlet.repl.co"
                       "/page/assets/application.css",
          "file_name": "page-loader-hexlet-repl-co"
                       "-page-assets-application.css"},
         {"file_link": "https://page-loader.hexlet.repl.co"
                       "/page/assets/professions/nodejs.png",
          "file_name": "page-loader-hexlet-repl-co"
                       "-page-assets-professions-nodejs.png"},
         {"file_link": "https://page-loader.hexlet.repl.co"
                       "/page/packs/js/script2.js",
          "file_name": "page-loader-hexlet-repl-co-page-packs-js-script2.js"},
         {"file_link": "https://page-loader.hexlet.repl.co/script3.js",
          "file_name": "page-loader-hexlet-repl-co-script3.js"},
         {"file_link": "https://page-loader.hexlet.repl.co/page/courses",
          "file_name": "page-loader-hexlet-repl-co-page-courses.html"}
         ]

    for file in list_of_files:
        file_name = file["file_name"]
        file_path = os.path.join(os.path.dirname(__file__),
                                 EXPECTED_FOLDER_FILES,
                                 file_name)
        if file_name.endswith(".png"):
            with open(file_path, "rb") as opened_file:
                content = opened_file.read()

        else:
            with open(file_path) as opened_file:
                content = opened_file.read()

        file["file_data"] = content
        file["file_path"] = file_path

    return list_of_files
