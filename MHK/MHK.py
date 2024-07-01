import numpy as np
import matplotlib.pyplot as plt

# Координаты точек по оси X и Y
x = np.array([0.4, 1.6, 2.8, 3.9])
y = np.array([1.9, 2.4, 3.2, 3.4])

# Вычисление коэффициентов для линейной аппроксимации методом наименьших квадратов
A = np.vstack([x, np.ones(len(x))]).T
m, c = np.linalg.lstsq(A, y, rcond=None)[0]

# Построение графика точек и аппроксимирующей прямой
plt.plot(x, m*x + c, 'r', label='линейная аппроксимация')
plt.plot(x[0], y[0], 'o', label='первая точка')
plt.plot(x[1], y[1], 'o', label='вторая точка')
plt.plot(x[2], y[2], 'o', label='третья точка')
plt.plot(x[3], y[3], 'o', label='четвёртая точка')


# Добавление уравнения аппроксимирующей прямой на график
plt.text(1.5, 2, f'Уравнение прямой: y = {m:.2f}x + {c:.2f}', fontsize=12)

# Настройка графика
plt.xlabel('XXX')
plt.ylabel('YYY')
plt.title('текст текст текст')
plt.legend()
plt.grid(True)

# Отображение графика
plt.show()
