import os
import shutil
from src.support.path import verify_path_for_rm
from src.support.check import check_path_correct
from src.support.logger import log_success, log_error, log_command

TRASH_DIR = os.path.join(os.getcwd(), ".trash")


def rm(*args) -> str:
    """
    Удаляет файлы или директории.

    :param args: Цели для удаления + опции
    :return: Возвращает пустую строку или сообщение об ошибке.
    :raises FileNotFoundError: Если источник не существует.
    :raises PermissionError: Если недостаточно прав доступа.
    """
    log_command(f"rm {' '.join(args)}")

    if len(args) == 0:
        error_message = "missing operand"
        log_error(error_message)
        return f"rm: {error_message}"

    if args[0] == '-r':
        remove_list = args[1:]
    else:
        remove_list = args

    if len(remove_list) == 0:
        error_message = "missing operand"
        log_error(error_message)
        return f"rm: {error_message}"

    errors = []

    for arg in remove_list:
        try:
            if verify_path_for_rm(arg):
                path = check_path_correct(arg)

                if not os.path.exists(TRASH_DIR):
                    os.makedirs(TRASH_DIR)

                if os.path.isdir(path):
                    if args[0] == '-r':
                        agree = input(f"rm: remove directory '{arg}'? (y/n): ")
                        if agree.lower() in ['yes', 'y']:
                            trash_path = os.path.join(TRASH_DIR, os.path.basename(path))
                            shutil.move(path, trash_path)
                            log_success("rm", f"remove directory {arg}")
                        else:
                            error_message = "Forbidden operation"
                            log_error(error_message)
                            return f"rm: {error_message}"
                    else:
                        error_message = "Is a directory"
                        log_error(error_message)
                        errors.append(f"rm: cannot remove '{arg}': {error_message}")
                else:
                    trash_path = os.path.join(TRASH_DIR, os.path.basename(path))
                    shutil.move(path, trash_path)
                    log_success("rm", f"remove file {arg}")
            else:
                error_message = "Operation not permitted"
                log_error(error_message)
                errors.append(f"rm: cannot remove '{arg}': {error_message}")

        except FileNotFoundError:
            error_message = f"'{arg}': No such file or directory"
            log_error(error_message)
            errors.append(f"rm: {error_message}")
        except PermissionError:
            error_message = f"'{arg}': Permission denied"
            log_error(error_message)
            errors.append(f"rm: {error_message}")
        except Exception as e:
            error_message = str(e)
            log_error(error_message)
            errors.append(f"rm: {error_message}")

    if errors:
        return "\n".join(errors)
    else:
        return ""
