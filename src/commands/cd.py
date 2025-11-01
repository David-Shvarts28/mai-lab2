import os
from src.support.check import check_is_dir
from src.support.logger import log_success, log_error, log_command


def cd(*args) -> str:
    """
    Смена текущей директории.

    :param args: Аргументы команды.
    :return: Возвращает пустую строку или сообщение об ошибке.
    :raises FileNotFoundError: Если путь не существует
    :raises NotADirectoryError: Если путь ведет к файлу
    :raises OSError: Если произошла ошибка ввода-вывода при работе с файловой системой.
    """
    try:
        log_command(f"cd {' '.join(args)}")

        if len(args) > 1:
            error_message = "too many arguments"
            log_error(error_message)
            return f"cd: {error_message}"

        elif len(args) == 0:
            path = '~'
        else:
            path = args[0]
        path_verify = check_is_dir(path)
        os.chdir(path_verify)
        log_success("cd", f"changed to {path_verify}")
        return ""

    except FileNotFoundError:
        error_message = "No such file or directory"
        log_error(error_message)
        return f"cd: {error_message}: {path}"

    except NotADirectoryError:
        error_message = "Not a directory"
        log_error(error_message)
        return f"cd: {error_message}: {path}"

    except OSError as e:
        error_message = f"OS error: {str(e)}"
        log_error(error_message)
        return f"cd: {error_message}"
