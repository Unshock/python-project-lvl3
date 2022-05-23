from page_loader import downloader
import os


def loader_engine(page_url, download_folder='cwd'):
    html_path, download_folder = downloader.download(page_url, download_folder)
    with open(html_path) as html:
        files_sub_pages = downloader.has_files(html.read())
    if files_sub_pages:
        dir_name = os.path.join(download_folder,
                                downloader.make_name(page_url, type='dir'))
        os.mkdir(dir_name)
        for sub_page in files_sub_pages:
            downloader.download_file(page_url, sub_page, dir_name)
        downloader.substitution(files_sub_pages, html_path, dir_name)
    return html_path


# t = loader_engine('https://page-loader.hexlet.repl.co/',
#                   '/home/victor/python/test')
