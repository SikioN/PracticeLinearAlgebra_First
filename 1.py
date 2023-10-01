import random

import numpy as np
from sympy import Matrix


# Создаем алфавит
alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя .!?'


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


# Функция для дешифрования сообщения
def decrypt(encrypted_message, key_matrix, n):
    size = key_matrix.shape[0]
    key_matrix_inverse = Matrix(key_matrix).inv_mod(n)
    decrypted_message = ""
    for i in range(0, len(encrypted_message), size):
        block = encrypted_message[i:i + size]
        block_indices = [alphabet.index(char) for char in block]
        decrypted_block_indices = np.dot(key_matrix_inverse, block_indices).astype(int) % len(alphabet)
        decrypted_block = ''.join([alphabet[index] for index in decrypted_block_indices])
        decrypted_message += decrypted_block
    return decrypted_message


# Функция для симуляции вредоносного вмешательства
def simulate_attack(encrypted_message):
    random_indices = random.sample(range(len(encrypted_message)), 3)
    encrypted_list = list(encrypted_message)
    for index in random_indices:
        encrypted_list[index] = random.choice(alphabet)
    return ''.join(encrypted_list)


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

# Симулируем вредоносное вмешательство, заменяя три случайных символа
corrupted_encrypted_message_2x2 = simulate_attack(encrypted_message_2x2)
corrupted_encrypted_message_3x3 = simulate_attack(encrypted_message_3x3)
corrupted_encrypted_message_4x4 = simulate_attack(encrypted_message_4x4)

# Расшифровываем сообщения без вредоносного вмешательства
decrypted_message_2x2 = decrypt(encrypted_message_2x2, key_matrix_2x2, n)
decrypted_message_3x3 = decrypt(encrypted_message_3x3, key_matrix_3x3, n)
decrypted_message_4x4 = decrypt(encrypted_message_4x4, key_matrix_4x4, n)

# Расшифровываем сообщения с вредоносным вмешательством
corrupted_decrypted_message_2x2 = decrypt(corrupted_encrypted_message_2x2, key_matrix_2x2, n)
corrupted_decrypted_message_3x3 = decrypt(corrupted_encrypted_message_3x3, key_matrix_3x3, n)
corrupted_decrypted_message_4x4 = decrypt(corrupted_encrypted_message_4x4, key_matrix_4x4, n)

# Выводим результаты
print("Исходное сообщение:", message)
print("\nЗашифрованное сообщение 2x2:", encrypted_message_2x2)
print("Расшифрованное сообщение 2x2:", decrypted_message_2x2)
print("Зашифрованное испорченное сообщение 2x2:", corrupted_encrypted_message_2x2)
print("Расшифрованное испорченное сообщение 2x2:", corrupted_decrypted_message_2x2)

print("\nЗашифрованное сообщение 3x3:", encrypted_message_3x3)
print("Расшифрованное сообщение 3x3:", decrypted_message_3x3)
print("Зашифрованное испорченное сообщение 3x3:", corrupted_encrypted_message_3x3)
print("Расшифрованное испорченное сообщение 3x3:", corrupted_decrypted_message_3x3)

print("\nЗашифрованное сообщение 4x4:", encrypted_message_4x4)
print("Расшифрованное сообщение 4x4:", decrypted_message_4x4)
print("Зашифрованное испорченное сообщение 4x4:", corrupted_encrypted_message_4x4)
print("Расшифрованное испорченное сообщение 4x4:", corrupted_decrypted_message_4x4)
