import random
import sympy

# Алфавит и ключевая матрица размером 2x2
alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя .!?'


# Функция для генерации случайной ключевой матрицы
def generate_random_key_matrix(n):
    while True:
        # Генерируем случайную матрицу 2x2 с элементами в диапазоне [1, n-1]
        key_matrix = sympy.Matrix([[random.randint(1, n - 1), random.randint(1, n - 1)],
                                   [random.randint(1, n - 1), random.randint(1, n - 1)]])
        # Проверяем, что определитель не имеет общих делителей с n
        determinant = key_matrix.det()
        if sympy.gcd(determinant, n) == 1:
            return key_matrix


# Генерируем случайное n, так чтобы gcd(alphabet_length, n) = 1
alphabet_length = len(alphabet)
n = random.randint(alphabet_length + 1, alphabet_length * 10)

# Генерируем случайную ключевую матрицу
original_key_matrix = generate_random_key_matrix(n)


# Функция для шифрования сообщения
def encrypt(message, key_matrix):
    encrypted_message = ""
    for i in range(0, len(message), 2):
        pair = message[i:i + 2]
        if len(pair) == 2:
            pair_matrix = sympy.Matrix([[alphabet.index(pair[0]), alphabet.index(pair[1])]])
            result_matrix = (pair_matrix * key_matrix) % len(alphabet)
            encrypted_pair = "".join([alphabet[result_matrix[0, 0]], alphabet[result_matrix[0, 1]]])
            encrypted_message += encrypted_pair
    return encrypted_message


# Функция для дешифрования сообщения и поиска ключевой матрицы
def decrypt_and_find_key(encrypted_message, original_key_matrix):
    decrypted_message = ""
    key_matrix = sympy.MatrixSymbol('key_matrix', 2, 2)
    equations = []
    for i in range(0, len(encrypted_message), 2):
        pair = encrypted_message[i:i + 2]
        if len(pair) == 2:
            pair_matrix = sympy.Matrix([[alphabet.index(pair[0]), alphabet.index(pair[1])]])
            result_matrix = (pair_matrix * key_matrix) % len(alphabet)
            decrypted_pair = "".join([alphabet[result_matrix[0, 0]], alphabet[result_matrix[0, 1]]])
            decrypted_message += decrypted_pair
            # Добавляем уравнения для решения системы
            equations.append(result_matrix - pair_matrix)

    # Решаем систему уравнений для нахождения ключевой матрицы
    solution = sympy.solve(equations, key_matrix)
    found_key_matrix = solution[key_matrix]

    return decrypted_message, found_key_matrix


# Генерация случайного сообщения из 12 символов
random.seed(123)  # Для воспроизводимости результатов
random_message = ''.join(random.choice(alphabet) for _ in range(12))

# Шифрование сообщения с использованием ключевой матрицы
encrypted_message = encrypt(random_message, original_key_matrix)


def decrypt_and_find_key(encrypted_message, original_key_matrix):
    decrypted_message = ""
    inverse_original_key_matrix = original_key_matrix.inv_mod(len(alphabet))
    for i in range(0, len(encrypted_message), 2):
        pair = encrypted_message[i:i + 2]
        if len(pair) == 2:
            pair_matrix = sympy.Matrix([[alphabet.index(pair[0]), alphabet.index(pair[1])]])
            result_matrix = (pair_matrix * inverse_original_key_matrix) % len(alphabet)
            decrypted_pair = "".join([alphabet[result_matrix[0, 0]], alphabet[result_matrix[0, 1]]])
            decrypted_message += decrypted_pair
    return decrypted_message, inverse_original_key_matrix



print(f"Исходное сообщение: {random_message}")
print(f"Зашифрованное сообщение: {encrypted_message}")




# Дешифрование и поиск ключевой матрицы
decrypted_message, found_key_matrix = decrypt_and_find_key(encrypted_message, original_key_matrix)
print(f"Дешифрованное сообщение: {decrypted_message}")
print(f"Найденная ключевая матрица: {found_key_matrix}")
