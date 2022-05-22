from page_loader import downloader
import os


def loader_engine(url_, path='cwd'):
    html_path, path = downloader.download(url_, path)
    with open(html_path) as html:
        files = downloader.has_pics(html.read())
    if files:
        dir_name = os.path.join(path, downloader.make_dir_name(url_))
        os.mkdir(dir_name)
        for file in files:
            downloader.download_file(url_, file, dir_name)
        downloader.substitution(files, html_path, dir_name)
    return html_path


t = loader_engine('https://page-loader.hexlet.repl.co/',
                  '/home/victor/python/test')
