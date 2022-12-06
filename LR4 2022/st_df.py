import streamlit as st
import pandas as pd
from sklearn import datasets


st.write("""
# Аналитика работы веб-сервиса
""")

st.sidebar.header('Ввод данных')

def user_input_features():
    data_length = st.sidebar.slider('Глубина анализа, день', 1, 30, 3)
    interval_width = st.sidebar.slider('Интервал анализа, час', 1, 24, 4)
    proc_type = st.sidebar.text_input("Тип операции")
    data = {'data_length': data_length,
            'interval_width': interval_width,
            'proc_type': proc_type}
    features = pd.DataFrame(data, index=[0])
    return features

df = user_input_features()

@st.cache
def load_dataset():
    dataset = pd.read_csv('log.csv', header=0, sep=',')
    return dataset

def flt_dataset(df, flt_df):
    op_type = flt_df.iloc[0]['proc_type']
    dataset = df.loc[df['op_type'] == op_type]
    return dataset

log_data = load_dataset()

flt_data = flt_dataset(log_data, df)

st.subheader('Введенные данные')
st.write(df)

st.subheader('Все данные лог-файлов')
st.write(log_data)

st.subheader('Отобранные данные лог-файлов')
st.write(flt_data)