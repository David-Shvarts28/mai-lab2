import os
import tarfile
from src.support.check import check_path_correct
from src.support.logger import log_success, log_error, log_command


def untar_func(*args) -> str:
    """
    Распаковка TAR архива в папку с именем архива.

    :param args: Аргументы команды.
    :return: Сообщение о результате или ошибке.
    :raises FileNotFoundError: Если архив не существует.
    :raises TarError: Если файл не является TAR архивом.
    :raises OSError: При ошибках файловой системы.
    """
    log_command(f"untar {' '.join(args)}")

    if len(args) != 1:
        error_message = "untar: exactly one archive expected"
        log_error(error_message)
        return error_message

    archive = args[0]

    try:

        path_archive = check_path_correct(archive)

        archive_name = os.path.splitext(os.path.basename(archive))[0]
        extract_dir = archive_name

        with tarfile.open(path_archive, 'r:*') as tar:
            tar.extractall(path=".")

        log_success("untar", f"extracted {archive} to {extract_dir}")
        return f"extracted {archive} to {extract_dir}"

    except tarfile.TarError:
        error_message = f"'{archive}' is not a tar archive"
        log_error(error_message)
        return f"untar: {error_message}"
    except FileNotFoundError:
        error_message = f"'{archive}': No such file or directory"
        log_error(error_message)
        return f"untar: {error_message}"
    except OSError as e:
        error_message = f"OS error: {str(e)}"
        log_error(error_message)
        return f"untar: {error_message}"
    except Exception as e:
        error_message = f"unexpected error: {str(e)}"
        log_error(error_message)
        return f"untar: {error_message}"
