import cv2
import numpy as np
from scipy.signal import medfilt
import matplotlib.pyplot as plt

# Загрузите изображение
image_path = '...'
image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

# Проверьте, успешно ли загружено изображение
if image is None:
    print("Ошибка при загрузке изображения.")
    exit()

# Создайте пустой массив для хранения точек с яркостью > 2
all_points = []

# Проход по вертикальным линиям
for x_coord in range(image.shape[1]):
    # Извлеките значения яркости для вертикальной линии, начиная сверху
    brightness_values = image[:, x_coord]

    # Вычислите производную от зависимости яркости от координаты
    brightness_gradient = np.gradient(brightness_values)

    # Примените медианный фильтр к данным производной
    median_filtered_gradient = medfilt(brightness_gradient, kernel_size=5)  # Измените размер ядра по вашему усмотрению

    # Сформируйте двумерный массив с координатами и значениями медианно отфильтрованной производной
    filtered_gradient_data = np.vstack((np.arange(len(median_filtered_gradient)), median_filtered_gradient)).T

    # Поиск первой точки с яркостью > 2 по модулю, начиная сверху вниз
    threshold = 2
    top_point = None
    for coord, value in filtered_gradient_data:
        if -threshold > value or value > threshold:
            top_point = (x_coord, coord)
            break

    # Поиск первой точки с яркостью > 2 по модулю, начиая снизу вверх
    bottom_point = None
    for coord, value in reversed(filtered_gradient_data):
        if -threshold > value or value > threshold:
            bottom_point = (x_coord, coord)
            break

    # Если найдены точки, добавьте их в общий массив, вместе с яркостью
    if top_point:
        top_brightness = brightness_values[int(top_point[1])]
        all_points.append((int(top_point[0]), int(top_point[1]), top_brightness))

    if bottom_point:
        bottom_brightness = brightness_values[int(bottom_point[1])]
        all_points.append((int(bottom_point[0]), int(bottom_point[1]), bottom_brightness))

# Преобразуйте список точек в массив
all_points = np.array(all_points)

# Извлечь координаты и яркости из массива
x_coordinates = all_points[:, 0]
y_coordinates = all_points[:, 1]
brightness_values = all_points[:, 2]
y_coordinates = np.array(y_coordinates)


def split_array(arr):
    # Инициализируем два пустых массива для результатов
    y_coordinates_up = []
    y_coordinates_botom = []

    # Проходим по элементам входного массива
    for i, element in enumerate(arr):
        # В зависимости от четности индекса добавляем элемент в соответствующий массив
        if i % 2 == 0:
            y_coordinates_up.append(element)
        else:
            y_coordinates_botom.append(element)

    return y_coordinates_up, y_coordinates_botom


# Пример использования
input_array = np.array(y_coordinates)
y_coordinates_up, y_coordinates_botom = split_array(input_array)


def y_coordinates_up_filter(arr):
    # Создаем копию входного массива для изменений
    result = arr.copy()

    # Проходим по элементам массива, начиная с второго и заканчивая предпоследним
    for i in range(1, len(arr) - 1):
        # Вычисляем разницу между текущим элементом и его соседними значениями
        diff_left = abs(arr[i] - arr[i - 1])
        diff_right = abs(arr[i] - arr[i + 1])
        diff_centr = abs(arr[i + 1] - arr[i - 1])

        # Если разница по модулю больше 10, заменяем текущий элемент на среднее значение соседей
        if diff_left > 10 and diff_right > 10 and diff_centr < 5:
            arr[i] = (arr[i - 1] + arr[i + 1]) / 2
        elif diff_left > 10 and diff_right > 10 and diff_centr > 5:
            arr[i] = mean_neighbor = arr[i - 1]
    return arr


# Пример использования
input_array = np.array(y_coordinates_up)
y_coordinates_up_filter = y_coordinates_up_filter(input_array)


def y_coordinates_botom_filter(arr):
    # Создаем копию входного массива для изменений
    result = arr.copy()

    # Проходим по элементам массива, начиная с второго и заканчивая предпоследним
    for i in range(1, len(arr) - 1):
        # Вычисляем разницу между текущим элементом и его соседними значениями
        diff_left = abs(arr[i] - arr[i - 1])
        diff_right = abs(arr[i] - arr[i + 1])
        diff_centr = abs(arr[i + 1] - arr[i - 1])

        # Если разница по модулю больше 10, заменяем текущий элемент на среднее значение соседей
        if diff_left > 10 and diff_right > 10 and diff_centr < 5:
            arr[i] = (arr[i - 1] + arr[i + 1]) / 2
        elif diff_left > 10 and diff_right > 10 and diff_centr > 5:
            arr[i] = arr[i - 1]
    return arr


# Пример использования
input_array = np.array(y_coordinates_botom)
y_coordinates_botom_filter = y_coordinates_botom_filter(input_array)


def combine_arrays(y_coordinates_up_filter, y_coordinates_botom_filter):
    combined_array = []
    max_len = max(len(y_coordinates_up_filter), len(y_coordinates_botom_filter))

    for i in range(max_len):
        if i < len(y_coordinates_up_filter):
            combined_array.append(y_coordinates_up_filter[i])
        if i < len(y_coordinates_botom_filter):
            combined_array.append(y_coordinates_botom_filter[i])

    return combined_array


# Пример использования
y_coordinates_up_filter = np.array(y_coordinates_up_filter)
y_coordinates_botom_filter = np.array(y_coordinates_botom_filter)
y_coordinates_new = combine_arrays(y_coordinates_up_filter, y_coordinates_botom_filter)

# Построение графика в виде точек
plt.scatter(x_coordinates, y_coordinates_new, color='r', marker='o', s=2)
plt.xlabel('Координата X')
plt.ylabel('Координата Y')
plt.grid(True)
plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
plt.axis('off')  # Отключаем оси координат
plt.show()

plt.savefig('my_plot.png')  # Указывайте здесь желаемое имя файла и формат (например, '.png' для PNG-изображения)
