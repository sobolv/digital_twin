import threading
import tkinter as tk
from datetime import datetime, timedelta
from tkinter import ttk

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkcalendar import DateEntry

from System.Battery import Battery
from System.ChargeController import ChargeController
from System.Inverter import Inverter
from System.RemoteMeter import RemoteMeter
from System.SolarPanel import SolarPanel


class SolarBatteryApp:
    def __init__(self, root):
        self.plot_x_array: list = list()
        self.plot_y_array: list = list()
        self.root = root
        self.root.title("Tkinter Layout with Tabs")

        self.stop_event = threading.Event()

        self.fig, self.ax = plt.subplots(figsize=(5, 5))
        self.fig2, self.ax2 = plt.subplots(figsize=(5, 5))

        self.setup_tabs()
        self.setup_tab1_ui()
        self.setup_tab2_ui()

        self.setup_model()

    def setup_tabs(self):
        # Notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill='both')

        # Tab 1 setup ("Калькулятор")
        self.tab1 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab1, text="Калькулятор")

        # Tab 2 setup
        self.tab2 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab2, text="Tab 2")

    def setup_tab1_ui(self):
        # Split pane for Tab 1
        pane1 = ttk.PanedWindow(self.tab1, orient=tk.HORIZONTAL)
        pane1.pack(fill='both', expand=True)

        # Left container (inputs and sliders)
        left_container1 = ttk.Frame(pane1, width=300)
        left_container1.pack_propagate(False)
        pane1.add(left_container1)

        # Сонячна панель section
        tk.Label(left_container1, text="Сонячна панель").pack(pady=5)

        # Option menu for units
        self.solar_unit_var = tk.StringVar(value="hour")
        self.solar_unit_menu = ttk.OptionMenu(left_container1, self.solar_unit_var, "hour", "hour", "minute", "second")
        self.solar_unit_menu.pack(pady=5)

        # Number input for solar irradiance
        tk.Label(left_container1, text="Сонячна ірадіація, Вт").pack(pady=5)
        self.solar_irradiance_var = tk.StringVar()
        solar_irradiance_entry = tk.Entry(left_container1, textvariable=self.solar_irradiance_var)
        solar_irradiance_entry.pack(pady=5)

        # Slider for shade on panel
        tk.Label(left_container1, text="Кількість тіні на панелі, %").pack(pady=5)
        self.shade_var = tk.DoubleVar(value=0)
        shade_slider = tk.Scale(left_container1, from_=0, to=100, orient=tk.HORIZONTAL, variable=self.shade_var)
        shade_slider.pack(pady=5)

        # Number input for panel temperature
        tk.Label(left_container1, text="Температура панелі, градуси цельсію").pack(pady=5)
        self.panel_temp_var = tk.StringVar()
        panel_temp_entry = tk.Entry(left_container1, textvariable=self.panel_temp_var)
        panel_temp_entry.pack(pady=5)

        # Акумулятор section
        tk.Label(left_container1, text="Акумулятор").pack(pady=5)

        # Number input for charge cycles
        tk.Label(left_container1, text="Кількість циклів заряду").pack(pady=5)
        self.charge_cycles_var = tk.StringVar()
        self.charge_cycles_entry = tk.Entry(left_container1, textvariable=self.charge_cycles_var)
        self.charge_cycles_entry.pack(pady=5)

        # Labels for battery voltage and charge
        self.voltage_label = tk.Label(left_container1, text="Напруга акумулятора, %")
        self.voltage_label.pack(pady=5)
        self.charge_label = tk.Label(left_container1, text="Заряд акумулятора, %")
        self.charge_label.pack(pady=5)

        # Навантаження section
        tk.Label(left_container1, text="Навантаження").pack(pady=5)

        # Number input for load
        tk.Label(left_container1, text="Постійне навантаження, А").pack(pady=5)
        self.load_var = tk.StringVar()
        load_entry = tk.Entry(left_container1, textvariable=self.load_var)
        load_entry.pack(pady=5)

        # Error label
        self.error_label = tk.Label(left_container1, text="", fg="red")
        self.error_label.pack(pady=10)

        # Buttons
        btn_calculate = tk.Button(left_container1, text="Калькулювати", command=self.calculate)
        btn_calculate.pack(pady=10)

        btn_clear = tk.Button(left_container1, text="Очистити графік", command=self.clear_graph)
        btn_clear.pack(pady=5)

        btn_stop = tk.Button(left_container1, text="Зупинити", command=self.stop_update)
        btn_stop.pack(pady=5)

        # Right container (single graph)
        right_container1 = ttk.Frame(pane1)
        pane1.add(right_container1)

        self.canvas1 = FigureCanvasTkAgg(self.fig, master=right_container1)
        self.canvas1.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def calculate(self):
        self.stop_event.clear()
        self.update_calculations()

    def setup_tab2_ui(self):
        # Split pane for Tab 2
        pane2 = ttk.PanedWindow(self.tab2, orient=tk.HORIZONTAL)
        pane2.pack(fill='both', expand=True)

        # Left container (date pickers and time fields)
        left_container2 = ttk.Frame(pane2, width=300)
        left_container2.pack_propagate(False)
        pane2.add(left_container2)

        tk.Label(left_container2, text="Select Date 1").pack(pady=5)
        self.date1 = DateEntry(left_container2)
        self.date1.pack(pady=5)

        tk.Label(left_container2, text="Select Date 2").pack(pady=5)
        self.date2 = DateEntry(left_container2)
        self.date2.pack(pady=5)

        tk.Label(left_container2, text="Hour (0-23) for Date 1").pack(pady=5)
        self.hour1 = tk.Entry(left_container2)
        self.hour1.pack(pady=5)

        tk.Label(left_container2, text="Minutes (0-59) for Date 1").pack(pady=5)
        self.minute1 = tk.Entry(left_container2)
        self.minute1.pack(pady=5)

        tk.Label(left_container2, text="Hour (0-23) for Date 2").pack(pady=5)
        self.hour2 = tk.Entry(left_container2)
        self.hour2.pack(pady=5)

        tk.Label(left_container2, text="Minutes (0-59) for Date 2").pack(pady=5)
        self.minute2 = tk.Entry(left_container2)
        self.minute2.pack(pady=5)

        self.error_label_tab2 = tk.Label(left_container2, text="", fg="red")
        self.error_label_tab2.pack(pady=10)

        btn_validate = tk.Button(left_container2, text="Validate & Draw Chart",
                                 command=lambda: None)  # Placeholder command
        btn_validate.pack(pady=10)

        # Right container (matplotlib chart)
        right_container2 = ttk.Frame(pane2)
        pane2.add(right_container2)

        self.canvas2 = FigureCanvasTkAgg(self.fig2, master=right_container2)
        self.canvas2.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def update_calculations(self):
        try:
            # Validations
            solar_irradiance = float(self.solar_irradiance_var.get())
            if solar_irradiance < 0:
                raise ValueError("Сонячна ірадіація повинна бути >= 0.")

            shade = float(self.shade_var.get()) / 100.0
            panel_temp = float(self.panel_temp_var.get())

            charge_cycles = int(self.charge_cycles_var.get())
            if charge_cycles < 0:
                raise ValueError("Кількість циклів заряду повинна бути >= 0.")

            load = float(self.load_var.get())
            if load < 0:
                raise ValueError("Постійне навантаження повинно бути >= 0.")

            # Convert time unit
            chosen_time_unit = self.solar_unit_var.get()
            if chosen_time_unit == "hour":
                time_delta = 3600
                self.current_time += timedelta(hours=time_delta)
            elif chosen_time_unit == "minute":
                time_delta = 60
                self.current_time += timedelta(minutes=time_delta)
            else:
                time_delta = 1
                self.current_time += timedelta(seconds=time_delta)

            self.plot_x_array.append(self.current_time)

            power, charge_in_percent, voltage, charge_cycles_return = self.controller.process_from_ui(solar_irradiance,
                                                                                                      shade, panel_temp)
            self.inverter.power_with_load(load)
            self.plot_y_array.append(charge_in_percent)
            # Perform calculation and update the UI
            self.voltage_label.config(text="Напруга: " + str(voltage) + "V")
            self.charge_label.config(text="Заряд: " + str(charge_in_percent) + "%")
            # self.charge_cycles_entry.insert(0, charge_cycles_return)

            self.error_label.config(text="")  # Clear previous error message

            # Update the graph
            self.ax.clear()  # Clear the previous graph but keep the axes
            self.ax.plot(self.plot_x_array, self.plot_y_array)
            self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
            for label in self.ax.get_xticklabels():
                label.set_rotation(90)

            # Use tight_layout to avoid label overlap
            self.fig.tight_layout()
            self.canvas1.draw()

            # Recursively call the update function every second if not stopped
            if not self.stop_event.is_set():
                self.root.after(1000, self.update_calculations)

        except Exception as e:
            self.error_label.config(text=f"Error: {str(e)}")

    def stop_update(self):
        self.stop_event.set()

    def clear_graph(self):
        self.ax.clear()  # Clear the data but leave the axes
        self.ax.set_title("Graph cleared")  # Optionally, show some placeholder message
        self.canvas1.draw()
        self.error_label.config(text="")  # Clear previous error message
        self.plot_x_array = []
        self.plot_y_array = []

    def setup_model(self):
        self.panel = SolarPanel()
        self.battery = Battery()
        self.remote_meter = RemoteMeter()
        self.controller = ChargeController(self.panel, self.battery, self.remote_meter)
        self.inverter = Inverter(self.battery)
        self.current_time = datetime.now()


if __name__ == "__main__":
    root = tk.Tk()
    app = SolarBatteryApp(root)
    root.mainloop()
