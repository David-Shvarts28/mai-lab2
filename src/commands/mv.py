import os
import shutil
from src.support.path import absolute_path
from src.support.check import check_path_correct, check_is_dir
from src.support.logger import log_success, log_error, log_command


def mv(*args) -> str:
    """
    Перемещение или переименование файла/каталога.

    :param args: Аргументы команды.
    :return: Возвращает пустую строку или сообщение об ошибке.
    :raises FileNotFoundError: Если источник не существует.
    :raises NotADirectoryError: Если назначение не каталог при множественных источниках.
    :raises PermissionError: Если недостаточно прав доступа.
    :raises OSError: Если произошла ошибка ввода-вывода при работе с файловой системой.
    """
    log_command(f"mv {' '.join(args)}")

    if len(args) < 2:
        error_message = "missing file operand"
        log_error(error_message)
        return f"mv: {error_message}"

    start = args[:-1]
    finish = args[-1]

    try:
        path_finish = check_is_dir(finish)
        is_dir = True
    except (FileNotFoundError, NotADirectoryError) as e:
        if len(start) > 1:
            if isinstance(e, FileNotFoundError):
                error_message = f"'{finish}': No such file or directory"
            else:
                error_message = f"'{finish}' is not a directory"

            log_error(error_message)
            return f"mv: {error_message}"
        else:
            path_finish = absolute_path(finish)
            is_dir = False

    results = []
    for arg in start:
        try:
            path_arg = check_path_correct(arg)

            if is_dir:
                final_dest = os.path.join(path_finish, os.path.basename(path_arg))
            else:
                final_dest = path_finish

            shutil.move(path_arg, final_dest)

        except FileNotFoundError:
            error_message = f"'{arg}': No such file or directory"
            log_error(error_message)
            results.append(f"mv: {error_message}")
        except NotADirectoryError:
            error_message = f"'{arg}': Not a directory"
            log_error(error_message)
            results.append(f"mv: {error_message}")
        except PermissionError:
            error_message = f"'{arg}': Permission denied"
            log_error(error_message)
            results.append(f"mv: {error_message}")
        except OSError as e:
            error_message = f"OS error: {str(e)}"
            log_error(error_message)
            results.append(f"mv: {error_message}")
        except Exception as e:
            error_message = str(e)
            log_error(error_message)
            results.append(f"mv: {error_message}")

    if results:
        return "\n".join(results)
    else:
        log_success("mv", f"moved {len(start)} items to {finish}")
        return ""
