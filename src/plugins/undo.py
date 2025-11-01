import os
import shutil
from src.support.logger import log_success, log_error, log_command

TRASH_DIR = os.path.join(os.getcwd(), ".trash")

def undo() -> str:
    """
    Отмена последней операции удаления.

    :return: Сообщение о результате или ошибке.
    """
    log_command("undo")

    try:

        rest_files = []
        items = os.listdir(TRASH_DIR)

        for item in items:
            path_trash = os.path.join(TRASH_DIR, item)
            path_dest = os.path.join(os.getcwd(), item)

            if os.path.exists(path_dest):
                return f"undo: cannot restore '{item}' - file already exists"

            shutil.move(path_trash, path_dest)
            rest_files.append(item)

        if rest_files:
            success_message = f"restored {len(rest_files)} items"
            log_success("undo", success_message)
            return success_message
        else:
            return "undo: trash is empty"

    except Exception as e:
        error_message = str(e)
        log_error(error_message)
        return f"undo: {error_message}"
