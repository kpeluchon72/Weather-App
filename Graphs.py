# Graph figures and extracting data from API call
import matplotlib.pyplot as plt


class Graphs:
    def __init__(self, weather_data, air_data):
        self.weather_data = weather_data

        self.air_data = air_data
        self.air_data_components = air_data["list"][0]["components"]
        self.air_data_pollutants = []
        self.air_data_concentration = []

        self.snows = [] # mm, probability
        self.days = []
        self.clouds = [] # %
        self.temperature_data = []  # average, feels like, min, max
        self.pressure_data = [] # sea level, ground level
        self.rains = [] # mm, probability
        self.humidity = []
        self.wind_speed = []

        for i in range(10):
            day = self.weather_data['list'][0]['dt_txt']
            self.days.append(day)

            temp_data = [self.weather_data['list'][i]['main']['temp'], self.weather_data['list'][i]['main']['feels_like'], weather_data['list'][i]['main']['temp_min'], weather_data['list'][i]['main']['temp_max']]
            self.temperature_data.append(temp_data)

            humidity_data = self.weather_data['list'][i]['main']['humidity']
            self.humidity.append(humidity_data)

            press_data = [self.weather_data['list'][i]['main']['pressure'], self.weather_data['list'][i]['main']['grnd_level']]
            self.pressure_data.append(press_data)

            cloudiness_data = self.weather_data['list'][i]['clouds']['all']
            self.clouds.append(cloudiness_data)

            wind_speed_data = self.weather_data['list'][i]['wind']['speed']
            self.wind_speed.append(wind_speed_data)

            if 'rain' in self.weather_data['list'][i]:
                rain = [self.weather_data['list'][i]['rain']['3h'], self.weather_data['list'][i]['pop']]
            else:
                rain = [0, 0]
            self.rains.append(rain)

            if 'snow' in self.weather_data['list'][i]:
                snow = [self.weather_data['list'][i]['snow']['3h'], self.weather_data['list'][i]['pop']]
            else:
                snow = [0, 0]
            self.snows.append(snow)

        for key, value in self.air_data_components.items():
            self.air_data_pollutants.append(key)
            self.air_data_concentration.append(value)

        self.periods = range(1, len(self.temperature_data) + 1)

    def plot_pressure(self):

        sea_level = [period[0] for period in self.pressure_data]
        ground_level = [period[1] for period in self.pressure_data]

        fig, ax = plt.subplots(figsize=(8, 6))

        ax.plot(self.periods, sea_level, marker='o', linestyle='-', label='Sea Level Pressure')
        ax.plot(self.periods, ground_level, marker='s', linestyle='--', label='Ground Level Pressure')

        ax.set_xticks(self.periods)

        ax.set_xlabel(f'3hr time steps from  {self.weather_data["list"][0]["dt_txt"]} to {self.weather_data["list"][-1]["dt_txt"]}')
        ax.set_ylabel('Pressure (hPa)')
        ax.set_title('Ground and Sea level Pressure')

        ax.legend()

        return fig

    def plot_temp(self):

        average_temps = [period[0] for period in self.temperature_data]
        min_temps = [period[1] for period in self.temperature_data]
        max_temps = [period[2] for period in self.temperature_data]

        fig, ax = plt.subplots(figsize=(8, 6))

        ax.plot(self.periods, average_temps, marker='o', linestyle='-', label='Average Temp')
        ax.plot(self.periods, min_temps, marker='s', linestyle='--', label='Min Temp')
        ax.plot(self.periods, max_temps, marker='^', linestyle='-.', label='Max Temp')

        ax.set_xticks(self.periods)

        ax.set_xlabel(f'3hr time steps from  {self.weather_data["list"][0]["dt_txt"]} to {self.weather_data["list"][-1]["dt_txt"]}')
        ax.set_ylabel('Temperature (°C)')
        ax.set_title('Temperature Variation')
        plt.tight_layout()

        ax.legend()

        return fig

    def plot_rain_snow(self):

        mm_of_rain = [period[0] for period in self.rains]
        snow_mm = [period[0] for period in self.snows]

        fig, ax = plt.subplots(figsize=(8, 6))

        ax.plot(self.periods, mm_of_rain, marker='o', linestyle='-', label='Rain')
        ax.plot(self.periods, snow_mm, marker='s', linestyle='--', label='Snow')

        ax.set_xticks(self.periods)

        ax.set_xlabel(f'3hr time steps from  {self.weather_data["list"][0]["dt_txt"]} to {self.weather_data["list"][-1]["dt_txt"]}')
        ax.set_ylabel('Precipitation (mm)')
        ax.set_title('Precipitation')
        ax.set_ylim(0, max(mm_of_rain) + .5)
        plt.tight_layout()

        ax.legend()

        return fig

    def rain_snow_prob(self):
        snow_prob = [period[1] for period in self.snows]
        rain_prob = [period[1] for period in self.rains]
        fig, ax = plt.subplots(figsize=(8, 6))

        bar_width = 0.35
        index = self.periods

        bar1 = ax.bar(index, rain_prob, bar_width, label='Rain Probability')
        bar2 = ax.bar([i + bar_width for i in index], snow_prob, bar_width, label='Snow Probability')

        ax.set_xticks(index)

        ax.set_xlabel(f'3hr time steps from {self.weather_data["list"][0]["dt_txt"]} to {self.weather_data["list"][-1]["dt_txt"]}')
        ax.set_ylabel('Probability in %')
        ax.set_title('Probability of Precipitation')
        ax.set_ylim(0, 1)
        ax.legend()

        plt.tight_layout()

        return fig

    def humidity_chart(self):
        fig, ax = plt.subplots(figsize=(8, 6))

        bar_width = 0.35

        ax.bar(self.periods, self.humidity, bar_width, label='Humidity')
        ax.set_xticks(self.periods)

        ax.set_xlabel(f'3hr time steps from {self.weather_data["list"][0]["dt_txt"]} to {self.weather_data["list"][-1]["dt_txt"]}')
        ax.set_ylabel('Humidity in %')
        ax.set_title('Humidity')

        ax.legend()

        plt.tight_layout()

        return fig

    def air_bar_graph(self):
        colors = ["gray", "#3399FF", "#003366", "#660066", "#FFFF33", "#FF0000", "#663300"]

        fig, ax = plt.subplots(figsize=(8, 6))

        bar_width = 0.35

        ax.bar(self.air_data_pollutants, self.air_data_concentration, color=colors, width=bar_width)

        ax.set_xlabel('Pollutants')
        ax.set_ylabel('Concentration in μg/m3 (Micrograms per Cubic Meter)')
        ax.set_title('Concentration of Air Pollutants')

        # logarithmic scale to better interpret data
        ax.set_yscale('log')

        return fig

    def cloudiness(self):
        fig, ax = plt.subplots(figsize=(8, 6))

        bar_width = 0.35

        ax.bar(self.periods, self.clouds, bar_width, label='Cloudiness')
        ax.set_xticks(self.periods)

        ax.set_xlabel(f'3hr time steps from {self.weather_data["list"][0]["dt_txt"]} to {self.weather_data["list"][-1]["dt_txt"]}')
        ax.set_ylabel('Cloudiness in %')
        ax.set_title('Cloudiness')

        ax.legend()

        plt.tight_layout()

        return fig

    def wind_speed_graph(self):
        fig, ax = plt.subplots(figsize=(8, 6))

        ax.plot(self.periods, self.wind_speed, marker='o', linestyle='-', label='Wind Speed')

        ax.set_xticks(self.periods)

        ax.set_xlabel(f'3hr time steps from  {self.weather_data["list"][0]["dt_txt"]} to {self.weather_data["list"][-1]["dt_txt"]}')
        ax.set_ylabel('Wind Speed (m/s)')
        ax.set_title('Wind Speed')
        plt.tight_layout()

        ax.legend()

        return fig

    def get_wind_direction(self):
        wind_degree = self.weather_data['list'][0]['wind']['deg']

        compass_directions = {
            'North': range(337, 23),
            'North East': range(23, 68),
            'East': range(68, 113),
            'South East': range(113, 158),
            'South': range(158, 203),
            'South West': range(203, 248),
            'West': range(248, 293),
            'North West': range(293, 338)
        }

        for direction, degree_range in compass_directions.items():
            if wind_degree % 360 in degree_range:
                return direction


"""
Example = Graphs({'cod': '200',
            'message': 0,
            'cnt': 10,
            'list':
                [{'dt': 1710633600, 'main': {'temp': 8.35, 'feels_like': 4.87, 'temp_min': 7.88, 'temp_max': 8.35, 'pressure': 1001, 'sea_level': 1001, 'grnd_level': 989, 'humidity': 73, 'temp_kf': 0.47}, 'weather': [{'id': 500, 'main': 'Rain', 'description': 'light rain', 'icon': '10n'}], 'clouds': {'all': 100}, 'wind': {'speed': 6.85, 'deg': 251, 'gust': 14.66}, 'visibility': 10000, 'pop': 0.74, 'rain': {'3h': 1.42}, 'sys': {'pod': 'n'}, 'dt_txt': '2024-03-17 00:00:00'},
                 {'dt': 1710644400, 'main': {'temp': 8.02, 'feels_like': 5.01, 'temp_min': 7.74, 'temp_max': 8.02, 'pressure': 999, 'sea_level': 999, 'grnd_level': 988, 'humidity': 68, 'temp_kf': 0.28}, 'weather': [{'id': 500, 'main': 'Rain', 'description': 'light rain', 'icon': '10n'}], 'clouds': {'all': 100}, 'wind': {'speed': 5.25, 'deg': 258, 'gust': 10.08}, 'visibility': 10000, 'pop': 0.49, 'rain': {'3h': 0.24}, 'sys': {'pod': 'n'}, 'dt_txt': '2024-03-17 03:00:00'},
                 {'dt': 1710655200, 'main': {'temp': 4.82, 'feels_like': 1.05, 'temp_min': 4.82, 'temp_max': 4.82, 'pressure': 1000, 'sea_level': 1000, 'grnd_level': 989, 'humidity': 81, 'temp_kf': 0}, 'weather': [{'id': 500, 'main': 'Rain', 'description': 'light rain', 'icon': '10n'}], 'clouds': {'all': 86}, 'wind': {'speed': 5.12, 'deg': 288, 'gust': 9.06}, 'visibility': 10000, 'pop': 0.51, 'rain': {'3h': 0.26}, 'sys': {'pod': 'n'}, 'dt_txt': '2024-03-17 06:00:00'},
                 {'dt': 1710666000, 'main': {'temp': 3.89, 'feels_like': -0.07, 'temp_min': 3.89, 'temp_max': 3.89, 'pressure': 1000, 'sea_level': 1000, 'grnd_level': 990, 'humidity': 73, 'temp_kf': 0}, 'weather': [{'id': 500, 'main': 'Rain', 'description': 'light rain', 'icon': '10n'}], 'clouds': {'all': 56}, 'wind': {'speed': 5.04, 'deg': 280, 'gust': 9.48}, 'visibility': 10000, 'pop': 0.22, 'rain': {'3h': 0.11}, 'sys': {'pod': 'n'}, 'dt_txt': '2024-03-17 09:00:00'},
                 {'dt': 1710676800, 'main': {'temp': 3.1, 'feels_like': -1.62, 'temp_min': 3.1, 'temp_max': 3.1, 'pressure': 1002, 'sea_level': 1002, 'grnd_level': 991, 'humidity': 68, 'temp_kf': 0}, 'weather': [{'id': 600, 'main': 'Snow', 'description': 'light snow', 'icon': '13d'}], 'clouds': {'all': 54}, 'wind': {'speed': 6.25, 'deg': 265, 'gust': 10.56}, 'visibility': 10000, 'pop': 0.28, 'snow': {'3h': 0.1}, 'sys': {'pod': 'd'}, 'dt_txt': '2024-03-17 12:00:00'},
                 {'dt': 1710687600, 'main': {'temp': 4.46, 'feels_like': -0.18, 'temp_min': 4.46, 'temp_max': 4.46, 'pressure': 1002, 'sea_level': 1002, 'grnd_level': 992, 'humidity': 53, 'temp_kf': 0}, 'weather': [{'id': 802, 'main': 'Clouds', 'description': 'scattered clouds', 'icon': '03d'}], 'clouds': {'all': 30}, 'wind': {'speed': 7, 'deg': 266, 'gust': 10.09}, 'visibility': 10000, 'pop': 0.04, 'sys': {'pod': 'd'}, 'dt_txt': '2024-03-17 15:00:00'},
                 {'dt': 1710698400, 'main': {'temp': 5, 'feels_like': 0.39, 'temp_min': 5, 'temp_max': 5, 'pressure': 1002, 'sea_level': 1002, 'grnd_level': 992, 'humidity': 50, 'temp_kf': 0}, 'weather': [{'id': 803, 'main': 'Clouds', 'description': 'broken clouds', 'icon': '04d'}], 'clouds': {'all': 65}, 'wind': {'speed': 7.36, 'deg': 267, 'gust': 10.37}, 'visibility': 10000, 'pop': 0, 'sys': {'pod': 'd'}, 'dt_txt': '2024-03-17 18:00:00'},
                 {'dt': 1710709200, 'main': {'temp': 4.7, 'feels_like': -0.13, 'temp_min': 4.7, 'temp_max': 4.7, 'pressure': 1003, 'sea_level': 1003, 'grnd_level': 992, 'humidity': 47, 'temp_kf': 0}, 'weather': [{'id': 804, 'main': 'Clouds', 'description': 'overcast clouds', 'icon': '04d'}], 'clouds': {'all': 98}, 'wind': {'speed': 7.74, 'deg': 276, 'gust': 10.52}, 'visibility': 10000, 'pop': 0, 'sys': {'pod': 'd'}, 'dt_txt': '2024-03-17 21:00:00'},
                 {'dt': 1710720000, 'main': {'temp': 3.06, 'feels_like': -1.64, 'temp_min': 3.06, 'temp_max': 3.06, 'pressure': 1005, 'sea_level': 1005, 'grnd_level': 994, 'humidity': 55, 'temp_kf': 0}, 'weather': [{'id': 804, 'main': 'Clouds', 'description': 'overcast clouds', 'icon': '04n'}], 'clouds': {'all': 91}, 'wind': {'speed': 6.16, 'deg': 282, 'gust': 11.13}, 'visibility': 10000, 'pop': 0.02, 'sys': {'pod': 'n'}, 'dt_txt': '2024-03-18 00:00:00'},
                 {'dt': 1710730800, 'main': {'temp': 1.39, 'feels_like': -3.68, 'temp_min': 1.39, 'temp_max': 1.39, 'pressure': 1005, 'sea_level': 1005, 'grnd_level': 994, 'humidity': 62, 'temp_kf': 0}, 'weather': [{'id': 801, 'main': 'Clouds', 'description': 'few clouds', 'icon': '02n'}], 'clouds': {'all': 13}, 'wind': {'speed': 5.99, 'deg': 277, 'gust': 10.93}, 'visibility': 10000, 'pop': 0, 'sys': {'pod': 'n'}, 'dt_txt': '2024-03-18 03:00:00'}],
            'city': {'id': 6167863, 'name': 'Downtown Toronto', 'coord': {'lat': 43.6532, 'lon': -79.3832}, 'country': 'CA', 'population': 0, 'timezone': -14400, 'sunrise': 1710588427, 'sunset': 1710631499}}
           , {
               "coord":[
                   50,
                   50
               ],
               "list":[
                   {
                       "dt":1605182400,
                       "main":{
                           "aqi":1
                       },
                       "components":{
                           "co":201.94053649902344,
                           "no":0.01877197064459324,
                           "no2":0.7711350917816162,
                           "o3":68.66455078125,
                           "so2":0.6407499313354492,
                           "pm2_5":0.5,
                           "pm10":0.540438711643219,
                           "nh3":0.12369127571582794
                       }
                   }
               ]
           })
"""
