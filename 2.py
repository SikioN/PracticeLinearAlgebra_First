import numpy as np


# Функция для генерации случайной матрицы-ключа
def generate_key_matrix(size, n):
    while True:
        key_matrix = np.random.randint(n, size=(size, size))
        det = int(np.round(np.linalg.det(key_matrix))) % n
        return key_matrix


# Функция для шифрования сообщения
def encrypt(message, key_matrix, n):
    size = key_matrix.shape[0]
    encrypted_message = ""
    for i in range(0, len(message), size):
        block = message[i:i + size]
        block_indices = [alphabet.index(char) for char in block]
        encrypted_block_indices = np.dot(key_matrix, block_indices) % len(alphabet)
        encrypted_block = ''.join([alphabet[index] for index in encrypted_block_indices])
        encrypted_message += encrypted_block
    return encrypted_message


# Создаем алфавит
alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя .!?'

# Исходное сообщение
message = "абвгдеёжзийк"

# Генерируем ключи разных размеров
n = len(alphabet)
key_matrix_2x2 = generate_key_matrix(2, n)

# Шифруем сообщение с каждым ключом
encrypted_message_2x2 = encrypt(message, key_matrix_2x2, n)

print(encrypted_message_2x2)


def split_message(message, block_size):
    return [message[i:i + block_size] for i in range(0, len(message), block_size)]


# Исходное сообщение и зашифрованное сообщение
message = "абвгдеёжзийк"
encrypted_message_2x2 = "ёязцйнлен пч"

# Алфавит
alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя .!?'
n = len(alphabet)

# Разбиваем исходное и зашифрованное сообщения на блоки
message_blocks = split_message(message, 2)
encrypted_blocks = split_message(encrypted_message_2x2, 2)

# Создание ключевых матриц для каждого блока
key_matrices = []
for i in range(len(message_blocks)):
    M_indices = [alphabet.index(char) for char in message_blocks[i]]
    C_indices = [alphabet.index(char) for char in encrypted_blocks[i]]

    # Создание матрицы M и C из индексов символов
    M = np.array(M_indices).reshape(2, 1)
    C = np.array(C_indices).reshape(2, 1)

    # Найдите обратную матрицу M^-1
    M_inv = np.linalg.inv(M)

    # Найдите ключевую матрицу K = M^-1 * C
    K = np.dot(M_inv, C) % n
    key_matrices.append(K)

print("Ключевые матрицы K для каждого блока:")
for i, K in enumerate(key_matrices):
    print(f"Блок {i + 1}:\n{K}")