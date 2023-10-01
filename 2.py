import numpy as np
import sympy
from sympy import Matrix


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


# Функция разбивающая исходное и зашифрованное сообщения на списки индексов пар символов
def split_message(message, alphabet):
    index_list = []
    for char1, char2 in zip(message[::2], message[1::2]):
        index1 = alphabet.index(char1)
        index2 = alphabet.index(char2)
        index_list.append([index1, index2])
    return index_list


if __name__ == '__main__':

    # Создаем алфавит
    alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя .!?'

    # Исходное сообщение
    message = "абвгдеёжзийк"

    # Сообщение, которое мы хотим расшифровать
    text = ""
    # Количество символово в сообщение
    k = 12
    while True:
        text = input("Введите сообщение из >= 12 символов: ")
        k -= (12 - len(text))
        text = text.ljust(12)
        if len(text) == 12:
            break
        else:
            print("Повторите попытку. Кажется, вы неверно ввели сообщение")

    n = len(alphabet)

    # Создаём ключ матрицу, чтобы зашифровать сообщения
    key_matrix = generate_key_matrix(2, n)

    # Шифруем сообщение с неизвестным ключом
    encrypted_message_2x2 = encrypt(message, key_matrix, n)

    # Перезаписываем значение на зашифрованное
    text = encrypt(text, key_matrix, n)

    # Обнуляем матрицу
    key_matrix = Matrix([[0, 0], [0, 0]])

    # Разбиваем исходное и зашифрованное сообщения на списки
    original_indices = split_message(message, alphabet)
    encrypted_indices = split_message(encrypted_message_2x2, alphabet)

    # Решение матричного уравнения
    for i in range(0, len(original_indices), 2):
        X = sympy.Matrix(
            [[original_indices[i][0], original_indices[i + 1][0]],
             [original_indices[i][1], original_indices[i + 1][1]]])
        _X = sympy.Matrix([[encrypted_indices[i][0], encrypted_indices[i + 1][0]],
                           [encrypted_indices[i][1], encrypted_indices[i + 1][1]]])

        X = X.inv_mod(len(alphabet))

        A = _X * X % n
        if decrypt(encrypted_message_2x2, A, n) == message:
            key_matrix = A
            break

    print(decrypt(text, key_matrix, n))