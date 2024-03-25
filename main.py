import streamlit as st
import pandas as pd
import WeatherData
import LatLongData
import Graphs
import APIkeys
import datetime


def window():

    st.markdown("<h1 style='color: white; font-family: Arial, sans-serif; font-size: 56px;'>Weather Data</h1>", unsafe_allow_html=True)

    # Sidebar
    st.sidebar.header('Settings')
    address = st.sidebar.text_input('Pick A Place')

    graphs = None

    if address:

        geocode = LatLongData.Geocode(APIkeys.Geocode_Key)
        weatherapi = WeatherData.WeatherApi(APIkeys.weather_key)

        try:
            long_lat = geocode.get_long_lat(address)
            weather_data = weatherapi.get_weather(long_lat)
            air_data = weatherapi.get_air(long_lat)
            graphs = Graphs.Graphs(weather_data, air_data)
            valid = True
        except KeyError:
            valid = False
            st.write("Please enter a more specific address")

        st.write(" ")
        st.markdown(f"<h2 style='color: white; font-family: Arial, sans-serif; font-size: 38px;'>Location {graphs.weather_data['city']['name']}, {graphs.weather_data['city']['country']}</h2>", unsafe_allow_html=True)

        # General Information Section

        information_container = st.container()

        with information_container:
            col1, col2 = st.columns(2)

            with col1:
                latitude = graphs.weather_data["city"]["coord"]["lat"]
                if latitude > 0:
                    lat_direction = " North"
                else:
                    lat_direction = " South"
                    latitude *= -1

                st.metric(label="Latitude", value=str(latitude) + "°" + lat_direction)

                sunrise = graphs.weather_data['city']['sunrise']
                sunrise = datetime.datetime.fromtimestamp(sunrise)
                sunrise_readable = sunrise.strftime("%Y-%m-%d %H:%M:%S")

                st.metric(label="Sunrise", value=sunrise_readable)

            with col2:
                longitude = graphs.weather_data["city"]["coord"]["lon"]
                if longitude > 0:
                    long_direction = " East"
                else:
                    long_direction = " West"
                    longitude *= -1

                st.metric(label="Longitude", value=str(longitude) + "°" + long_direction)

                sunset = graphs.weather_data['city']['sunset']
                sunset = datetime.datetime.fromtimestamp(sunset)
                sunset_readable = sunset.strftime("%Y-%m-%d %H:%M:%S")

                st.metric(label="Sunset", value=sunset_readable)

            # timezone from UTC

            offset_seconds = graphs.weather_data["city"]["timezone"]
            offset_hours = offset_seconds // 3600
            offset_minutes = (offset_seconds % 3600) // 60

            if offset_seconds < 0:
                offset_state = "behind"
            else:
                offset_state = "ahead"

            st.subheader(f"{abs(offset_hours):02d} hr and {abs(offset_minutes):02d} min {offset_state} UTC (Universal Time Coordinated)")
            st.subheader(f"Main Condition: {graphs.weather_data['list'][0]['weather'][0]['main']}, {graphs.weather_data['list'][0]['weather'][0]['description']}")

        st.write(" ")
        st.write(" ")

        # Temperature Section

        temperature_container = st.container()

        with temperature_container:
            col1, col2, col3, col4 = st.columns(4)

            st.pyplot(graphs.plot_temp())

            with col1:
                st.markdown(f"<h2 style='color: white; font-family: Arial, sans-serif; font-size: 38px;'>Temperature</h2>", unsafe_allow_html=True)
                st.metric(label="Current Temperature", value=f"{graphs.temperature_data[0][0]} °C")
            with col2:
                st.markdown(f"<h2 style='color: #0E1117; font-family: Arial, sans-serif; font-size: 38px;'>_</h2>", unsafe_allow_html=True)
                st.metric(label="Minimum Temperature", value=f"{graphs.temperature_data[0][1]} °C")
            with col3:
                st.markdown(f"<h2 style='color: #0E1117; font-family: Arial, sans-serif; font-size: 38px;'>.</h2>", unsafe_allow_html=True)
                st.metric(label="Maximum Temperature", value=f"{graphs.temperature_data[0][2]} °C")
            with col4:
                st.markdown(f"<h2 style='color: #0E1117; font-family: Arial, sans-serif; font-size: 38px;'>.</h2>", unsafe_allow_html=True)
                st.metric(label="Feels Like", value=f"{graphs.temperature_data[0][3]} °C")

            st.subheader("Temperature Data")

            temp_data = pd.DataFrame(graphs.temperature_data, columns=["Average (°C)", "Min (°C)", "Max (°C)", "Feels Like (°C)"])
            temp_data = temp_data.transpose()
            temp_data_styled = temp_data.style.format("{:.2f}")
            st.table(temp_data_styled)

        st.write(" ")
        st.write(" ")

        # rain and snow section

        precipitation_container = st.container()

        with precipitation_container:
            col1, col2, col3 = st.columns(3)

            st.pyplot(graphs.plot_rain_snow())
            st.pyplot(graphs.rain_snow_prob())

            with col1:
                st.markdown(f"<h2 style='color: white; font-family: Arial, sans-serif; font-size: 38px;'>Precipitation</h2>", unsafe_allow_html=True)
                st.metric(label="Current Rain Amount", value=f"{graphs.rains[0][0]} mm")
            with col2:
                st.markdown(f"<h2 style='color: #0E1117; font-family: Arial, sans-serif; font-size: 38px;'>.</h2>", unsafe_allow_html=True)
                st.metric(label="Current Snow Amount", value=f"{graphs.snows[0][0]} mm")
            with col3:
                st.markdown(f"<h2 style='color: #0E1117; font-family: Arial, sans-serif; font-size: 38px;'>.</h2>", unsafe_allow_html=True)
                st.metric(label="Probability of Precipitation", value=f"{graphs.rains[0][1]} %")

            st.subheader("Rain Data")
            rain_data = pd.DataFrame(graphs.rains, columns=["mm", "Probability"])
            rain_data = rain_data.transpose()
            rain_data = rain_data.style.format("{:.2f}")
            st.table(rain_data)

            st.subheader("Snow Data")
            snow_data = pd.DataFrame(graphs.snows, columns=["mm", "Probability"])
            snow_data = snow_data.transpose()
            snow_data = snow_data.style.format("{:.2f}")
            st.table(snow_data)

        st.write(" ")
        st.write(" ")

        # Humidity Section

        humidity_container = st.container()

        with humidity_container:
            st.markdown(f"<h2 style='color: white; font-family: Arial, sans-serif; font-size: 38px;'>Humidity</h2>", unsafe_allow_html=True)
            st.pyplot(graphs.humidity_chart())

            st.subheader("Humidity Data")
            humidity_data = pd.DataFrame(graphs.humidity, columns=["Humidity %"])
            humidity_data = humidity_data.transpose()
            humidity_data = humidity_data.style.format("{:.2f}")
            st.table(humidity_data)

        st.write(" ")
        st.write(" ")

        # Pressure Section

        pressure_container = st.container()

        with pressure_container:
            st.markdown(f"<h2 style='color: white; font-family: Arial, sans-serif; font-size: 38px;'>Pressure</h2>", unsafe_allow_html=True)
            st.pyplot(graphs.plot_pressure())

            st.subheader("Ground Pressure and Sea Pressure Data")
            pressure_data = pd.DataFrame(graphs.pressure_data, columns=["Sea Level in Hectopascals (hPa) ", "Ground Level in Hectopascals (hPa)"])
            pressure_data = pressure_data.transpose()
            pressure_data = pressure_data.style.format("{:.2f}")
            st.table(pressure_data)

        st.write(" ")
        st.write(" ")
        st.markdown(f"<h2 style='color: white; font-family: Arial, sans-serif; font-size: 38px;'>Clouds and Wind</h2>", unsafe_allow_html=True)
        # Wind and cloud section

        cloud_wind_container = st.container()

        with cloud_wind_container:
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric(label="Cloudiness", value=f"{graphs.clouds[0]} %")

            with col2:
                st.metric(label="Visibility (max = 10km)", value=f"{graphs.weather_data['list'][0]['visibility']} m")

            with col3:
                st.metric(label="Wind Speed", value=f"{graphs.wind_speed[0]} m/s")

            with col4:
                st.metric(label="Wind Direction", value=f"{graphs.get_wind_direction()} ({graphs.weather_data['list'][0]['wind']['deg']}°)")

            st.pyplot(graphs.cloudiness())

            st.subheader("Cloudiness Data")
            cloud_data = pd.DataFrame(graphs.clouds, columns=["Cloudiness in %"])
            cloud_data = cloud_data.transpose()
            cloud_data = cloud_data.style.format("{:.2f}")
            st.table(cloud_data)

            st.pyplot(graphs.wind_speed_graph())

            st.subheader("Wind Speed Data")
            wind_data = pd.DataFrame(graphs.wind_speed, columns=["Wind Speed in m/s"])
            wind_data = wind_data.transpose()
            wind_data = wind_data.style.format("{:.2f}")
            st.table(wind_data)

        st.write(" ")
        st.write(" ")

        # Air Pollution Section

        air_pollution_container = st.container()

        with air_pollution_container:
            col1, col2 = st.columns(2)

            with col1:
                st.markdown(f"<h2 style='color: white; font-family: Arial, sans-serif; font-size: 38px;'>Air Quality</h2>", unsafe_allow_html=True)
                st.metric(label="Air Quality Index", value=graphs.air_data["list"][0]["main"]["aqi"])

            # air quality scale

            air_quality_scale_data = [1, 2, 3, 4, 5]
            air_quality_scale_score = ["Good", "Fair", "Moderate", "Poor", "Very Poor"]
            air_quality_scale = pd.DataFrame(air_quality_scale_data, index=air_quality_scale_score, columns=["Air Quality Score"])
            air_quality_scale = air_quality_scale.transpose()
            st.table(air_quality_scale)

            st.pyplot(graphs.air_bar_graph())

            # components legend

            air_component_meanings = [
                "Carbon Monoxide",
                "Nitrogen Monoxide",
                "Nitrogen Dioxide",
                "Ozone",
                "Sulphur Dioxide",
                "Fine Particle Matter",
                "Course Particulate Matter",
                "Ammonia"
            ]

            st.subheader("Composition of Air")
            air_components = pd.DataFrame(graphs.air_data_pollutants, index=air_component_meanings, columns=["Shortened Form"])
            st.table(air_components)

            # Pollutant contents table
            st.subheader("Air Pollutant Data")
            pollutant_data = pd.DataFrame(graphs.air_data_concentration, index=graphs.air_data_pollutants, columns=["Concentration in Micrograms per Cubic Meter (μg/m3)"])
            pollutant_data = pollutant_data.transpose()
            pollutant_data = pollutant_data.style.format("{:.2f}")
            st.table(pollutant_data)


if __name__ == "__main__":
    window()
