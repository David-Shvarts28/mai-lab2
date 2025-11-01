import os
from src.support.logger import log_command, log_error, log_success

def load_history() -> list:
    """
    Загрузка истории команд из файла .history.

    :return: Список ранее выполненных команд.
    """
    if os.path.exists(".history"):
        with open(".history", 'r') as f:
            return [line.strip() for line in f.readlines()]
    return []

command_history = load_history()


def history(*args) -> str:
    """
    Вывод истории выполненных команд.

    :param args: Количество отображаемых команд(опционально).
    :return: Строка с историей команд или сообщение об ошибке.
    """
    log_command(f"history {' '.join(args)}")

    try:
        n = len(command_history)
        if args:
            if len(args) > 1:
                return "history: too many arguments"
            if not args[0].isdigit():
                return "history: numeric argument required"
            n = int(args[0])
            if n <= 0:
                return "history: argument must be greater than 0"

        if len(command_history) == 0:
            return "history: no commands in history"

        back_commands = command_history[-n:]
        first_num = len(command_history) - len(back_commands) + 1

        result = []
        for i, j in enumerate(back_commands, first_num):
            result.append(f"{i}  {j}")

        log_success("history", f"show history from {n} command")
        return "\n".join(result)

    except Exception as e:
        error_msg = f"history: unexpected error: {str(e)}"
        log_error(error_msg)
        return error_msg


def add_history(command: str) -> None:
    """
    Добавление команды в историю и сохранение в файл.

    :param command: Команда для добавления в историю.
    :return: None
    """
    if command.strip() and command != 'exit':
        command_history.append(command)
        with open(".history", 'w') as f:
            for command in command_history:
                f.write(command + '\n')
