import threading
from datetime import datetime, timedelta

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import ttkbootstrap as ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from ttkbootstrap.widgets import DateEntry

from System.devices import HairDryer, Fridge, Lamp, Microwave, TV, Kettle
from System.emulator import emulator

font_size = 10
font_name = "Roboto"

from System.Battery import Battery
from System.ChargeController import ChargeController
from System.Inverter import Inverter
from System.RemoteMeter import RemoteMeter
from System.SolarPanel import SolarPanel


class SolarBatteryApp:
    def __init__(self, root):
        self.device_list = list()
        self.plot_x_array: list = list()
        self.plot_x_array_2: list = list()
        self.plot_y_array: list = list()
        self.plot_y_array_2: list = list()
        self.plot_power_array_2 = []
        self.root = root
        self.root.title("Цифровий двійник лабораторного стенду сонячної панелі")

        self.stop_event = threading.Event()
        self.stop_event_2 = threading.Event()

        self.fig, self.ax = plt.subplots(figsize=(5, 5))
        self.fig2, self.ax2 = plt.subplots(figsize=(5, 5))
        self.fig3, self.ax3 = plt.subplots(figsize=(5, 5))

        self.setup_tabs()
        self.setup_tab1_ui()
        self.setup_tab2_ui()

        self.setup_model()

    def setup_tabs(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill='both')

        # Tab 1 setup ("Калькулятор")
        self.tab1 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab1, text="Калькулятор")

        # Tab 2 setup
        self.tab2 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab2, text="Моделювання навантаження пристроїв")

    def setup_tab1_ui(self):
        style = ttk.Style()
        style.configure("Custom.TFrame", background="#7D8A8B")

        # Split pane for Tab 1
        pane1 = ttk.PanedWindow(self.tab1, orient=ttk.HORIZONTAL)
        pane1.pack(fill='both', expand=True)

        # Left container (inputs and sliders)
        left_container1 = ttk.Frame(pane1, style="Custom.TFrame", width=500)
        left_container1.pack_propagate(False)
        pane1.add(left_container1)

        # Сонячна панель section
        ttk.Label(left_container1, text="Сонячна панель", font=(font_name, font_size, 'bold'), foreground="white",
                  background="#7D8A8B").pack(pady=5)

        # Option menu for units
        ttk.Label(left_container1, text="Одиниця виміру часу", font=(font_name, font_size), foreground="white",
                  background="#7D8A8B").pack(pady=5)
        self.solar_unit_var = ttk.StringVar(value="година")
        self.solar_unit_menu = ttk.OptionMenu(left_container1, self.solar_unit_var, "година", "година", "хвилина",
                                              "секунда")
        self.solar_unit_menu.pack(pady=5)

        # Number input for solar irradiance
        ttk.Label(left_container1, text="Сонячна ірадіація, Вт", font=(font_name, font_size), foreground="white",
                  background="#7D8A8B").pack(pady=5)
        self.solar_irradiance_var = ttk.StringVar()
        solar_irradiance_entry = ttk.Entry(left_container1, textvariable=self.solar_irradiance_var)
        solar_irradiance_entry.pack(pady=5)

        ttk.Label(left_container1, text="Кут нахилу сонячних променів, °", font=(font_name, font_size), foreground="white",
                  background="#7D8A8B").pack(pady=5)
        self.sun_ray_angle_var = ttk.StringVar()
        sun_ray_angle_entry = ttk.Entry(left_container1, textvariable=self.sun_ray_angle_var)
        sun_ray_angle_entry.pack(pady=5)

        ttk.Label(left_container1, text="Кут нахилу панелі, °", font=(font_name, font_size), foreground="white",
                  background="#7D8A8B").pack(pady=5)
        self.panel_angle_var = ttk.StringVar()
        panel_angle_entry = ttk.Entry(left_container1, textvariable=self.panel_angle_var)
        panel_angle_entry.pack(pady=5)

        scale_style = ttk.Style()
        scale_style.configure("Custom.Horizontal.TScale", background="#7D8A8B")

        # Slider for shade on panel
        ttk.Label(left_container1, text="Кількість тіні на панелі, %", font=(font_name, font_size), foreground="white",
                  background="#7D8A8B").pack(pady=5)
        self.shade_var = ttk.DoubleVar(value=0)
        shade_slider = ttk.Scale(left_container1, from_=0, to=100, orient=ttk.HORIZONTAL, variable=self.shade_var,
                                 style="Custom.Horizontal.TScale")
        shade_slider.pack(pady=5)

        # Number input for panel temperature
        ttk.Label(left_container1, text="Температура панелі, градуси цельсію", font=(font_name, font_size),
                  foreground="white", background="#7D8A8B").pack(pady=5)
        self.panel_temp_var = ttk.StringVar()
        panel_temp_entry = ttk.Entry(left_container1, textvariable=self.panel_temp_var)
        panel_temp_entry.pack(pady=5)

        # Акумулятор section
        ttk.Label(left_container1, text="Акумулятор", font=(font_name, font_size, 'bold'), foreground="white",
                  background="#7D8A8B").pack(pady=5)

        # Number input for charge cycles
        ttk.Label(left_container1, text="Кількість циклів заряду", font=(font_name, font_size), foreground="white",
                  background="#7D8A8B").pack(pady=5)
        self.charge_cycles_var = ttk.StringVar()
        self.charge_cycles_entry = ttk.Entry(left_container1, textvariable=self.charge_cycles_var)
        self.charge_cycles_entry.pack(pady=5)

        # Labels for battery voltage and charge
        self.power_label = ttk.Label(left_container1, text="Генерація панелі, Вт", font=(font_name, font_size),
                                     foreground="white", background="#7D8A8B")
        self.power_label.pack(pady=5)
        self.voltage_label = ttk.Label(left_container1, text="Напруга акумулятора, %", font=(font_name, font_size),
                                       foreground="white", background="#7D8A8B")
        self.voltage_label.pack(pady=5)
        self.charge_label = ttk.Label(left_container1, text="Заряд акумулятора, %", font=(font_name, font_size),
                                      foreground="white", background="#7D8A8B")
        self.charge_label.pack(pady=5)

        # Навантаження section
        ttk.Label(left_container1, text="Навантаження", font=(font_name, font_size), foreground="white",
                  background="#7D8A8B").pack(pady=5)
        self.current_draw = ttk.Label(left_container1, text="Споживання, Вт", font=(font_name, font_size),
                                      foreground="white",
                                      background="#7D8A8B")
        self.current_draw.pack(pady=5)
        # Number input for load
        ttk.Label(left_container1, text="Постійне навантаження, А", font=(font_name, font_size), foreground="white",
                  background="#7D8A8B").pack(pady=5)


        self.load_var = ttk.StringVar()
        load_entry = ttk.Entry(left_container1, textvariable=self.load_var)
        load_entry.pack(pady=5)

        # Error label
        self.error_label = ttk.Label(left_container1, text="", font=(font_name, font_size), background="#7D8A8B",
                                     foreground="#D60000")
        self.error_label.pack(pady=10)

        # Buttons
        btn_calculate = ttk.Button(left_container1, text="Калькулювати", command=self.calculate)
        btn_calculate.pack(pady=10)

        btn_clear = ttk.Button(left_container1, text="Очистити графік", command=self.clear_graph)
        btn_clear.pack(pady=5)

        btn_stop = ttk.Button(left_container1, text="Зупинити", command=self.stop_update)
        btn_stop.pack(pady=5)

        # Right container (single graph)
        right_container1 = ttk.Frame(pane1)
        pane1.add(right_container1)

        self.canvas1 = FigureCanvasTkAgg(self.fig, master=right_container1)
        self.canvas1.get_tk_widget().pack(side=ttk.TOP, fill=ttk.BOTH, expand=True)

    def calculate(self):
        self.stop_event.clear()
        self.update_calculations()

    def setup_tab2_ui(self):
        pane2 = ttk.PanedWindow(self.tab2, orient=ttk.HORIZONTAL)
        pane2.pack(fill='both', expand=True)

        # Left container (date picker, sliders, etc.)
        left_container2 = ttk.Frame(pane2, style="Custom.TFrame", width=500)
        left_container2.pack_propagate(False)
        pane2.add(left_container2)

        # Option menu for units
        ttk.Label(left_container2, text="Одиниця виміру часу", font=(font_name, font_size), foreground="white",
                  background="#7D8A8B").pack(pady=5)
        self.solar_unit_var_2 = ttk.StringVar(value="година")
        self.solar_unit_menu_2 = ttk.OptionMenu(left_container2, self.solar_unit_var_2, "година", "година", "хвилина",
                                              "секунда")
        self.solar_unit_menu_2.pack(pady=5)

        # Start date label and picker
        ttk.Label(left_container2, text="Start Date (YYYY-MM-DD HH:MM)", font=(font_name, font_size),
                  foreground="white", background="#7D8A8B").pack(pady=5)
        self.start_date = DateEntry(left_container2, bootstyle="info", width=20)
        self.start_date.pack(pady=5)
        self.start_time = ttk.Entry(left_container2, width=10)
        self.start_time.pack(pady=5)
        self.start_time.insert(0, "00:00")  # Default time

        # Shadow coefficient slider
        ttk.Label(left_container2, text="Shadow Coefficient", font=(font_name, font_size), foreground="white",
                  background="#7D8A8B").pack(pady=5)
        self.shadow_var = ttk.DoubleVar(value=0)
        self.shadow_slider = ttk.Scale(left_container2, from_=0, to=100, orient=ttk.HORIZONTAL,
                                       variable=self.shadow_var,
                                       style="Custom.Horizontal.TScale")
        self.shadow_slider.pack(pady=5)

        # Panel temperature input
        ttk.Label(left_container2, text="Panel Temperature (°C)", font=(font_name, font_size), foreground="white",
                  background="#7D8A8B").pack(pady=5)
        self.panel_temp2_var = ttk.StringVar()
        panel_temp2_entry = ttk.Entry(left_container2, textvariable=self.panel_temp2_var)
        panel_temp2_entry.pack(pady=5)

        # Devices section
        ttk.Label(left_container2, text="Devices", font=(font_name, font_size, 'bold'), foreground="white",
                  background="#7D8A8B").pack(pady=10)

        # Container for device inputs and buttons
        devices_frame = ttk.Frame(left_container2, style="Custom.TFrame")
        devices_frame.pack(pady=5)

        # Hair Dryer input
        ttk.Label(devices_frame, text="Hair Dryer", font=(font_name, font_size), foreground="white",
                  background="#7D8A8B").grid(row=0, column=0, pady=5)
        ttk.Label(devices_frame, text="Temperature", font=(font_name, font_size), foreground="white",
                  background="#7D8A8B").grid(row=0, column=1)
        self.hairdryer_temp_var = ttk.StringVar(value="1")
        self.hairdryer_temp = ttk.Combobox(devices_frame, textvariable=self.hairdryer_temp_var, values=["1", "2", "3"],
                                           width=5, state="readonly")
        self.hairdryer_temp.grid(row=0, column=2)

        ttk.Label(devices_frame, text="Speed", font=(font_name, font_size), foreground="white",
                  background="#7D8A8B").grid(row=0, column=3)
        self.hairdryer_speed_var = ttk.StringVar(value="1")
        self.hairdryer_speed = ttk.Combobox(devices_frame, textvariable=self.hairdryer_speed_var, values=["1", "2"],
                                            width=5, state="readonly")
        self.hairdryer_speed.grid(row=0, column=4)

        ttk.Button(devices_frame, text="+", command=self.add_hairdryer).grid(row=0, column=5, padx=5)

        # Fridge input
        ttk.Label(devices_frame, text="Fridge", font=(font_name, font_size), foreground="white",
                  background="#7D8A8B").grid(row=1, column=0, pady=5)
        ttk.Button(devices_frame, text="+", command=self.add_fridge).grid(row=1, column=5, padx=5)

        # Lamp input
        ttk.Label(devices_frame, text="Lamp", font=(font_name, font_size), foreground="white",
                  background="#7D8A8B").grid(row=2, column=0, pady=5)
        ttk.Button(devices_frame, text="+", command=self.add_lamp).grid(row=2, column=5, padx=5)

        # Microwave input
        ttk.Label(devices_frame, text="Microwave", font=(font_name, font_size), foreground="white",
                  background="#7D8A8B").grid(row=3, column=0, pady=5)
        self.microwave_power_var = ttk.StringVar(value="120")
        self.microwave_power = ttk.Combobox(devices_frame, textvariable=self.microwave_power_var,
                                            values=["120", "250", "380", "500", "700"], width=5, state="readonly")
        self.microwave_power.grid(row=3, column=2)
        ttk.Button(devices_frame, text="+", command=self.add_microwave).grid(row=3, column=5, padx=5)

        # TV input
        ttk.Label(devices_frame, text="TV", font=(font_name, font_size), foreground="white",
                  background="#7D8A8B").grid(row=4, column=0, pady=5)
        ttk.Button(devices_frame, text="+", command=self.add_tv).grid(row=4, column=5, padx=5)

        # Kettle input
        ttk.Label(devices_frame, text="Kettle", font=(font_name, font_size), foreground="white",
                  background="#7D8A8B").grid(row=5, column=0, pady=5)
        ttk.Label(devices_frame, text="Amount of Water", font=(font_name, font_size), foreground="white",
                  background="#7D8A8B").grid(row=5, column=1)
        self.kettle_water_amount_var = ttk.StringVar()
        self.kettle_water_amount = ttk.Entry(devices_frame, textvariable=self.kettle_water_amount_var, width=5)
        self.kettle_water_amount.grid(row=5, column=2)

        ttk.Label(devices_frame, text="Start Temp (°C)", font=(font_name, font_size), foreground="white",
                  background="#7D8A8B").grid(row=5, column=3)
        self.kettle_start_temp_var = ttk.StringVar()
        self.kettle_start_temp = ttk.Entry(devices_frame, textvariable=self.kettle_start_temp_var, width=5)
        self.kettle_start_temp.grid(row=5, column=4)

        ttk.Button(devices_frame, text="+", command=self.add_kettle).grid(row=5, column=5, padx=5)

        # Buttons
        btn_calculate_tab2 = ttk.Button(left_container2, text="Calculate", command=self.update_2)
        btn_calculate_tab2.pack(pady=10)

        btn_clear_tab2 = ttk.Button(left_container2, text="Clear Chart", command=self.clear_graph_tab2)
        btn_clear_tab2.pack(pady=5)

        btn_stop_tab2 = ttk.Button(left_container2, text="Stop", command=self.stop_update_tab2)
        btn_stop_tab2.pack(pady=5)

        # Right container (graph and dynamic buttons for devices)
        right_container2 = ttk.Frame(pane2)
        pane2.add(right_container2)

        self.canvas2 = FigureCanvasTkAgg(self.fig2, master=right_container2)
        self.canvas2.get_tk_widget().pack(side=ttk.LEFT, fill=ttk.BOTH, expand=True)
        self.canvas3 = FigureCanvasTkAgg(self.fig3, master=right_container2)
        self.canvas3.get_tk_widget().pack(side=ttk.RIGHT, fill=ttk.BOTH, expand=True)

        # Device buttons
        self.device_buttons_frame = ttk.Frame(right_container2)
        self.device_buttons_frame.pack(side=ttk.BOTTOM, fill=ttk.X)

    def add_hairdryer(self):
        temperature = int(self.hairdryer_temp_var.get())
        speed = int(self.hairdryer_speed_var.get())
        hairdryer = HairDryer(temperature, speed)
        self.device_list.append(hairdryer)
        self.update_device_buttons()

    def add_fridge(self):
        fridge = Fridge()
        self.device_list.append(fridge)
        self.update_device_buttons()

    def add_lamp(self):
        lamp = Lamp()
        self.device_list.append(lamp)
        self.update_device_buttons()

    def add_microwave(self):
        power = int(self.microwave_power_var.get())
        microwave = Microwave(power)
        self.device_list.append(microwave)
        self.update_device_buttons()

    def add_tv(self):
        tv = TV()
        self.device_list.append(tv)
        self.update_device_buttons()

    def add_kettle(self):
        water_amount = int(self.kettle_water_amount_var.get())
        start_temp = int(self.kettle_start_temp_var.get())
        kettle = Kettle(water_amount, start_temp)
        self.device_list.append(kettle)
        self.update_device_buttons()

    def update_device_buttons(self):
        # Clear the current buttons
        for widget in self.device_buttons_frame.winfo_children():
            widget.destroy()

        # Add a button for each device in the list
        for i, device in enumerate(self.device_list):
            btn = ttk.Button(self.device_buttons_frame, text=str(device), command=lambda i=i: self.remove_device(i))
            btn.pack(side=ttk.LEFT, padx=5)

    def remove_device(self, index):
        del self.device_list[index]
        self.update_device_buttons()

    def update_2(self):
        self.stop_event_2.clear()
        self.calculate_tab2()
    counter = 0

    def calculate_tab2(self):

        try:
            panel_temp2_var = float(self.panel_temp2_var.get())
            shadow_slider = float(self.shadow_slider.get()) / 100
            start_date = self.start_date.entry.get()
            start_time = self.start_time.get()
        except ValueError as e:
            # Show error message if any field is not a valid number
            self.error_label = ttk.Label(self.tab2, text="Error: Please enter valid numeric values.", foreground="red")
            self.error_label.pack(pady=10)
            return

        if panel_temp2_var <= 0 or shadow_slider <= 0:
            self.error_label = ttk.Label(self.tab2, text="Error: All values must be positive numbers.",
                                         foreground="red")
            self.error_label.pack(pady=10)
            return

        combined_datetime = datetime.strptime(f"{start_date} {start_time}", "%d.%m.%Y %H:%M")
        if self.counter is 0:
            self.current_time_2 = combined_datetime
            self.counter = 1


        # Convert time unit
        chosen_time_unit = self.solar_unit_var_2.get()
        if chosen_time_unit == "година":
            time_delta = 1
            self.current_time_2 += timedelta(hours=1)
        elif chosen_time_unit == "хвилина":
            time_delta = 60
            self.current_time_2 += timedelta(minutes=1)
        else:
            time_delta = 3600
            self.current_time_2 += timedelta(seconds=1)

        irradiance = emulator.get_solar_irradiance_for_datetime(self.current_time_2) * 1000  # TODO delta_time?
        power, charge_in_percent, voltage, charge_cycles_return = self.controller_2.process_from_ui(irradiance,
                                                                                                    shadow_slider,
                                                                                                    panel_temp2_var,
                                                                                                    time_delta)  # Charging

        total_draw = 0
        for device in self.device_list:
            total_draw += device.power_on(time_delta) # Calculate total power draw at given time of powered on devices
        print(f"Total draw: {total_draw}, Total power: {power}, Total charge: {charge_in_percent}")
        power_draw, charge_in_percent, voltage = self.inverter_2.power_with_load(total_draw, time_delta) # Discharge


        # Check if the length exceeds the limit, remove the oldest data if necessary
        max_points = 50
        if len(self.plot_x_array_2) > max_points:
            self.plot_x_array_2.pop(0)  # Remove the first (oldest) element from the x array
            self.plot_y_array_2.pop(0)  # Remove the first (oldest) element from the y array
            self.plot_power_array_2.pop(0)  # Remove the first (oldest) element from the y array

        self.plot_x_array_2.append(self.current_time_2)
        self.plot_y_array_2.append(charge_in_percent)
        self.plot_power_array_2.append(power)

        # Update the graph
        self.ax2.clear()
        self.ax3.clear()  # Clear the power plot
        self.ax2.plot(self.plot_x_array_2, self.plot_y_array_2)
        self.ax2.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
        for label in self.ax2.get_xticklabels():
            label.set_rotation(90)

        # Maintain the scale by setting the limits manually
        self.ax2.set_xlim(
            [self.plot_x_array_2[0], self.plot_x_array_2[-1]])  # Adjust x-axis limits to the current data range
        self.ax2.set_ylim([-10, 110])  # Adjust y-axis limits, assuming charge_in_percent is between 0 and 100
        # Use tight_layout to avoid label overlap
        self.ax2.set_title('Charge in Percentage')
        self.ax2.set_ylabel('Charge (%)')
        self.ax2.legend()

        # Create a new subplot for power
        self.ax3.plot(self.plot_x_array_2, self.plot_power_array_2, color='orange', label='Power (W)')
        self.ax3.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
        for label in self.ax3.get_xticklabels():
            label.set_rotation(90)
        self.ax3.set_xlim([self.plot_x_array_2[0], self.plot_x_array_2[-1]])
        self.ax3.set_ylim([0, max(self.plot_power_array_2) * 1.1])  # Adjust y-axis limits for power
        self.ax3.set_title('Power Generated from Solar Panel')
        self.ax3.set_ylabel('Power (W)')
        self.ax3.legend()

        self.fig2.tight_layout()
        self.canvas2.draw()
        self.canvas3.draw()

        # Recursively call the update function every second if not stopped
        if not self.stop_event_2.is_set():
            self.root.after(1000, self.calculate_tab2)

    def clear_graph_tab2(self):
        self.ax2.clear()  # Clear the data but leave the axes
        self.ax2.set_title("Графік очищено")  # Optionally, show some placeholder message
        self.canvas2.draw()
        self.canvas3.draw()
        self.error_label.config(text="")  # Clear previous error message
        self.plot_x_array_2 = []
        self.plot_y_array_2 = []
        self.plot_power_array_2 = []
        pass

    def stop_update_tab2(self):
        self.stop_event_2.set()

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
            elif load*220 > 4000:
                raise ValueError("Споживання перевищує можливості інвертора")

            sun_ray_angle = float(self.sun_ray_angle_var.get())
            if(sun_ray_angle < 0):
                raise ValueError("Кут нахилу сонячних променів повинен бути >= 0.")

            panel_angle = float(self.panel_angle_var.get())
            if panel_angle < 0:
                raise ValueError("Кут нахилу панелі повинен бути >= 0.")

            # Convert time unit
            chosen_time_unit = self.solar_unit_var.get()
            if chosen_time_unit == "година":
                time_delta = 1
                self.current_time += timedelta(hours=1)
            elif chosen_time_unit == "хвилина":
                time_delta = 60
                self.current_time += timedelta(minutes=1)
            else:
                time_delta = 3600
                self.current_time += timedelta(seconds=1)

            power, charge_in_percent, voltage, charge_cycles_return = self.controller.process_from_ui(solar_irradiance,
                                                                                                      shade, panel_temp,
                                                                                                      time_delta,
                                                                                                      sun_ray_angle,
                                                                                                      panel_angle)
            power_draw, charge_in_percent, voltage = self.inverter.power_with_load_amps(load, time_delta)

            self.plot_x_array.append(self.current_time)
            self.plot_y_array.append(charge_in_percent)

            # Check if the length exceeds the limit, remove the oldest data if necessary
            max_points = 50
            if len(self.plot_x_array) > max_points:
                self.plot_x_array.pop(0)  # Remove the first (oldest) element from the x array
                self.plot_y_array.pop(0)  # Remove the first (oldest) element from the y array
            # Perform calculation and update the UI
            self.power_label.config(text="Генерація панелі: " + str(power) + " Вт")
            self.voltage_label.config(text="Напруга: " + str(voltage) + "V")
            self.charge_label.config(text="Заряд: " + str(charge_in_percent) + "%")
            self.current_draw.config(text="Споживання " + str(power_draw) + "Вт")
            # self.charge_cycles_entry.insert(0, charge_cycles_return)

            self.error_label.config(text="")  # Clear previous error message

            # Update the graph
            self.ax.clear()  # Clear the previous graph but keep the axes
            self.ax.plot(self.plot_x_array, self.plot_y_array)
            self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
            for label in self.ax.get_xticklabels():
                label.set_rotation(90)

            # Maintain the scale by setting the limits manually
            self.ax.set_xlim(
                [self.plot_x_array[0], self.plot_x_array[-1]])  # Adjust x-axis limits to the current data range
            self.ax.set_ylim([-10, 110])  # Adjust y-axis limits, assuming charge_in_percent is between 0 and 100
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
        self.ax.set_title("Графік очищено")  # Optionally, show some placeholder message
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

        self.panel_2 = SolarPanel()
        self.battery_2 = Battery()
        self.remote_meter_2 = RemoteMeter()
        self.controller_2 = ChargeController(self.panel_2, self.battery_2, self.remote_meter_2)
        self.inverter_2 = Inverter(self.battery_2)
        self.current_time = datetime.now()


if __name__ == "__main__":
    root = ttk.Window(themename="flatly")
    app = SolarBatteryApp(root)
    root.mainloop()
