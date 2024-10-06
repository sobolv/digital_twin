import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from datetime import datetime


# Function to draw example graphs for Tab 1 (you can replace it with your graph logic)
def draw_graphs(canvas_list):
    fig, axs = plt.subplots(3, 1, figsize=(5, 8))

    for i, ax in enumerate(axs):
        ax.plot([1, 2, 3], [i + 1, i + 2, i + 3])
        ax.set_title(f"Graph {i + 1}")

    for i, canvas in enumerate(canvas_list):
        canvas.draw()


# Function to validate input from Tab 2 and draw the chart
def validate_and_draw_chart(date1, date2, hour1, minute1, hour2, minute2, error_label, canvas):
    try:
        datetime.strptime(date1.get(), '%m/%d/%y')
        datetime.strptime(date2.get(), '%m/%d/%y')
        if not (0 <= int(hour1.get()) <= 23 and 0 <= int(hour2.get()) <= 23):
            raise ValueError("Hour must be between 0 and 23.")
        if not (0 <= int(minute1.get()) <= 59 and 0 <= int(minute2.get()) <= 59):
            raise ValueError("Minutes must be between 0 and 59.")

        error_label.config(text="")

        # Replace this with your chart plotting logic
        fig, ax = plt.subplots(figsize=(5, 5))
        ax.plot([1, 2, 3], [int(hour1.get()), int(minute1.get()), int(hour2.get())])
        canvas.figure = fig
        canvas.draw()

    except Exception as e:
        error_label.config(text=str(e))


# Main window setup
root = tk.Tk()
root.title("Tkinter Layout with Tabs")

# Notebook for tabs
notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill='both')

# Tab 1 setup
tab1 = ttk.Frame(notebook)
notebook.add(tab1, text="Tab 1")

# Split pane for Tab 1
pane1 = ttk.PanedWindow(tab1, orient=tk.HORIZONTAL)
pane1.pack(fill='both', expand=True)

# Left container (inputs and sliders)
left_container1 = ttk.Frame(pane1, width=200)
left_container1.pack_propagate(False)
pane1.add(left_container1)

for i in range(5):
    tk.Label(left_container1, text=f"Input {i + 1}").pack(pady=5)
    tk.Entry(left_container1).pack(pady=5)

for i in range(3):
    tk.Label(left_container1, text=f"Slider {i + 1}").pack(pady=5)
    tk.Scale(left_container1, from_=0, to=100, orient=tk.HORIZONTAL).pack(pady=5)

# Right container (matplotlib graphs)
right_container1 = ttk.Frame(pane1)
pane1.add(right_container1)

canvas_list = []
for i in range(3):
    fig, ax = plt.subplots(figsize=(5, 2))
    canvas = FigureCanvasTkAgg(fig, master=right_container1)
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    canvas_list.append(canvas)

draw_graphs(canvas_list)

# Tab 2 setup
tab2 = ttk.Frame(notebook)
notebook.add(tab2, text="Tab 2")

# Split pane for Tab 2
pane2 = ttk.PanedWindow(tab2, orient=tk.HORIZONTAL)
pane2.pack(fill='both', expand=True)

# Left container (date pickers and time fields)
left_container2 = ttk.Frame(pane2, width=300)
left_container2.pack_propagate(False)
pane2.add(left_container2)

tk.Label(left_container2, text="Select Date 1").pack(pady=5)
date1 = DateEntry(left_container2)
date1.pack(pady=5)

tk.Label(left_container2, text="Select Date 2").pack(pady=5)
date2 = DateEntry(left_container2)
date2.pack(pady=5)

tk.Label(left_container2, text="Hour (0-23) for Date 1").pack(pady=5)
hour1 = tk.Entry(left_container2)
hour1.pack(pady=5)

tk.Label(left_container2, text="Minutes (0-59) for Date 1").pack(pady=5)
minute1 = tk.Entry(left_container2)
minute1.pack(pady=5)

tk.Label(left_container2, text="Hour (0-23) for Date 2").pack(pady=5)
hour2 = tk.Entry(left_container2)
hour2.pack(pady=5)

tk.Label(left_container2, text="Minutes (0-59) for Date 2").pack(pady=5)
minute2 = tk.Entry(left_container2)
minute2.pack(pady=5)

error_label = tk.Label(left_container2, text="", fg="red")
error_label.pack(pady=10)

btn_validate = tk.Button(left_container2, text="Validate & Draw Chart",
                         command=lambda: validate_and_draw_chart(date1, date2, hour1, minute1, hour2, minute2,
                                                                 error_label, canvas2))
btn_validate.pack(pady=10)

# Right container (matplotlib chart)
right_container2 = ttk.Frame(pane2)
pane2.add(right_container2)

fig2, ax2 = plt.subplots(figsize=(5, 5))
canvas2 = FigureCanvasTkAgg(fig2, master=right_container2)
canvas2.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

root.mainloop()