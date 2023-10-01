import random
import numpy as np

# Шаг 1: Создать словарь для букв русского алфавита (32 символа) и их двоичных кодов
alphabet = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
binary_dict = {}
for i, char in enumerate(alphabet):
    binary_code = bin(i)[2:].zfill(5)
    binary_dict[char] = binary_code

# Шаг 2: Закодировать слово "нуль"
word = "нуль"
binary_word = ''.join([binary_dict[char] for char in word])
binary_word = binary_word.ljust(20, '0')

# Шаг 3: Создать матрицу G и матрицу H для кода Хэмминга (7, 4)
G = np.array([[1, 1, 0, 1],
              [1, 0, 1, 1],
              [1, 0, 0, 0],
              [0, 1, 1, 1],
              [0, 1, 0, 0],
              [0, 0, 1, 0],
              [0, 0, 0, 1]])

H = np.array([[1, 0, 1, 0, 1, 0, 1],
              [0, 1, 1, 0, 0, 1, 1],
              [0, 0, 0, 1, 1, 1, 1]])

# Шаг 4: Закодировать слово "нуль" с помощью матрицы G
encoded_word = np.dot(np.array(list(binary_word), dtype=int), G) % 2


# Шаг 5: Симулировать вредоносное вмешательство
def introduce_errors(encoded_word, num_errors):
    error_indices = random.sample(range(len(encoded_word)), num_errors)
    corrupted_word = encoded_word.copy()
    for index in error_indices:
        corrupted_word[index] = 1 - encoded_word[index]
    return corrupted_word


corrupted_word = introduce_errors(encoded_word, 1)

# Шаг 6: Декодировать и исправить ошибки с использованием матрицы H
syndrome = np.dot(corrupted_word, H.T) % 2
error_position = sum([syndrome[i] * 2 ** i for i in range(3)]) - 1
if error_position >= 0:
    corrupted_word[error_position] = 1 - corrupted_word[error_position]

# Шаг 7: Перевести результат в слово из 4 букв
decoded_word = ''.join([binary_word[i:i + 5] for i in range(0, len(binary_word), 5)])
print(f"Закодированное слово: {binary_word}")
print(f"Исходное слово: {word}")
print(f"Раскодированное слово: {decoded_word}")
