import os
from .path import absolute_path

def check_path_correct(path: str) -> str:
    """
    Проверяет что путь существует.

    :param path: Строка, содержащая путь для проверки.
    :return: Абсолютный путь, если проверка пройдена.
    :raises FileNotFoundError: Если путь не существует.
    """
    path = absolute_path(path)
    if os.path.exists(path):
        return path
    else:
        raise FileNotFoundError("Путь не существует")


def check_is_file(path: str) -> str: #type: ignore
    """
    Проверяет что путь ведет к файлу.

    :param path: Строка, содержащая путь для проверки.
    :return: Абсолютный путь, если проверка пройдена.
    :raises FileNotFoundError: Если путь не существует.
    :raises IsADirectoryError: Если путь ведет к папке.
    """
    path = check_path_correct(path)
    if os.path.isfile(path):
        return path
    elif os.path.isdir(path):
        raise IsADirectoryError("Путь ведет к папке а не к файлу")



def check_is_dir(path: str) -> str: #type: ignore
    """
    Проверяет что путь ведет к папке.

    :param path: Строка, содержащая путь для проверки.
    :return: Абсолютный путь, если проверка пройдена.
    :raises FileNotFoundError: Если путь не существует.
    :raises NotADirectoryError: Если путь ведет к файлу.
    """
    path = check_path_correct(path)
    if os.path.isdir(path):
        return path
    elif os.path.isfile(path):
        raise NotADirectoryError("Путь ведет к файлу а не к папке")
