import streamlit as st
import requests
import folium
from streamlit_folium import folium_static

st.title("Прогноз температуры в Таиланде")

st.write("""
Это приложение использует модель машинного обучения для прогнозирования температуры на основе координаты и времени.
""")

st.header("Введите данные")
date = st.text_input("Дата", value='2023-03-01')
latitude = st.number_input("Широта", value=14.0)
longitude = st.number_input("Долгота", value=101.5)

if st.button("Получить прогноз"):
    data = {
        "date": date,
        "latitude": latitude,
        "longitude": longitude
    }

    try:
        response = requests.post(
            "http://0.0.0.0:8000/predict/",  # Ваш публичный URL
            json=data
        )
        response.raise_for_status()

        prediction = response.json()["prediction"]
        st.success(f"Температура {prediction:.2f} в {data['latitude']:.2f} {data['longitude']:.2f}")

        m = folium.Map(location=[latitude, longitude], zoom_start=12)

        folium.Marker(
            location=[latitude, longitude],
            popup="Текущее местоположение",
            icon=folium.Icon(color="blue")
        ).add_to(m)

        folium.Marker(
            location=[latitude, longitude + 0.01],
            popup=f"Температура: {prediction:.2f}",
            icon=folium.Icon(color="red")
        ).add_to(m)

        # Отображение карты в Streamlit
        folium_static(m)

    except requests.exceptions.RequestException as e:
        st.error(f"Ошибка при отправке запроса: {e}")
    except ValueError as e:
        st.error(f"Ошибка при обработке ответа: {e}")