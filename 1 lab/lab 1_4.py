def read_input_from_file(filename):
    with open(filename, 'r') as file:
        participants = file.readline().strip().split()

        n = int(file.readline())
        expenses = {name: 0 for name in participants}
        for _ in range(n):
            name, amount = file.readline().strip().split()
            expenses[name] += int(amount)

    return participants, expenses


def calculate_transfers(participants, expenses):
    total = sum(expenses.values())
    average = total / len(participants)

    balances = []
    for name in participants:
        balance = expenses[name] - average
        balances.append((name, balance))

    # Сортировка по балансу (от меньшего к большему)
    balances.sort(key=lambda x: x[1])

    transfers = []
    left = 0
    right = len(balances) - 1

    while left < right:
        debtor, debt = balances[left]
        creditor, credit = balances[right]

        amount = min(-debt, credit)
        if amount > 0.0001:  # погрешность
            transfers.append((debtor, creditor, round(amount, 2)))

        balances[left] = (debtor, debt + amount)
        balances[right] = (creditor, credit - amount)

        if abs(balances[left][1]) < 0.0001:
            left += 1
        if abs(balances[right][1]) < 0.0001:
            right -= 1

    return transfers


def main():
    try:
        participants, expenses = read_input_from_file('friends.txt')
    except FileNotFoundError:
        print("Файл friends.txt не найден!")
        return
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return

    transfers = calculate_transfers(participants, expenses)

    print(len(transfers))
    for transfer in transfers:
        print(f"{transfer[0]} {transfer[1]} {transfer[2]:.2f}")


if __name__ == "__main__":
    main()