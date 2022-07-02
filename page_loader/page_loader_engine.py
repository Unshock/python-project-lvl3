import os
import logging
from progress.bar import Bar
from page_loader import downloader
from page_loader.processing import normalize_download_folder
from page_loader.substitution import substitute
import logging.config


# file_log = logging.FileHandler(os.path.join('loader.log'))
# file_log.setLevel(logging.DEBUG)
# console_out = logging.StreamHandler()
# console_out.setLevel(logging.INFO)

# logging.basicConfig(handlers=(file_log, console_out),
#                    level=logging.DEBUG,
#                    format='%(asctime)s %(levelname)s: %(message)s',
#                    datefmt='%d/%m/%Y %I:%M:%S')

# if __name__ == '__main__':

# logger = logging.getLogger(__name__)


def download(page_url, download_folder='cwd',
             file_loader=downloader.download_file):
    download_folder = normalize_download_folder(download_folder)
    # logging.config.fileConfig(fname='page_loader/b.conf',
    #                          disable_existing_loggers=False)

    logging.info(f'Start loader_engine {page_url}')

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
    logging.info('Finish loader_engine\n')
    return html_path

# print('imya:', __name__)
# g = download('https://page-loader.hexlet.repl.co', '/home/victor/python/test')
