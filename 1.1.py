import random
from sympy import Matrix, symbols, mod_inverse

# Создаем алфавит
alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя .!?'

# Функция для генерации случайной матрицы-ключа
def generate_key_matrix(size, n):
    while True:
        key_matrix = Matrix(size, size, lambda i, j: random.randint(0, n - 1))
        det = key_matrix.det() % n
        if det != 0 and mod_inverse(det, n) is not None:
            return key_matrix

# Функция для шифрования сообщения
def encrypt(message, key_matrix, n):
    size = key_matrix.rows
    encrypted_message = ""
    for i in range(0, len(message), size):
        block = message[i:i + size]
        block_indices = [alphabet.index(char) for char in block]
        block_vector = Matrix(block_indices)
        encrypted_block_vector = (key_matrix * block_vector).applyfunc(lambda x: x % len(alphabet))
        encrypted_block = ''.join([alphabet[index] for index in encrypted_block_vector.tolist()])
        encrypted_message += encrypted_block
    return encrypted_message

# Функция для дешифрования сообщения
def decrypt(encrypted_message, key_matrix, n):
    size = key_matrix.rows
    key_matrix_inverse = key_matrix.inv_mod(n)
    decrypted_message = ""
    for i in range(0, len(encrypted_message), size):
        block = encrypted_message[i:i + size]
        block_indices = [alphabet.index(char) for char in block]
        block_vector = Matrix(block_indices)
        decrypted_block_vector = (key_matrix_inverse * block_vector).applyfunc(lambda x: x % len(alphabet))
        decrypted_block = ''.join([alphabet[index] for index in decrypted_block_vector.tolist()])
        decrypted_message += decrypted_block
    return decrypted_message

# Исходное сообщение
message = "это лаба пла"

# Генерируем ключи разных размеров
n = len(alphabet)
key_matrix_2x2 = generate_key_matrix(2, n)
key_matrix_3x3 = generate_key_matrix(3, n)
key_matrix_4x4 = generate_key_matrix(4, n)

# Шифруем сообщение с каждым ключом
encrypted_message_2x2 = encrypt(message, key_matrix_2x2, n)
encrypted_message_3x3 = encrypt(message, key_matrix_3x3, n)
encrypted_message_4x4 = encrypt(message, key_matrix_4x4, n)

# Расшифровываем сообщения
decrypted_message_2x2 = decrypt(encrypted_message_2x2, key_matrix_2x2, n)
decrypted_message_3x3 = decrypt(encrypted_message_3x3, key_matrix_3x3, n)
decrypted_message_4x4 = decrypt(encrypted_message_4x4, key_matrix_4x4, n)

# Выводим результаты
print("Исходное сообщение:", message)
print("\nЗашифрованное сообщение 2x2:", encrypted_message_2x2)
print("Расшифрованное сообщение 2x2:", decrypted_message_2x2)

print("\nЗашифрованное сообщение 3x3:", encrypted_message_3x3)
print("Расшифрованное сообщение 3x3:", decrypted_message_3x3)

print("\nЗашифрованное сообщение 4x4:", encrypted_message_4x4)
print("Расшифрованное сообщение 4x4:", decrypted_message_4x4)
