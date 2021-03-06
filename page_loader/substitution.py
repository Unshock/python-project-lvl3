import logging


def substitute(html_path: str, attribute_value: str, local_file_path: str):
    """
    :param html_path: path to downloaded web page html file
    :param attribute_value: attribute value in html file that has
        been downloaded locally and should have new path to local file
    :param local_file_path: relative path to local file that is
        html_files/file-name and should be put in HTML file
    :return: returns nothing, but substitute one given attribute value to
        relative file path in given HTML document
    """
    with open(html_path, 'r') as html:
        x = html.read()
    with open(html_path, 'w') as html:
        x = x.replace(f'"{attribute_value}"', f'"{local_file_path}"')
        html.write(x)
    logging.info(f'Name {attribute_value} replaced with {local_file_path}')
