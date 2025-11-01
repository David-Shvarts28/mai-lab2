import os
from tarfile import open
from src.support.path import absolute_path
from src.support.check import check_is_dir
from src.support.logger import log_success, log_error, log_command


def tar_func(*args) -> str:
    """
    Создание TAR.GZ архива.

    :param args: Аргументы команды.
    :return: Сообщение о результате или ошибке.
    :raises FileNotFoundError: Если папка не существует.
    :raises NotADirectoryError: Если источник не является каталогом.
    :raises OSError: Если произошла ошибка ввода-вывода при работе с файловой системой.
    """
    log_command(f"tar {' '.join(args)}")

    if len(args) < 2:
        error_message = "missing tar operand"
        log_error(error_message)
        return f"tar: {error_message}"

    folder, archive_tar = args[0], args[1]
    try:
        path_folder = check_is_dir(folder)
        path_archive = absolute_path(archive_tar)

        with open(path_archive, "w:gz") as tar:
            tar.add(path_folder, arcname=os.path.basename(path_folder))


    except NotADirectoryError:
        error_message = f"'{folder}': Not a directory"
        log_error(error_message)
        return f"tar: {error_message}"
    except FileNotFoundError:
        error_message = f"'{folder}': No such file or directory"
        log_error(error_message)
        return f"tar: {error_message}"
    except OSError as e:
        error_message = f"OS error: {str(e)}"
        log_error(error_message)
        return f"tar: {error_message}"
    except Exception as e:
        error_message = str(e)
        log_error(error_message)
        return f"tar: {error_message}"

    success_message = f"created {archive_tar} from {folder}"
    log_success("tar", success_message)
    return success_message
