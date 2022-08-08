import os
import logging
from progress.bar import Bar
from page_loader import downloader
from page_loader import resources
from page_loader import file_system
from page_loader.naming import make_file_name


# Записка для проверяющего
# По совету Маруфа изменил логику приложения. Оставил одну "универсальную"
# функцию для скачивания главной HTML страницы или локальных файлов.
# Сделал обработку HTML с изменением Всех найденных локальных путей, в независи
# мости от того, был ли файл скачан или нет.
# создал дополнительные модули и распеделил по ним функции.


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

    html_response = file_loader(page_url, main_html=True)

    list_of_files, beautiful_html = resources.handle_html(page_url,
                                                          html_response.text)

    final_html_path = file_system.save_file(beautiful_html,
                                            make_file_name(page_url),
                                            download_folder)
    if list_of_files:
        dir_name, dir_path = resources.create_local_files_dir(page_url,
                                                              download_folder)
        with Bar('Downloading local files', max=len(list_of_files)) as bar:
            for sub_page in list_of_files:

                download_link = sub_page['url']
                file_name = sub_page['name']
                file_response = file_loader(download_link)

                file_system.save_file(file_response.content,
                                      file_name, dir_path)
            bar.next()

    logging.info('Download finished\n')
    return final_html_path
