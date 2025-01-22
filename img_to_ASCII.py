from PIL import Image
from PIL import ImageFilter
from PIL import ImageOps
from PIL import ImageEnhance

# Определяем ASCII-алфавит
ascii_alphabet = [
    "@", "W", "#", "M", "B", "8", "&", "%", "Q", "D", "$", "O", "0", "K", "R", "P",
    "H", "E", "X", "Z", "Y", "G", "U", "N", "S", "5", "A", "V", "4", "2", "6", "9",
    "7", "3", "1", "I", "T", "J", "L", "C", "F", "!", "?", "*", ":", "+", "=", "^",
    "~", "-", "_", ";", ",", ".", "", "'", "\"", "|", "/", "\\", "(", ")", "[", "]",
    "{", "}", "<", ">", " ", " "
]
# Функция для преобразования изображения в ASCII-арт
def image_to_ascii(image_path, cluster_w, output_path):

    # Загружаем изображение и применяем фильтры
    image = Image.open(image_path)
    base_width = cluster_w +50
    wpercent = (base_width / float(image.size[0]))
    hsize = int((float(image.size[1]) * float(wpercent)))
    image = image.resize((base_width, hsize), Image.Resampling.LANCZOS)
    image = image.filter(ImageFilter.SMOOTH)
    
    image = ImageEnhance.Contrast(image).enhance(7)
    image = image.convert("L")  # Переводим в чёрно-белый формат


    width, height = image.size
    aspect_ratio = height / width

    # Рассчитываем размеры ASCII-арта
    cluster_width = width // cluster_w
    cluster_height = int((height // cluster_w) // 0.35)

    # Проверка на минимальный размер кластера
    if cluster_width < 1 or cluster_height < 1:
        raise ValueError("Размеры кластера слишком малы. Увеличьте ширину ASCII-арта.")

    # Определяем размеры результирующей матрицы
    ascii_art = []

    # Разбиваем изображение на кластеры
    for y in range(0, height, cluster_height):
        line = []
        for x in range(0, width, cluster_width):
            # Получаем пиксели текущего кластера
            cluster = image.crop((x, y, x + cluster_width, y + cluster_height))
            pixels = list(cluster.getdata())

            # Рассчитываем среднюю яркость
            avg_brightness = sum(pixels) // len(pixels) if len(pixels) > 0 else 255

            # Нормализуем яркость в диапазоне от 1 до 255
            normalized_brightness = max(1, min(avg_brightness, 255))

            # Сопоставляем яркость с символом из алфавита
            index = (normalized_brightness - 1) * (len(ascii_alphabet) - 1) // 254
            ascii_char = ascii_alphabet[index]
            line.append(ascii_char)

        # Добавляем строку в ASCII-арт
        ascii_art.append("".join(line))

    # Записываем результат в текстовый файл
    with open(output_path, "w", encoding="utf-8") as file:
        for line in ascii_art:
            file.write(line + "\n")

    print(f"ASCII-арт успешно записан в файл {output_path}")

# Пример использования функции
image_to_ascii("/home/tsokurenkosv/pythonProjects/ASCII/img7.jpg", cluster_w=100, output_path="output_ascii_art.txt")