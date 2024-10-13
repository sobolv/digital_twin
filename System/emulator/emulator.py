import random
from datetime import datetime, timedelta


from System.SolarPanel import SolarPanel

sun_ray_angle_by_month_and_hour = {
    'January': [0, 0, 0, 0, 0, 0, 0, 0, 0.98, 8.05, 13.55, 17.07, 18.29, 17.07, 13.55, 8.05, 0.98, 0, 0, 0, 0, 0, 0, 0],
    'February': [0, 0, 0, 0, 0, 0, 0, 0, 7.35, 14.84, 20.76, 24.6, 25.94, 24.6, 20.76, 14.84, 7.35, 0, 0, 0, 0, 0, 0, 0],
    'March': [0, 0, 0, 0, 0, 0, 0, 7.59, 16.59, 24.67, 31.23, 35.59, 37.13, 35.59, 31.23, 24.67, 16.59, 7.59, 0, 0, 0, 0, 0, 0],
    'April': [0, 0, 0, 0, 0, 0, 7.24, 16.78, 26.11, 34.77, 42.07, 47.13, 48.96, 47.13, 42.07, 34.77, 26.11, 16.78, 7.24, 0, 0, 0, 0, 0],
    'May': [0, 0, 0, 0, 0, 5.29, 14.38, 23.85, 33.35, 42.42, 50.39, 56.16, 58.33, 56.16, 50.39, 42.42, 33.35, 23.85, 14.38, 5.29, 0, 0, 0, 0],
    'June': [0, 0, 0, 0, 0, 8.8, 17.73, 27.12, 36.65, 45.9, 54.2, 60.41, 62.81, 60.41, 54.2, 45.9, 36.65, 27.12, 17.73, 8.8, 0.69, 0, 0, 0],
    'July': [0, 0, 0, 0, 0, 7.56, 16.54, 25.97, 35.49, 44.68, 52.86, 58.9, 61.22, 58.9, 52.86, 44.68, 35.49, 25.97, 16.54, 7.56, 0, 0, 0, 0],
    'August': [0, 0, 0, 0, 0, 1.86, 11.07, 20.59, 30.03, 38.91, 46.56, 51.97, 53.97, 51.97, 46.56, 38.91, 30.03, 20.59, 11.07, 1.86, 0, 0, 0, 0],
    'September': [0, 0, 0, 0, 0, 0, 2.63, 12.15, 21.33, 29.7, 36.61, 41.29, 42.97, 41.29, 36.61, 29.7, 21.33, 12.15, 2.63, 0, 0, 0, 0, 0],
    'October': [0, 0, 0, 0, 0, 0, 0, 5.87, 14.8, 22.76, 29.19, 33.44, 34.94, 33.44, 29.19, 22.76, 14.8, 5.87, 0, 0, 0, 0, 0, 0],
    'November': [0, 0, 0, 0, 0, 0, 0, 0, 5.9, 13.3, 19.12, 22.89, 24.19, 22.89, 19.12, 13.3, 5.9, 0, 0, 0, 0, 0, 0, 0],
    'December': [0, 0, 0, 0, 0, 0, 0, 0, 0.28, 7.3, 12.76, 16.25, 17.45, 16.25, 12.76, 7.3, 0.28, 0, 0, 0, 0, 0, 0, 0]
}

class MonthToMinMaxIrradiation:
    def __init__(self, month: str, min_irr_1: float, min_irr_2: float, max_irr_1: float, max_irr_2: float, sunrise: str,
                 sunset: str):
        self.month = month
        self.min_irr_1 = min_irr_1
        self.min_irr_2 = min_irr_2
        self.max_irr_1 = max_irr_1
        self.max_irr_2 = max_irr_2
        self.sunrise = sunrise
        self.sunset = sunset


# Irradiance and daylight data by month
irradiance_by_month = [
    MonthToMinMaxIrradiation("January", 0.01, 0.03, 0.3, 0.4, "07:30", "16:30"),
    MonthToMinMaxIrradiation("February", 0.01, 0.03, 0.4, 0.5, "07:00", "17:30"),
    MonthToMinMaxIrradiation("March", 0.01, 0.05, 0.5, 0.6, "06:30", "18:30"),
    MonthToMinMaxIrradiation("April", 0.05, 0.1, 0.6, 0.7, "06:00", "19:00"),
    MonthToMinMaxIrradiation("May", 0.05, 0.15, 0.7, 0.8, "05:30", "19:30"),
    MonthToMinMaxIrradiation("June", 0.1, 0.2, 0.8, 0.9, "05:00", "20:30"),
    MonthToMinMaxIrradiation("July", 0.1, 0.2, 0.8, 0.9, "05:00", "20:30"),
    MonthToMinMaxIrradiation("August", 0.08, 0.15, 0.7, 0.8, "05:30", "20:00"),
    MonthToMinMaxIrradiation("September", 0.05, 0.1, 0.6, 0.7, "06:00", "19:00"),
    MonthToMinMaxIrradiation("October", 0.01, 0.05, 0.4, 0.5, "06:30", "18:00"),
    MonthToMinMaxIrradiation("November", 0.01, 0.03, 0.3, 0.4, "07:00", "17:00"),
    MonthToMinMaxIrradiation("December", 0.01, 0.02, 0.25, 0.3, "07:30", "16:30")
]


# Function to check if the current time is during daylight hours
def is_daylight(month, current_time):
    for data in irradiance_by_month:
        if month == data.month:
            sunrise = datetime.strptime(data.sunrise, "%H:%M").time()
            sunset = datetime.strptime(data.sunset, "%H:%M").time()
            return sunrise <= current_time.time() <= sunset
    return False


# Function to get the irradiance range based on month and hour
def get_irradiance_range(month, hour):
    for data in irradiance_by_month:
        if month == data.month:
            if 6 <= hour < 10:  # Morning hours
                return random.uniform(data.min_irr_1, data.min_irr_2)
            elif 10 <= hour <= 15:  # Peak solar hours
                return random.uniform(data.max_irr_1, data.max_irr_2)
            else:  # Late afternoon
                return random.uniform(data.min_irr_1, data.min_irr_2)
    return 0  # Default case, should not happen if months are correctly matched


# Updated function to generate date list and map it to solar irradiance
def generate_dates_with_irradiance(start, end, delta_type='minutes', delta_value=1):
    date_irradiance_dict = {}

    # Convert start and end to datetime objects
    current = datetime.strptime(start, "%Y-%m-%d %H:%M")
    end_date = datetime.strptime(end, "%Y-%m-%d %H:%M")

    # Set the delta
    if delta_type == 'minutes':
        delta = timedelta(minutes=delta_value)
    elif delta_type == 'hours':
        delta = timedelta(hours=delta_value)
    else:
        raise ValueError("delta_type must be either 'minutes' or 'hours'")

    # Generate dates and map to solar irradiance
    while current <= end_date:
        month_name = current.strftime("%B")
        hour_of_day = current.hour

        # Check if the current time is in daylight hours
        if is_daylight(month_name, current):
            irradiance = get_irradiance_range(month_name, hour_of_day)
        else:
            irradiance = 0  # No sun during non-daylight hours

        date_irradiance_dict[current] = irradiance
        current += delta

    return date_irradiance_dict


# Example usage
start_date = '2024-10-06 04:00'
end_date = '2024-10-07 20:00'
delta_value = 60  # 60 minutes

dates_with_irradiance =   generate_dates_with_irradiance(start_date, end_date, delta_type='minutes',
                                                       delta_value=delta_value)

sp = SolarPanel()
# Print result
for date, irradiance in dates_with_irradiance.items():
    power = sp.generate_power_from_ui(irradiance * 1000, 0.1, 25, 1)
    print(f"{date}: {irradiance:.4f} {power:.4f}")
