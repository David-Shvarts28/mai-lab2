from src.support.check import check_is_file
from src.support.logger import log_success, log_error, log_command


def cat(*args) -> str:
    """
    Выводит содержимое файла.

    :param args: Аргументы команды.
    :return: Содержимое файла.
    :raises FileNotFoundError: Если путь не существует.
    :raises IsADirectoryError: Если путь ведет к папке.
    :raises OSError: Если произошла ошибка ввода-вывода при работе с файловой системой.
    """
    log_command(f"cat {' '.join(args)}")

    if len(str(args)) == 0:
        error_message = "missing file operand"
        log_error(error_message)
        return f"cat: {error_message}"

    result = []
    files_read = 0
    errors = []

    for file in args:
        try:
            path = check_is_file(file)
            with open(path, "r") as text:
                value = text.read()
            result.append(value)
            files_read += 1

        except FileNotFoundError:
            error_message = "No such file or directory"
            log_error(error_message)
            errors.append(f"cat: {file}: {error_message}")
        except IsADirectoryError:
            error_message = "Is a directory"
            log_error(error_message)
            errors.append(f"cat: {file}: {error_message}")
        except OSError as e:
            error_message = f"OS error: {str(e)}"
            log_error(error_message)
            errors.append(f"cat: {file}: {error_message}")

    res = "\n".join(result)
    if errors:
        res += "\n" + "\n".join(errors)
    log_success("cat", f"read {files_read} files")
    return res
