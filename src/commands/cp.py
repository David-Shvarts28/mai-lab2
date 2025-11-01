import os
import shutil
from src.support.path import absolute_path
from src.support.check import check_path_correct, check_is_dir
from src.support.logger import log_success, log_error, log_command


def cp(*args) -> str:
    """
    Копирование файла/каталога.

    :param args: Аргументы команды.
    :return: Возвращает пустую строку или сообщение об ошибке.
    :raises FileNotFoundError: Если источник не существует.
    :raises NotADirectoryError: Если путь ведет к файлу.
    :raises PermissionError: Если недостаточно прав доступа.
    :raises OSError: Если произошла ошибка ввода-вывода при работе с файловой системой.
    """
    log_command(f"cp {' '.join(args)}")

    if len(args) < 2:
        error_message = "missing file operand"
        log_error(error_message)
        return f"cp: {error_message}"

    if args[0] == '-r':
        recursive = True
        start = args[1:-1]
    else:
        recursive = False
        start = args[:-1]
    finish = args[-1]

    if len(start) == 0:
        error_message = "missing file operand"
        log_error(error_message)
        return f"cp: {error_message}"

    try:
        path_finish = check_is_dir(finish)
        is_dir_finish = True
    except (FileNotFoundError, NotADirectoryError):
        if len(start) > 1:
            error_message = f"'{finish}' is not a directory"
            log_error(error_message)
            return f"cp: {error_message}"
        path_finish = absolute_path(finish)
        is_dir_finish = False

    results = []
    for arg in start:
        try:
            path_arg = check_path_correct(arg)

            if is_dir_finish:
                final_dest = os.path.join(path_finish, os.path.basename(path_arg))
            else:
                final_dest = path_finish

            if os.path.isdir(path_arg):
                if recursive:
                    if os.path.exists(final_dest):
                        shutil.rmtree(final_dest)
                    shutil.copytree(path_arg, final_dest)
                else:
                    message = f"no correct directory '{arg}'"
                    log_error(message)
                    results.append(f"cp: -r not specified; {message}")
            else:
                shutil.copy2(path_arg, final_dest)

        except FileNotFoundError:
            error_message = f"'{arg}': No such file or directory"
            log_error(error_message)
            results.append(f"cp: {error_message}")
        except PermissionError:
            error_message = f"'{arg}': Permission denied"
            log_error(error_message)
            results.append(f"cp: {error_message}")
        except Exception as e:
            error_message = f"'{arg}': {str(e)}"
            log_error(error_message)
            results.append(f"cp: {error_message}")
        except OSError as e:
            error_message = f"OS error: {str(e)}"
            log_error(error_message)
            results.append(f"cp: {error_message}")

    if results:
        return "\n".join(results)
    else:
        log_success("cp", f"copied {len(start)} items to {finish}")
        return ""
