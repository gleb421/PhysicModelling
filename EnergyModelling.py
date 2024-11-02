import tkinter as tk
from tkinter import ttk
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# Функция для численного решения ОДУ методом Рунге-Кутты 4-го порядка
def runge_kutta_4th_order(f, y0, t, args=()):
    n = len(t)
    y = np.zeros((n, len(y0)))
    y[0] = y0
    dt = t[1] - t[0]

    for i in range(1, n):
        k1 = f(t[i - 1], y[i - 1], *args)
        k2 = f(t[i - 1] + dt / 2, y[i - 1] + dt / 2 * np.array(k1), *args)
        k3 = f(t[i - 1] + dt / 2, y[i - 1] + dt / 2 * np.array(k2), *args)
        k4 = f(t[i - 1] + dt, y[i - 1] + dt * np.array(k3), *args)

        y[i] = y[i - 1] + (dt / 6) * (np.array(k1) + 2 * np.array(k2) + 2 * np.array(k3) + np.array(k4))

    return y


# Функция для вычисления производных (модель колебания груза на пружине с сопротивлением)
def spring_oscillation(t, y, m, k, b):
    x, v = y
    dxdt = v
    dvdt = -k / m * x - b / m * v
    return [dxdt, dvdt]


# Функция для расчета энергий
def calculate_energies(m, k, y):
    x = y[:, 0]
    v = y[:, 1]
    kinetic_energy = 0.5 * m * v ** 2
    potential_energy = 0.5 * k * x ** 2
    total_energy = kinetic_energy + potential_energy
    return kinetic_energy, potential_energy, total_energy


# Функция для построения графиков
def plot_energies():
    try:
        # Получаем параметры из полей ввода
        m = float(entry_mass.get())
        k = float(entry_k.get())
        b = float(entry_b.get())
    except ValueError:
        result_label.config(text="Ошибка: введите корректные значения параметров")
        return

    # Начальные условия: начальная координата (смещение) и скорость
    x0 = 1.0
    v0 = 0.0
    y0 = [x0, v0]

    # Время моделирования
    t_span = (0, 20)
    t_eval = np.linspace(t_span[0], t_span[1], 500)

    # Решение ОДУ методом Рунге-Кутты 4-го порядка
    y_solution = runge_kutta_4th_order(spring_oscillation, y0, t_eval, args=(m, k, b))

    # Вычисление энергий
    kinetic_energy, potential_energy, total_energy = calculate_energies(m, k, y_solution)

    # Создаем графики
    fig = Figure(figsize=(8, 6))
    ax1 = fig.add_subplot(311)
    ax1.plot(t_eval, kinetic_energy, label="Кинетическая энергия", color="blue")
    ax1.set_ylabel("Энергия (Дж)")
    ax1.legend()

    ax2 = fig.add_subplot(312)
    ax2.plot(t_eval, potential_energy, label="Потенциальная энергия", color="orange")
    ax2.set_ylabel("Энергия (Дж)")
    ax2.legend()

    ax3 = fig.add_subplot(313)
    ax3.plot(t_eval, total_energy, label="Полная энергия", color="green")
    ax3.set_xlabel("Время (с)")
    ax3.set_ylabel("Энергия (Дж)")
    ax3.legend()

    # Отображение графика на Tkinter Canvas
    for widget in canvas_frame.winfo_children():
        widget.destroy()

    canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)


# Настройка интерфейса tkinter
root = tk.Tk()
root.title("Энергетические превращения при колебании груза на пружине")
root.geometry("800x800")

# Ввод массы груза
ttk.Label(root, text="Масса груза (кг):").pack(pady=5)
entry_mass = ttk.Entry(root)
entry_mass.pack()

# Ввод коэффициента жесткости пружины
ttk.Label(root, text="Коэффициент жесткости пружины k (Н/м):").pack(pady=5)
entry_k = ttk.Entry(root)
entry_k.pack()

# Ввод коэффициента сопротивления
ttk.Label(root, text="Коэффициент сопротивления b (кг/с):").pack(pady=5)
entry_b = ttk.Entry(root)
entry_b.pack()

# Кнопка для построения графиков
btn_plot = ttk.Button(root, text="Построить графики", command=plot_energies)
btn_plot.pack(pady=10)

# Поле для вывода результата
result_label = ttk.Label(root, text="")
result_label.pack()

# Фрейм для графиков
canvas_frame = ttk.Frame(root)
canvas_frame.pack(fill=tk.BOTH, expand=True)

# Запуск приложения
root.mainloop()
