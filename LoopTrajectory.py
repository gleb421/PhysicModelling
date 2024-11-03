import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk

def plot_trajectory():
    # Заданные параметры
    m = 3  # кг
    mu = 0.03
    R = 3  # м
    alpha = np.pi + (np.pi / 6)  # 4π/3 радиан

    # Ускорение свободного падения
    g = 9.8  # м/с^2

    # Вычисление начальной скорости (из предыдущего решения)
    v0_squared = 2 * g * R * (7/4 - mu * (np.sqrt(3)/2))
    v0 = np.sqrt(v0_squared)

    # Скорость в точке отрыва от дуги
    v_alpha = np.sqrt(g * R / 2)

    # Координаты точки отрыва
    cos_alpha = np.cos(alpha)
    sin_alpha = np.sin(alpha)
    x0 = R * sin_alpha
    y0 = R * (1 - cos_alpha)

    # Компоненты скорости в точке отрыва
    phi = alpha + (np.pi / 2)
    v_x = v_alpha * np.cos(phi)
    v_y = v_alpha * np.sin(phi)

    # Время полета для построения траектории
    t_flight = (-v_y - np.sqrt(v_y**2 + 2 * g * y0)) / (-g)
    t = np.linspace(0, t_flight, 100)

    # Уравнения траектории после отрыва
    x_traj = x0 + v_x * t
    y_traj = y0 + v_y * t - 0.5 * g * t**2

    # Координаты дуги
    theta_arc = np.linspace(0, alpha, 100)
    x_arc = R * np.sin(theta_arc)
    y_arc = R * (1 - np.cos(theta_arc))

    # Создание графика
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(x_arc, y_arc, label='Путь по дуге', color='blue')
    ax.plot(x_traj, y_traj, label='Траектория после отрыва', color='red')
    ax.scatter([x0], [y0], color='green', label='Точка отрыва')
    ax.set_xlabel('x (м)')
    ax.set_ylabel('y (м)')
    ax.set_title('Траектория тела после отрыва от дуги')
    ax.legend()
    ax.grid(True)
    ax.axis('equal')

    # Вставка графика в интерфейс
    canvas = FigureCanvasTkAgg(fig, master=window)  # Создание объекта canvas
    canvas.draw()
    canvas.get_tk_widget().pack()

# Создание главного окна
window = tk.Tk()
window.title("Мертвая петля")
window.geometry("800x600")

# Кнопка для построения графика
plot_button = tk.Button(window, text="Построить траекторию", command=plot_trajectory)
plot_button.pack()

# Запуск главного цикла
window.mainloop()
