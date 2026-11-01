import prompt


def print_commands():
    """Печатает список доступных команд."""
    print("<command> exit - выйти из программы")
    print("<command> help - справочная информация")


def welcome():
    """Приветствует пользователя и запрашивает команды."""
    print("Первая попытка запустить проект!")
    print()
    print("***")
    print_commands()
    while True:
        command = prompt.string("Введите команду: ")
        if command == "exit":
            break
        if command == "help":
            print_commands()