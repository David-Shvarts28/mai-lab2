import os
import shutil
import stat
from datetime import datetime
from src.support.logger import log_command, log_error, log_success
from src.support.check import check_is_dir


def ls(*args) -> str:
    """
    Выводит список файлов и каталогов в указанной директории.

    :param args: Аргументы команды.
    :return: Отформатированная строка с содержимым директории.
    :raises FileNotFoundError: Если указанный путь не существует.
    :raises NotADirectoryError: Если указанный путь ведет к файлу.
    :raises OSError: Если произошла ошибка ввода-вывода при работе с файловой системой.
    """
    log_command(f"ls {' '.join(args)}")

    try:
        path = None
        for arg in args:
            if not arg.startswith('-'):
                path = arg
                break

        if path is not None: #было path != None, я ненавижу pre-commit((
            path_verify = check_is_dir(path)
        else:
            path_verify = check_is_dir('.')

        items = [i for i in sorted(os.listdir(path_verify)) if not i.startswith(".")]

        if '-l' in args:
            result = "\n".join(format_l(item, path_verify) for item in items)
        else:
            result = format_no_l(items)

        log_success("ls", f"{len(items)} items")
        return result

    except FileNotFoundError:
        error_message = "No such file or directory"
        log_error(error_message)
        if len(args) == 2 and args[0] == '-' and args[1] == 'l':
            return f"ls: {args[0]}: {error_message} \nls: {args[1]}: {error_message}"
        return f"ls: {error_message}"
    except NotADirectoryError:
        error_message = "Not a directory"
        log_error(error_message)
        if len(args) == 2 and args[0] == '-' and args[1] == 'l':
            return f"ls: {args[0]}: {error_message} \nls: {args[1]}: {error_message}"
        return f"ls: {error_message}"
    except OSError as e:
        error_message = f"OS error: {str(e)}"
        log_error(error_message)
        return f"ls: {error_message}"


def format_no_l(items: list) -> str:
    """
    Форматирует список файлов в колонки.

    :param items: Список имен файлов и директорий.
    :return: Отформатированная строка с элементами, расположенными в колонках.
    """
    if not items:
        return ""

    size = shutil.get_terminal_size()
    width = size.columns

    max_len = max(len(item) for item in items) + 1
    num = max(1, width // max_len)

    result = []
    num_rows = (len(items) + num - 1) // num

    for row in range(num_rows):
        line = []
        for col in range(num):
            idx = row + (col * num_rows)
            if idx < len(items):
                line.append(items[idx].ljust(max_len))
        result.append(''.join(line))

    return '\n'.join(result)


def format_l(item: str, path_verify: str) -> str:
    """
    Форматирует подробную информацию о файле/директории.

    :param item: Имя файла/директории.
    :param path_verify: Абсолютный путь к родительской директории.
    :return: Отформатированная строка с детальной информацией.
    """
    item_path = os.path.join(path_verify, item)

    info = os.stat(item_path)
    permissions = stat.filemode(info.st_mode)
    size = info.st_size
    modificate_time = datetime.fromtimestamp(info.st_mtime).strftime("%b %d %H:%M")
    if os.path.isdir(item_path):
        item_name = f"{item}/"
    else:
        item_name = item

    return f"{permissions} {size} {modificate_time} {item_name}"
