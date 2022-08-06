import os
import logging
from progress.bar import Bar
from page_loader import downloader
from page_loader.substitution import substitute


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

    logging.info(f'Start to download {page_url}')

    html_path = downloader.download_html(page_url, download_folder)
    with open(html_path) as html:
        files_sub_pages = downloader.make_list_of_files(page_url, html.read())
    if files_sub_pages:
        dir_name, dir_path = downloader.create_local_files_dir(page_url,
                                                               download_folder)
        with Bar('Downloading local files', max=len(files_sub_pages)) as bar:
            for sub_page in files_sub_pages:

                download_link = sub_page['link']
                file_name = sub_page['name']
                html_attribute_value = sub_page['attribute_value']

                download_files = file_loader(download_link, file_name, dir_path)
                if download_files:
                    local_file_path = os.path.join(dir_name, file_name)
                    substitute(html_path, html_attribute_value, local_file_path)

                bar.next()
    logging.info('Download finished\n')
    return html_path
