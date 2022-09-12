import os
import logging
from progress.bar import Bar
from page_loader import downloader
from page_loader import resources
from page_loader import file_system
from page_loader.url import make_file_name, make_dir_name


def download(page_url: str, download_folder='.',
             file_loader=downloader.download_file) -> str:
    """
    :param page_url: the url of the original page needed to be downloaded
    :param download_folder: path where HTML file should be downloaded
    :param file_loader: for the availability to use mocks in tests
    :return: the function gets the url and the download folder directory path
        (optionally) and downloads HTML by the given URL and all local files in
        the tags: img, link, script. So the given page can be open locally
        without internet connection. Function returns the absolute path to the
        downloaded HTML file.
    """
    download_folder = os.path.abspath(download_folder)

    if not os.path.exists(download_folder):
        error_message = f'The folder with name \"{download_folder}\"' \
                        f' does not exists. Exit.\n'
        raise FileExistsError(error_message)

    html_response = file_loader(page_url, exit_ability=True)

    beautiful_html, assets = resources.prepare_assets(page_url,
                                                      html_response.text)

    html_path = file_system.save_file(beautiful_html,
                                      make_file_name(page_url),
                                      download_folder)

    if assets:
        files_dir_path = os.path.join(download_folder, make_dir_name(page_url))

        if not os.path.exists(files_dir_path):
            os.mkdir(files_dir_path)

        with Bar('Downloading local files', max=len(assets)) as bar:
            for file in assets:

                file_url = file['url']
                file_name = file['name']

                file_response = file_loader(file_url, exit_ability=False)
                if file_response:
                    file_system.save_file(file_response.content,
                                          file_name, files_dir_path)
                bar.next()

    logging.info('Download finished\n')
    return html_path
