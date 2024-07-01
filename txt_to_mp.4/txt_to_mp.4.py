import os
import matplotlib.pyplot as plt
import imageio.v2 as imageio

# Путь к папке с текстовыми файлами
input_folder = "..."
output_video_folder = "..."

# Папка для сохранения изображений
output_folder = "..."
os.makedirs(output_folder, exist_ok=True)

# Список файлов в папке
files = os.listdir(input_folder)
files = [f for f in files if f.endswith(".txt")]

# Создание списка для хранения всех изображений
images = []

# Проход по каждому файлу
for i, file in enumerate(files):
    if i % 5 != 0:
        continue  # Рассматриваем только каждый пятый файл

    # Чтение данных из файла
    with open(os.path.join(input_folder, file), "r") as f:
        data = f.readlines()
    data = [line.strip().split() for line in data]
    X = [float(row[0]) for row in data]
    Y = [float(row[1]) for row in data]
    
    # Границы расчётной области
    c = 1500 

    # Создание графика
    plt.figure()
    plt.scatter(X, Y, color='blue', s=0.5)  # Точки из файла
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title(file)

    # Set the limits of the plot
    plt.xlim(0, c)
    plt.ylim(0, c)
    plt.autoscale(False)

    # Сохранение графика в виде изображения
    output_path = os.path.join(output_folder, file.replace(".txt", ".png"))
    plt.savefig(output_path)

    # Добавление изображения в список для создания видео
    images.append(imageio.imread(output_path))

    # Закрытие текущего графика
    plt.close()

# Путь для сохранения видео
video_path = os.path.join(output_video_folder, "название_видео.mp4")

# Создание видео из списка изображений
imageio.mimsave(video_path, images, fps=60)  # fps - количество кадров в секунду

print("Видео успешно сохранено:", video_path)
