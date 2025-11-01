import shlex
from commands.ls import ls #type: ignore
from commands.cd import cd #type: ignore
from commands.cat import cat #type: ignore
from commands.cp import cp #type: ignore
from commands.mv import mv #type: ignore
from commands.rm import rm #type: ignore
from plugins.zip import zip_func #type: ignore
from plugins.unzip import unzip_func #type: ignore
from plugins.tar import tar_func #type: ignore
from plugins.untar import untar_func #type: ignore
from plugins.grep import grep_func #type: ignore
from plugins.history import history #type: ignore
from plugins.undo import undo #type: ignore


commands = {
    'ls': ls,
    'cd': cd,
    'cat': cat,
    'cp': cp,
    'mv': mv,
    'rm': rm,
    'zip': zip_func,
    'unzip': unzip_func,
    'tar': tar_func,
    'untar': untar_func,
    'history': history,
    'undo': undo,
    'grep': grep_func

}

def parse(command: str) -> list:
    """
    Разбирает строку команды и выполняет её.

    :param command: Полная строка команды от пользователя
    :return: Список (успех, сообщение)
    """
    if len(command.split()) == 0:
        return [True, ""]
    block = shlex.split(command)
    args = block[1:]
    command_name = block[0]

    if command_name in commands:
        try:
            res = commands[command_name](*args)
            return [True, res]
        except Exception as e:
            return [False, str(e)]
    else:
        return [False, f"Команда '{command_name}' не найдена"]
