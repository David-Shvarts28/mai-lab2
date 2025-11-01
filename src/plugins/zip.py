import os
from zipfile import ZipFile
from src.support.path import absolute_path
from src.support.check import check_is_dir
from src.support.logger import log_success, log_error, log_command


def zip_func(*args) -> str:
    """
    Создание ZIP архива из каталога.

    :param args: Аргументы команды.
    :return: Сообщение о результате
    :raises FileNotFoundError: Если указанный путь не существует.
    :raises NotADirectoryError: Если указанный путь ведет к файлу.
    :raises OSError: Если произошла ошибка ввода-вывода при работе с файловой системой.
    """
    log_command(f"zip {' '.join(args)}")

    if len(args) < 2:
        error_message = "missing zip operand"
        log_error(error_message)
        return f"zip: {error_message}"


    folder, archive = args[0], args[1]
    try:
        folder_path = check_is_dir(folder)
        archive_path = absolute_path(archive)

        with ZipFile(archive_path, 'w') as myzip:
            for path, name, filenames in os.walk(folder_path):
                for filename in filenames:
                    file_path = os.path.join(path, filename)
                    arcname = os.path.relpath(file_path, folder_path)
                    myzip.write(file_path, arcname)

    except NotADirectoryError:
        error_message = f"'{folder}': Not a directory"
        log_error(error_message)
        return f"zip: {error_message}"
    except FileNotFoundError:
        error_message = f"'{folder}': No such file or directory"
        log_error(error_message)
        return f"zip: {error_message}"
    except OSError as e:
        error_message = f"OS error: {str(e)}"
        log_error(error_message)
        return f"zip: {error_message}"
    except Exception as e:
        error_message = str(e)
        log_error(error_message)
        return f"zip: {error_message}"

    success_message = f"created {archive} from {folder}"
    log_success("zip", success_message)
    return success_message
