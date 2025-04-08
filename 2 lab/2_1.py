import random
import time

# Узел АВЛ-дерева
class AVLNode:
    def __init__(self, key):
        self.key = key
        self.height = 1
        self.left = None
        self.right = None

# АВЛ-дерево
class AVLTree:
    def __init__(self):
        self.root = None

    def insert(self, root, key):
        if not root:
            return AVLNode(key)
        elif key < root.key:
            root.left = self.insert(root.left, key)
        elif key > root.key:
            root.right = self.insert(root.right, key)
        else:
            return root  # исключение для дубликатов

        root.height = 1 + max(self.get_height(root.left),
                              self.get_height(root.right))

        balance = self.get_balance(root)

        if balance > 1 and key < root.left.key:
            return self.right_rotate(root)

        if balance < -1 and key > root.right.key:
            return self.left_rotate(root)

        if balance > 1 and key > root.left.key:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)

        if balance < -1 and key < root.right.key:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root

    def search(self, root, key):
        if not root:
            return False
        if key == root.key:
            return True
        elif key < root.key:
            return self.search(root.left, key)
        else:
            return self.search(root.right, key)

    def left_rotate(self, z):
        y = z.right
        T2 = y.left

        y.left = z
        z.right = T2

        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))

        return y

    def right_rotate(self, z):
        y = z.left
        T3 = y.right

        y.right = z
        z.left = T3

        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))

        return y

    def get_height(self, node):
        return node.height if node else 0

    def get_balance(self, node):
        return self.get_height(node.left) - self.get_height(node.right) if node else 0

    def add(self, key):
        self.root = self.insert(self.root, key)

    def contains(self, key):
        return self.search(self.root, key)

def main():
    NUM_ELEMENTS = 10**5
    RANGE_MIN = -10**6
    RANGE_MAX = 10**6

    print(f"Генерация {NUM_ELEMENTS} случайных чисел...")
    data = random.sample(range(RANGE_MIN, RANGE_MAX), NUM_ELEMENTS)

    print("Запись в список и дерево...")
    vector = []
    tree = AVLTree()

    start_insert = time.time()
    for number in data:
        vector.append(number)
        tree.add(number)
    end_insert = time.time()
    print(f"Запись завершена за {end_insert - start_insert:.2f} секунд.")


    print(f"Генерация еще {NUM_ELEMENTS} чисел для поиска...")
    search_data = [random.randint(RANGE_MIN, RANGE_MAX) for _ in range(NUM_ELEMENTS)]

    print("Проверка наличия в списке и дереве...")
    start_check = time.time()
    in_vector = sum(1 for num in search_data if num in vector)
    in_tree = sum(1 for num in search_data if tree.contains(num))
    end_check = time.time()

    print(f"Найдено в списке: {in_vector}")
    print(f"Найдено в дереве: {in_tree}")
    print(f"Проверка завершена за {end_check - start_check:.2f} секунд.")

    # Поиск только в дереве
    print("Проверка только в дереве...")
    start_tree_only = time.time()
    in_tree_only = sum(1 for num in search_data if tree.contains(num))
    end_tree_only = time.time()

    print(f"Найдено в дереве: {in_tree_only}")
    print(f"Проверка только в дереве заняла {end_tree_only - start_tree_only:.2f} секунд.")

    print("\n📊 Сравнение времени:")
    print(f"- Вставка в дерево и список: {end_insert - start_insert:.2f} сек")
    print(f"- Поиск в списке и дереве: {end_check - start_check:.2f} сек")
    print(f"- Только поиск в дереве: {end_tree_only - start_tree_only:.2f} сек")


if __name__ == "__main__":
    main()
