from datetime import datetime


def parse_date(date_str):
    for fmt in ['%d.%m.%Y', '%d/%m/%Y']:
        try:
            return datetime.strptime(date_str, fmt).date()
        except ValueError:
            continue
    return None


def parse_price(price_str):
    try:
        return float(price_str.replace(',', '.'))
    except ValueError:
        return None


def parse_order_line(line):
    line = line.strip()
    if not line:
        return None
    for sep in [' ', ',', ';']:
        if sep in line:
            parts = [p.strip() for p in line.split(sep) if p.strip()]
            if len(parts) >= 3:
                break
    else:
        return None

    date, name, price = None, None, None

    for part in parts:
        d = parse_date(part)
        if d:
            date = d
            parts.remove(part)
            break

    for part in parts:
        p = parse_price(part)
        if p is not None:
            price = p
            parts.remove(part)
            break

    name = ' '.join(parts).strip('"\'')

    if date and name and price is not None:
        return date, name, price
    return None


def process_orders(filename):
    pizza_counts = {}
    date_totals = {}
    max_order = None
    total_orders = 0
    total_price = 0.0

    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            order = parse_order_line(line)
            if not order:
                continue

            date, name, price = order

            pizza_counts[name] = pizza_counts.get(name, 0) + 1

            date_totals[date] = date_totals.get(date, 0.0) + price

            if max_order is None or price > max_order[2]:
                max_order = (date, name, price)

            total_orders += 1
            total_price += price

    return {
        'pizza_counts': pizza_counts,
        'date_totals': date_totals,
        'max_order': max_order,
        'total_orders': total_orders,
        'total_price': total_price
    }


def print_statistics(stats):
    #Список пицц по популярности
    print("а) Список пицц по популярности:")
    for name, count in sorted(stats['pizza_counts'].items(), key=lambda x: (-x[1], x[0])):
        print(f"{name} - {count}")

    #Суммарная стоимость по дням
    print("\nб) Суммарная стоимость по дням:")
    for date, total in sorted(stats['date_totals'].items()):
        print(f"{date.strftime('%d.%m.%Y')} {total:.2f}")

    #Самый дорогой заказ
    if stats['max_order']:
        date, name, price = stats['max_order']
        print(f"\nв) {date.strftime('%d.%m.%Y')} {name} {price:.2f}")

    #Средняя стоимость заказа
    if stats['total_orders'] > 0:
        avg = stats['total_price'] / stats['total_orders']
        print(f"\nг) {avg:.2f}")


def main():
    filename = "pizza.txt"
    # filename = "Lab01_task3_input.txt"
    try:
        stats = process_orders(filename)
        print_statistics(stats)
    except FileNotFoundError:
        print("Файл не найден!")
    except Exception as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()