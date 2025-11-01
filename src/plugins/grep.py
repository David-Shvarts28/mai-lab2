import os
import re
from src.support.logger import log_success, log_error, log_command


def grep_func(*args) -> str:
    """
    Поиск строк в файлах по шаблону.

    :param args: Аргументы команды.
    :return: Результаты поиска или сообщение об ошибке.
    :raises FileNotFoundError: Если указанный путь не существует.
    :raises OSError: Если произошла ошибка ввода-вывода при работе с файловой системой.
    :raises UnicodeDecodeError: Если файл имеет бинарный формат и не может быть прочитан как текст.

    """
    log_command(f"grep {' '.join(args)}")

    if len(args) < 2:
        error_message = "missing operand"
        log_error(error_message)
        return f"grep: {error_message}"

    pattern = args[0]
    path = args[1]

    try:
        if '-i' in args:
            flags = re.IGNORECASE
        else:
            flags = 0 #type: ignore
        reg = re.compile(pattern, flags)
    except re.error:
        error_message = "invalid pattern"
        log_error(error_message)
        return f"grep: {error_message}"

    results = []
    errors = []

    if os.path.isfile(path):
        try:
            with open(path, 'r', encoding='utf-8') as folder:
                for num, line in enumerate(folder, 1):
                    if reg.search(line):
                        results.append(f"{path}:{num}:{line.strip()}")
        except FileNotFoundError:
            error_message = "No such file or directory"
            log_error(error_message)
            return f"grep: {path}: {error_message}"
        except UnicodeDecodeError:
            error_message = "Binary file"
            log_error(error_message)
            return f"grep: {path}: {error_message}"
        except OSError as e:
            error_message = f"OS error: {str(e)}"
            log_error(error_message)
            return f"grep: {path}: {error_message}"

    elif os.path.isdir(path):
        if '-r' in args:
            for r, dirs, files in os.walk(path):
                for file in files:
                    file_path = os.path.join(r, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as folder:
                            for num, line in enumerate(folder, 1):
                                if reg.search(line):
                                    results.append(f"{file_path}:{num}:{line.strip()}")
                    except (UnicodeDecodeError, OSError) as e:
                        errors.append(f"grep: {file_path}: {str(e)}")
        else:
            error_message = "is a directory"
            log_error(error_message)
            return f"grep: {path}: {error_message}"

    else:
        error_message = "no such file or directory"
        log_error(error_message)
        return f"grep: {path}: {error_message}"

    output = []
    if results:
        output.extend(results)
    if errors:
        output.extend(errors)

    if output:
        log_success("grep", f"found {len(results)} matches")
        return "\n".join(output)
    else:
        log_success("grep", "no matches found")
        return ""
