import logging
import os
import pathlib


def save_file(response, file_name, folder):
    """
    :param response: data of the downloaded file
    :param file_name: the name file should be saved with
    :param folder: folder file should be saved to
    :return: gets the data of downloaded file and saves it in given directory.
        Returns full path to the saved file.
    """
    file_path = pathlib.Path(folder, file_name)

    try:
        file_path.touch(exist_ok=False)
    except FileExistsError:
        error_message = f'File \'{file_path}\' already exists. Exit.\n'
        raise FileExistsError(error_message)
    except PermissionError:
        error_message = f'You don\'t have access to the directory' \
                        f' \'{folder}\'. Exit.\n'
        raise PermissionError(error_message)

    if isinstance(response, bytes):
        with open(file_path, 'wb') as new_file:
            new_file.write(response)
    elif isinstance(response, str):
        with open(file_path, 'w') as new_file:
            new_file.write(response)
    else:
        raise

    logging.info(f'File \'{file_name}\' saved in \'{folder}\'')

    return os.path.abspath(new_file.name)
