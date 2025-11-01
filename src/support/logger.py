import logging

def logger() -> logging.Logger:
    """
    Создание базовой конфигурации для логирования.

    :return: Объект логгера с настроенной конфигурацией
    """
    logging.basicConfig(filename='../shell.log',
                        encoding='utf-8',
                        format='[%(asctime)s] %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        level=logging.DEBUG)

    return logging.getLogger("Shell-Logger")


shell_logger = logger()


def log_command(user_input: str) -> None:
    """
    Запись команды в файл логирования.

    :param user_input: Строка с командой пользователя
    :return: None
    """
    shell_logger.debug(user_input)


def log_error(error_message: str) -> None:
    """
    Запись ошибки в файл логирования.

    :param error_message: Строка с сообщением об ошибке
    :return: None
    """
    shell_logger.error(f"ERROR: {error_message}")


def log_success(operation: str, details: str = "") -> None:
    """
    Запись успешной операции в файл логирования.

    :param operation: Название выполненной операции
    :param details: Дополнительные детали операции (опционально)
    :return: None
    """
    if details:
        shell_logger.info(f"SUCCESS: {operation} - {details}")
    else:
        shell_logger.info(f"SUCCESS: {operation}")
