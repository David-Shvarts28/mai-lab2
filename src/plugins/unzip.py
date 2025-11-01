import os
from zipfile import ZipFile, BadZipFile
from src.support.check import check_path_correct
from src.support.logger import log_success, log_error, log_command


def unzip_func(*args) -> str:
    """
    Распаковка ZIP архива.

    :param args: Аргументы команды.
    :return: Сообщение о результате
    :raises FileNotFoundError: Если указанный путь не существует.
    :raises BadZipFile: Если файл не является ZIP архивом.
    :raises OSError: Если произошла ошибка ввода-вывода при работе с файловой системой.
    """
    log_command(f"unzip {' '.join(args)}")

    if len(args) != 1:
        error_message = "too many arguments"
        log_error(error_message)
        return f"unzip: {error_message}"

    archive = args[0]

    try:
        path_archive = check_path_correct(archive)

        archive_name = os.path.splitext(os.path.basename(archive))[0]
        extract_dir = archive_name

        os.makedirs(extract_dir, exist_ok=True)

        with ZipFile(path_archive, 'r') as myzip:
            myzip.extractall(path=extract_dir)

        success_message = f"extracted {archive} to {extract_dir}"
        log_success(f"unzip: {success_message}")
        return f"unzip: {success_message}"

    except BadZipFile:
        error_message = f"'{archive}' is not a zip archive"
        log_error(error_message)
        return f"unzip: {error_message}"
    except FileNotFoundError:
        error_message = f"'{archive}': No such file or directory"
        log_error(error_message)
        return f"unzip: {error_message}"
    except OSError as e:
        error_message = f"OS error: {str(e)}"
        log_error(error_message)
        return f"unzip: {error_message}"
    except Exception as e:
        error_message = f"unexpected error: {str(e)}"
        log_error(error_message)
        return f"unzip: {error_message}"
