import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

# Створення головного вікна

# root = tk.Tk()
root = ttk.Window(themename="flatly")

root.title("Приклад Tkinter")
root.geometry("%dx%d" % (1280, 832))

style = ttk.Style()
style.configure("TFrame", background="#7D8A8B")  # #D3D3D3 - сірий колір

# Створюємо контейнер з іншим фоном
frame = ttk.Frame(root, style="TFrame", padding=10, width=550)
frame.pack(fill=Y, side=LEFT, padx=16, pady=10)  # Відступ 16px зліва
frame.pack_propagate(False)
# Додаємо кнопки, текстові поля, слайдери до контейнера
button = ttk.Button(frame, text="Button")
button.pack(pady=5)

entry = ttk.Entry(frame)
entry.pack(pady=5)

slider = ttk.Scale(frame, from_=0, to=100, orient=HORIZONTAL)
slider.pack(pady=5)

# Додаємо дропдаун меню (Combobox)
dropdown = ttk.Combobox(frame, values=["Option 1", "Option 2", "Option 3"])
dropdown.pack(pady=5)
dropdown.current(0)  # Вибираємо перший елемент за замовчуванням

root.mainloop()