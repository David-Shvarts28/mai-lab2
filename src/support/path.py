import os

def absolute_path(path: str|None) -> str:
    """
    Преобразование относительного пути в абсолютный.

    :param path: Строка в которой хранится путь
    :return: Возвращает абсолютный путь или строку, содержащую полный путь к текущему каталогу.
    """
    if path is None or len(str(path)) == 0:
        return os.getcwd()
    return os.path.abspath(os.path.expanduser(os.path.expandvars(path)))

def verify_path_for_rm(path: str) -> bool:
    """
    Специальная защитная функция для команды rm, которая проверяет, не пытается ли
    пользователь удалить корневой или родительский каталог.

    :param path: Строка в которой хранится путь
    :return: False - если путь в запрещенном списке, True - если путь подходит
    """
    path_for_rm = absolute_path(path)
    haram = [os.path.abspath("/"), # корневой каталог
             os.path.dirname(os.getcwd())] # родительский каталог

    if path_for_rm in haram:
        return False
    return True
