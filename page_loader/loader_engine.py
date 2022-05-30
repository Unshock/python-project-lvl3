from page_loader import downloader
import os


def loader_engine(page_url, download_folder='cwd',
                  file_loader=downloader.download_file):
    html_path, download_folder = downloader.download(page_url, download_folder)
    with open(html_path) as html:
        files_sub_pages = downloader.has_files(html.read())
    if files_sub_pages:
        dir_name = downloader.make_name(page_url, type='dir')
        dir_path = os.path.join(download_folder, dir_name)
        os.mkdir(dir_path)
        for sub_page in files_sub_pages:
            file_loader(page_url, sub_page, dir_path)
        downloader.substitution(files_sub_pages, html_path, dir_name)
    return html_path

# g = 'https://page-loader.hexlet.repl.co/'
# flib = 'https://flibusta.club/'
# stak = 'https://gs-labs.ru/'
# bio = 'https://bioline.ru/catalog'
# t = loader_engine(g, '/home/victor/python/test')
