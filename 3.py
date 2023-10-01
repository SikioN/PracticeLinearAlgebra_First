import numpy as np
import random


# Функция для кодирования слова из 4 букв
def word_to_bit(word):
    if len(word) != 4:
        raise ValueError("Слово должно состоять из 4 букв")
    encoded_word = ''
    for char in word:
        encoded_word += binary_dict[char]
    return encoded_word


def encode_word(encoded_input_list, G):
    encoded_list = []
    for i in range(len(encoded_input_list)):
        res = np.dot(G, encoded_input_list[i]) % 2
        encoded_list.append(res)
    return encoded_list


# Симуляция вмешательства
def simulate_error(encoded_word, n):
    # Случайно выбираем два индекса для инвертирования битов
    corrupted_text = []
    count = n
    for c in encoded_word:
        text = "".join(str(_) for _ in (c.T).tolist()[0])
        error_indices = random.sample(range(len(text)), 1 if count > 0 else 0)
        count -= 1 if count > 0 else 0
        corrupted_word = list(text)
        for index in error_indices:
            corrupted_word[index] = '1' if corrupted_word[index] == '0' else '0'
        corrupted_text.append(''.join(corrupted_word))

    corrupted = [np.array(list(map(int, c))).reshape(7, 1) for c in corrupted_text]

    return corrupted


# Декодирование испорченного слова
def decode_word(encoded_input_list, H):
    decode_list = []
    for encoded_message in encoded_input_list:
        # Вычислиение синдром
        encoded_message = (encoded_message.T).tolist()[0]
        syndrome = np.dot(H, encoded_message) % 2

        # Определите позицию ошибки
        error_position = 0
        for i in range(3):
            if np.array_equal(syndrome, H[i]):
                error_position = i + 1
                break

        # Исправление ошибки, если она есть
        if error_position > 0:
            encoded_message[error_position - 1] = (encoded_message[error_position - 1] + 1) % 2

        # Извлечение информационных битов
        decoded_message = np.array([encoded_message[2], encoded_message[4], encoded_message[5], encoded_message[6]])
        decode_list.append("".join([str(c) for c in decoded_message.tolist()]))

    return decode_list


def binary_to_letters(binary_word, alphabet):
    binary_word = "".join(binary_word)
    binary = [binary_word[i: i + 5] for i in range(0, len(binary_word), 5)]
    output = ""
    for bit in binary:
        output += alphabet[bit]
    return output


# Сопоставление букв русского алфавита пятибитовым двоичным номерам
alphabet = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'
binary_dict = {}
binary_dict_rev = {}

for i, char in enumerate(alphabet):
    binary_dict[char] = format(i, '05b')
    binary_dict_rev[format(i, '05b')] = char

# Создание матриц G и H для кода Хэмминга (7, 4)
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

if __name__ == '__main__':
    # Выбор и кодирование слова
    input_word = "тест"
    bit_input = word_to_bit(input_word)
    bit_input_list = [np.array(list(map(int, bit_input[i:i + 4]))).reshape(4, 1) for i in range(0, len(bit_input), 4)]
    print(f"Исходное слово '{input_word}' в двоичной форме: {bit_input}")

    # Шифрование слова
    encode = encode_word(bit_input_list, G)

    # Количество испорченных битов
    n = 1
    corrupted_word = simulate_error(encode, n)

    decoded_word = decode_word(corrupted_word, H)
    print(f"Декодированное слово после исправления ошибок: {decoded_word}")

    # Переводим декодированное слово обратно в буквы
    decoded_letters = binary_to_letters(decoded_word, binary_dict_rev)
    print(f"Декодированное слово в буквах: {decoded_letters}")
