from page_loader import downloader
import os
import logging
from progress.bar import Bar


if __name__ == '__main__':
    file_log = logging.FileHandler('loader.log')
    file_log.setLevel(logging.DEBUG)
    console_out = logging.StreamHandler()
    console_out.setLevel(logging.WARNING)

    logging.basicConfig(handlers=(file_log, console_out),
                        level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s: %(message)s',
                        datefmt='%d/%m/%Y %I:%M:%S')


def loader_engine(page_url, download_folder='cwd',
                  file_loader=downloader.download_file):

    logging.info(f'Start loader_engine {page_url}')
    download_folder = downloader.normalize_download_folder(download_folder)
    html_path = downloader.download(page_url, download_folder)
    with open(html_path) as html:
        files_sub_pages = downloader.make_list_of_files(page_url, html.read())
    # if files_sub_pages:
    dir_name, dir_path = downloader.create_files_dir(page_url,
                                                     download_folder)
    with Bar('Downloading local files', max=len(files_sub_pages)) as bar:
        for sub_page in files_sub_pages:
            if file_loader(sub_page['link'], sub_page['name'], dir_path):
                html_file_path = os.path.join(dir_name, sub_page['name'])
                downloader.substitution(html_path,
                                        sub_page['attribute_value'],
                                        html_file_path)

            bar.next()
    logging.info('Finish loader_engine\n')
    return html_path
