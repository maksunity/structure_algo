def calc(expr):
    def priority(op):
        if op in ('+', '-'):
            return 1
        if op in ('*', '/'):
            return 2
        return 0

    def apply_op(a, b, op):
        if op == '+':
            return a + b
        if op == '-':
            return a - b
        if op == '*':
            return a * b
        if op == '/':
            if b == 0:
                raise ZeroDivisionError("Деление на ноль.")
            return a // b  # целочислено

    def to_tokens(s):
        tokens = []
        num = ''
        for ch in s:
            if ch.isdigit() or (ch == '-' and (not tokens or tokens[-1] in '()+-*/')):
                num += ch
            elif ch.isalpha() and len(ch) == 1:
                if num:
                    tokens.append(num)
                    num = ''
                tokens.append(ch)
            else:
                if num:
                    tokens.append(num)
                    num = ''
                if ch in '+-*/()':
                    tokens.append(ch)
        if num:
            tokens.append(num)
        return tokens

    def evaluate(tokens, var_values):
        values = []
        ops = []

        def process():
            try:
                b = values.pop()
                a = values.pop()
                op = ops.pop()
                values.append(apply_op(a, b, op))
            except IndexError:
                raise ValueError("Ошибка в расстановке скобок или операциях.")

        i = 0
        while i < len(tokens):
            token = tokens[i]
            if token.isdigit() or (token.startswith('-') and token[1:].isdigit()):
                values.append(int(token))
            elif token.isalpha():
                if token not in var_values:
                    raise ValueError(f"Переменная '{token}' не задана.")
                values.append(var_values[token])
            elif token == '(':
                ops.append(token)
            elif token == ')':
                while ops and ops[-1] != '(':
                    process()
                if not ops:
                    raise ValueError("Несбалансированные скобки.")
                ops.pop()
            elif token in '+-*/':
                while ops and ops[-1] != '(' and priority(ops[-1]) >= priority(token):
                    process()
                ops.append(token)
            i += 1

        while ops:
            if ops[-1] == '(' or ops[-1] == ')':
                raise ValueError("Несбалансированные скобки.")
            process()

        return values[0]

    # Разбор выражения
    expr = expr.replace(' ', '')
    tokens = to_tokens(expr)

    # Поиск переменных
    variables = sorted(set(tok for tok in tokens if tok.isalpha()))
    var_values = {}

    for var in variables:
        while True:
            try:
                value = int(input(f"Введите значение переменной '{var}': "))
                var_values[var] = value
                break
            except ValueError:
                print("Ошибка: введите целое число.")

    try:
        result = evaluate(tokens, var_values)
        print(f"Результат: {result}")
    except Exception as e:
        print("Ошибка при вычислении:", e)

def main():
    print("Выберите способ ввода:")
    print("1. Ввести выражение вручную")
    print("2. Использовать встроенное выражение")

    choice = input("Ваш выбор (1/2): ").strip()
    if choice == '1':
        expression = input("Введите выражение: ")
    else:
        expression = "3 + x * (2 + y) - z" # Ранее заготовленное выражение

    calc(expression)


if __name__ == "__main__":
    main()
