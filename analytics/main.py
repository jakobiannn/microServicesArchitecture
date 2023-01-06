import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
import data_frames

st.header("""Аналитика работы веб-сервиса""")

st.sidebar.header('Ввод данных')


def user_input_features():
    data_length = st.sidebar.slider('Глубина анализа, день', 1, 30, 3)
    interval_width = st.sidebar.slider('Интервал анализа, час', 1, 24, 24)
    proc_type = st.sidebar.text_input("Тип операции", 'ping')
    data = {'data_length': data_length,
            'interval_width': interval_width,
            'proc_type': proc_type}
    features = pd.DataFrame(data, index=[0])
    return features


df = user_input_features()

count_all = data_frames.load_count_by_type()

st.subheader('Количество вызовов операций по их типу')
st.bar_chart(count_all, x='TYPE')

count_by_time = data_frames.load_count_by_time(df)
st.subheader('Количество вызовов операций с выборкой по времени')
st.bar_chart(count_by_time, x='HOUR', y='COUNT')

st.subheader('Диаграмма по количеству операций')
fig1, ax1 = plt.subplots()
ax1.pie(count_all['COUNT'], labels=count_all['TYPE'], autopct='%1.1f%%',
        shadow=True, startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
st.pyplot(fig1)

st.subheader('Диаграмма по времени выполнения операций')
df_duration = data_frames.log_avg_duration()
fig1, ax1 = plt.subplots()
ax1.pie(df_duration['DURATION'], labels=df_duration['TYPE'], autopct='%1.1f%%',
        shadow=True, startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
st.pyplot(fig1)
