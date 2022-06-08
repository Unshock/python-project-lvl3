from page_loader import downloader
import os
import logging


def loader_engine(page_url, download_folder='cwd',
                  file_loader=downloader.download_file):
    logging.basicConfig(filename='loader.log', level=logging.INFO,
                        format='%(asctime)s %(levelname)s: %(message)s',
                        datefmt='%d/%m/%Y %I:%M:%S')
    logging.info('------------------------')
    logging.info(f'Start loader_engine {page_url}')
    logging.info('------------------------')
    html_path, download_folder = downloader.download(page_url, download_folder)
    with open(html_path) as html:
        files_sub_pages = downloader.has_files(page_url, html.read())
    if files_sub_pages:
        dir_name, dir_path = downloader.create_files_dir(page_url,
                                                         download_folder)
        for sub_page in files_sub_pages:
            full_file_name = os.path.join(dir_name,
                                          downloader.make_file_name(page_url,
                                                                    sub_page))
            file_loader(page_url, sub_page, dir_path)
            downloader.substitution(html_path, sub_page, full_file_name)
    logging.info('------------------------')
    logging.info('Finish loader_engine')
    logging.info('------------------------')
    return html_path


g = 'https://page-loader.hexlet.repl.co/'
flib = 'https://flibusta.club/'
gs = 'https://gs-labs.ru/'
bio = 'https://bioline.ru/biomebel'
# hex = 'https://ru.hexlet.io/courses'
# t = loader_engine(gs, '/home/victor/python/test')
