def string_hash(s, table_size):
    hash_value = 0
    for char in s:
        hash_value = (hash_value * 31 + ord(char)) % table_size
    return hash_value


class Dictionary:
    def __init__(self, size=1000):
        self.size = size
        self.table = [[] for _ in range(size)]  # Метод цепочек для разрешения коллизий

    def add(self, word):
        index = string_hash(word, self.size)
        chain = self.table[index]
        if word not in chain:  # дубликаты
            chain.append(word)

    def check(self, word):
        index = string_hash(word, self.size)
        chain = self.table[index]
        return "yes" if word in chain else "no"


def automatic_mode():
    commands = [
        "add hello",
        "add world",
        "check hello",
        "check world",
        "check python",
        "add python",
        "check python"
    ]

    print("\nВыбран автоматический режим. Выполняются команды:")
    for cmd in commands:
        print(f"> {cmd}")

    process_commands(commands)


def manual_mode():
    print("\nВыбран ручной режим. Вводите команды (пустая строка - завершение):")
    print("Доступные команды: add <слово>, check <слово>")

    commands = []
    while True:
        cmd = input("> ").strip()
        if not cmd:
            break
        commands.append(cmd)

    process_commands(commands)


def process_commands(commands):
    dict = Dictionary()
    results = []
    for command in commands:
        parts = command.split()
        if not parts:
            continue
        if parts[0] == "add" and len(parts) > 1:
            dict.add(parts[1])
        elif parts[0] == "check" and len(parts) > 1:
            result = dict.check(parts[1])
            results.append(result)
            print(result)
        else:
            print(f"Неизвестная команда: {command}")

    return results


def main():
    print("Выберите режим ввода:")
    print("1 - Автоматический режим (демонстрация)")
    print("2 - Ручной режим (ввод команд вручную)")

    while True:
        choice = input("Ваш выбор (1 или 2): ").strip()
        if choice == "1":
            automatic_mode()
            break
        elif choice == "2":
            manual_mode()
            break
        else:
            print("Некорректный ввод. Пожалуйста, введите 1 или 2.")


if __name__ == "__main__":
    main()