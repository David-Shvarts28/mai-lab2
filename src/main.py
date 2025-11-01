from src.support.logger import log_error
from src.parser import parse
from plugins.history import add_history #type: ignore


def main() -> None:
    """
    Является точкой входа в приложение.

    :return: Данная функция ничего не возвращает
    """
    print("Hello, type 'exit' to quit.")
    while True:
        try:
            command = input("%")
            if command.strip() and command != 'exit' and 'history' not in command:
                add_history(command)
            if command.strip() == 'exit':
                print("Goodbye!")
                break
            if not command.strip():
                continue
            success, result = parse(command)
            if success:
                if result:
                    print(result)
            else:
                log_error(result)
                print(f"Error: {result}")
        except Exception as e:
            log_error(f"Unexpected error: {str(e)}")
            print(f"Unexpected error: {str(e)}")


if __name__ == "__main__":
    main()
