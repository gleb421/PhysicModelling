import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import messagebox


class ElectrostaticFieldApp:
    def __init__(self, master):
        self.master = master
        master.title("Визуализация электростатического поля")

        # Заголовок
        self.label_info = tk.Label(master, text="Введите параметры зарядов (x, y, q):")
        self.label_info.pack(pady=5)

        # Поле для ввода зарядов
        self.entry_charges = tk.Entry(master, width=50)
        self.entry_charges.insert(0, "-1,0,1e-9; 1,0,-1e-9")  # Значения по умолчанию
        self.entry_charges.pack(pady=5)

        # Кнопка запуска
        self.button = tk.Button(master, text="Построить поле", command=self.run_simulation)
        self.button.pack(pady=10)

        # Поле для графика
        self.figure, self.ax = plt.subplots(figsize=(6, 5))
        self.canvas = FigureCanvasTkAgg(self.figure, master)
        self.canvas.get_tk_widget().pack(pady=5)

    def run_simulation(self):
        try:
            # Чтение и обработка данных из ввода
            charges_input = self.entry_charges.get()
            charges = []
            for charge_str in charges_input.split(";"):
                x, y, q = map(float, charge_str.split(","))
                charges.append((x, y, q))
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректные данные: x,y,q; x,y,q ...")
            return

        # Построение электростатического поля
        self.plot_field(charges)

    def plot_field(self, charges):
        # Константы
        k = 8.99e9  # Константа Кулона (Н·м²/Кл²)

        # Сетка точек
        x = np.linspace(-2, 2, 50)
        y = np.linspace(-2, 2, 50)
        X, Y = np.meshgrid(x, y)

        # Инициализация векторов поля
        Ex = np.zeros(X.shape)
        Ey = np.zeros(Y.shape)

        # Вычисление электростатического поля
        for cx, cy, q in charges:
            dx = X - cx
            dy = Y - cy
            r_squared = dx**2 + dy**2
            r = np.sqrt(r_squared)

            # Избегаем деления на ноль
            r_squared[r_squared == 0] = np.inf
            r[r == 0] = np.inf

            Ex += k * q * dx / r_squared
            Ey += k * q * dy / r_squared

        # Нормализация для визуализации
        E = np.sqrt(Ex**2 + Ey**2)
        Ex /= E
        Ey /= E

        # Очистка предыдущего графика
        self.ax.clear()

        # Построение векторного поля
        self.ax.quiver(X, Y, Ex, Ey, E, cmap='viridis', scale=20, pivot='middle')

        # Рисуем заряды
        for cx, cy, q in charges:
            if q > 0:
                self.ax.plot(cx, cy, 'ro', markersize=10, label=f'+{q*1e9:.1f} нКл')
            else:
                self.ax.plot(cx, cy, 'bo', markersize=10, label=f'{q*1e9:.1f} нКл')

        # Эквипотенциальные линии
        V = np.zeros(X.shape)
        for cx, cy, q in charges:
            r = np.sqrt((X - cx)**2 + (Y - cy)**2)
            r[r == 0] = np.inf
            V += k * q / r

        self.ax.contour(X, Y, V, levels=20, cmap='cool', alpha=0.7)

        # Настройки графика
        self.ax.set_title("Электростатическое поле точечных зарядов")
        self.ax.set_xlabel("X (м)")
        self.ax.set_ylabel("Y (м)")
        self.ax.axhline(0, color='black', linewidth=0.5)
        self.ax.axvline(0, color='black', linewidth=0.5)
        self.ax.grid()

        # Обновление графика
        self.canvas.draw()


if __name__ == "__main__":
    root = tk.Tk()
    app = ElectrostaticFieldApp(root)
    root.mainloop()
