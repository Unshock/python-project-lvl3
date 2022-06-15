from page_loader import downloader
import os
import logging

file_log = logging.FileHandler('loader.log')
file_log.setLevel(logging.DEBUG)
console_out = logging.StreamHandler()
console_out.setLevel(logging.INFO)


def loader_engine(page_url, download_folder='cwd',
                  file_loader=downloader.download_file):
    logging.basicConfig(handlers=(file_log, console_out),
                        level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s: %(message)s',
                        datefmt='%d/%m/%Y %I:%M:%S')
    logging.info(f'Start loader_engine {page_url}')
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
    logging.info('Finish loader_engine\n')
    return html_path


g = 'https://page-loader.hexlet.re3pl.co/'
flib = 'https://flibusta.club/'
gs = 'https://gs-labs.ru/'
bio = 'https://bioline.ru/biomebel'
# hex = 'https://ru.hexlet.io/courses'
# t = loader_engine(g, '/home/victor/python/test')
