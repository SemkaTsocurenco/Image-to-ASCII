import cv2
import os
from PIL import Image
from PIL import ImageFilter
from PIL import ImageEnhance
from PIL import  ImageOps

# Определяем ASCII-алфавит
ascii_alphabet = [
    "@", "W", "#", "M", "B", "8", "&", "%", "Q", "D", "$", "O", "0", "K", "R", "P",
    "H", "E", "X", "Z", "Y", "G", "U", "N", "S", "5", "A", "V", "4", "2", "6", "9",
    "7", "3", "1", "I", "T", "J", "L", "C", "F", "!", "?", "*", ":", "+", "=", "^",
    "~", "-", "_", ";", ",", ".", "", "'", "\"", "|", "/", "\\", "(", ")", "[", "]",
    "{", "}", "<", ">", " ", " "
]

# Функция для преобразования изображения в ASCII-арт
def frame_to_ascii(frame, cluster_w):
    # Преобразуем кадр в изображение PIL
    image = Image.fromarray(frame)
    
    base_width = cluster_w + 150
    wpercent = (base_width / float(image.size[0]))
    hsize = int((float(image.size[1]) * float(wpercent)))
    image = image.resize((base_width, hsize), Image.Resampling.LANCZOS)
    
    image = image.filter(ImageFilter.SMOOTH)
    image = ImageEnhance.Contrast(image).enhance(5)
    image = image.convert("L")
    
    width, height = image.size
    cluster_width = width // cluster_w
    cluster_height = int((height // cluster_w) // 0.35)
    image = ImageOps.invert(image)
    
    if cluster_width < 1 or cluster_height < 1:
        raise ValueError("Размеры кластера слишком малы. Увеличьте ширину ASCII-арта.")

    ascii_art = []
    for y in range(0, height, cluster_height):
        line = []
        for x in range(0, width, cluster_width):
            cluster = image.crop((x, y, x + cluster_width, y + cluster_height))
            pixels = list(cluster.getdata())
            avg_brightness = sum(pixels) // len(pixels) if len(pixels) > 0 else 255
            normalized_brightness = max(1, min(avg_brightness, 255))
            index = (normalized_brightness - 1) * (len(ascii_alphabet) - 1) // 254
            ascii_char = ascii_alphabet[index]
            line.append(ascii_char)

        ascii_art.append("".join(line))

    return ascii_art

# Функция для обработки видео и вывода ASCII-арта в консоль
def video_to_ascii(video_path, cluster_w):
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print("Не удалось открыть видео.")
        return

    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Меняем размер фрейма и преобразуем его в ASCII-арт
            ascii_art = frame_to_ascii(frame, cluster_w)

            # Очищаем терминал
            os.system("clear" if os.name == "posix" else "cls")

            # Выводим ASCII-арт
            for line in ascii_art:
                print(line)

            # Задержка для контроля частоты кадров (30 FPS)
            cv2.waitKey(33)

    finally:
        cap.release()
        cv2.destroyAllWindows()

# Пример использования функции
video_to_ascii("/home/tsokurenkosv/pythonProjects/ASCII/videoplayback.mp4", cluster_w=175)

