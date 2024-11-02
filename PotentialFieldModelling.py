import tkinter as tk
from tkinter import ttk
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# Функция для расчета потенциальной энергии
def calculate_potential_field(x, y, field_type, params):
    if field_type == "Гравитационное поле":
        G, m1, m2 = params
        U = -G * m1 * m2 / np.sqrt(x ** 2 + y ** 2 + 1e-6)  # Добавляем маленькое значение для избежания деления на ноль
    elif field_type == "Сила упругости":
        k = params[0]
        U = 0.5 * k * (x ** 2 + y ** 2)
    elif field_type == "Степенная функция":
        a, n, b, m = params
        U = a * x ** n + b * y ** m
    else:
        U = np.zeros_like(x)
    return U


# Функция для построения графика
def plot_potential_field():
    # Удаляем старый график, если он существует
    for widget in canvas_frame.winfo_children():
        widget.destroy()

    # Получаем параметры от пользователя
    try:
        field_type = field_type_var.get()
        if field_type == "Гравитационное поле":
            G = float(entry_G.get())
            m1 = float(entry_m1.get())
            m2 = float(entry_m2.get())
            params = (G, m1, m2)
        elif field_type == "Сила упругости":
            k = float(entry_k.get())
            params = (k,)
        elif field_type == "Степенная функция":
            a = float(entry_a.get())
            n = float(entry_n.get())
            b = float(entry_b.get())
            m = float(entry_m.get())
            params = (a, n, b, m)
    except ValueError:
        result_label.config(text="Ошибка: введите корректные значения параметров")
        return

    # Задаем сетку координат
    x = np.linspace(-10, 10, 100)
    y = np.linspace(-10, 10, 100)
    X, Y = np.meshgrid(x, y)
    U = calculate_potential_field(X, Y, field_type, params)

    # Создаем фигуру для отображения на холсте
    fig = Figure(figsize=(6, 5))

    # Контурный график
    ax1 = fig.add_subplot(121)
    cp = ax1.contourf(X, Y, U, cmap="viridis")
    fig.colorbar(cp, ax=ax1)
    ax1.set_title("Контурное распределение U(x, y)")
    ax1.set_xlabel("x")
    ax1.set_ylabel("y")

    # 3D-график
    ax2 = fig.add_subplot(122, projection='3d')
    ax2.plot_surface(X, Y, U, cmap="viridis")
    ax2.set_title("3D график U(x, y)")
    ax2.set_xlabel("x")
    ax2.set_ylabel("y")
    ax2.set_zlabel("U(x, y)")

    # Отображение графика на Tkinter Canvas
    canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)


# Функция для обновления видимости полей ввода параметров
def update_fields(*args):
    field_type = field_type_var.get()
    frame_gravity.grid_remove()
    frame_spring.grid_remove()
    frame_power.grid_remove()
    if field_type == "Гравитационное поле":
        frame_gravity.grid()
    elif field_type == "Сила упругости":
        frame_spring.grid()
    elif field_type == "Степенная функция":
        frame_power.grid()


# Настройка интерфейса tkinter
root = tk.Tk()
root.title("Моделирование потенциального поля")
root.geometry("800x800")

# Выбор типа силы
field_type_var = tk.StringVar()
field_type_var.set("Гравитационное поле")
field_type_var.trace("w", update_fields)

ttk.Label(root, text="Выберите тип силы:").pack(pady=5)
field_type_menu = ttk.OptionMenu(root, field_type_var, "Гравитационное поле", "Гравитационное поле", "Сила упругости",
                                 "Степенная функция")
field_type_menu.pack()

# Параметры для гравитационного поля
frame_gravity = ttk.Frame(root)
ttk.Label(frame_gravity, text="G:").grid(row=0, column=0)
entry_G = ttk.Entry(frame_gravity)
entry_G.grid(row=0, column=1)
ttk.Label(frame_gravity, text="m1:").grid(row=1, column=0)
entry_m1 = ttk.Entry(frame_gravity)
entry_m1.grid(row=1, column=1)
ttk.Label(frame_gravity, text="m2:").grid(row=2, column=0)
entry_m2 = ttk.Entry(frame_gravity)
entry_m2.grid(row=2, column=1)

# Параметры для силы упругости
frame_spring = ttk.Frame(root)
ttk.Label(frame_spring, text="Коэффициент жесткости k:").grid(row=0, column=0)
entry_k = ttk.Entry(frame_spring)
entry_k.grid(row=0, column=1)

# Параметры для степенной функции
frame_power = ttk.Frame(root)
ttk.Label(frame_power, text="Коэффициент a:").grid(row=0, column=0)
entry_a = ttk.Entry(frame_power)
entry_a.grid(row=0, column=1)
ttk.Label(frame_power, text="Степень n для x:").grid(row=1, column=0)
entry_n = ttk.Entry(frame_power)
entry_n.grid(row=1, column=1)
ttk.Label(frame_power, text="Коэффициент b:").grid(row=2, column=0)
entry_b = ttk.Entry(frame_power)
entry_b.grid(row=2, column=1)
ttk.Label(frame_power, text="Степень m для y:").grid(row=3, column=0)
entry_m = ttk.Entry(frame_power)
entry_m.grid(row=3, column=1)

frame_gravity.pack()

# Кнопка для построения графика
btn_plot = ttk.Button(root, text="Построить график", command=plot_potential_field)
btn_plot.pack(pady=10)

# Поле для вывода результата
result_label = ttk.Label(root, text="")
result_label.pack()

# Фрейм для графиков
canvas_frame = ttk.Frame(root)
canvas_frame.pack(fill=tk.BOTH, expand=True)

# Запуск приложения
root.mainloop()
