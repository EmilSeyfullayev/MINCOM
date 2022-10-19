import streamlit as st
import sqlite3
import pandas as pd
import datetime
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('whitegrid')


@st.cache(ttl=60*60*24)
def read_data():
    connection = sqlite3.connect('transit_2019_2022_8Months.db')
    data = pd.read_sql(''' select * from 'transit_data' ''', connection)
    data['DATESIGN'] = pd.to_datetime(data['DATESIGN']).dt.date
    data['FROMTO'] = data['From'] + " - " + data['To']
    column_names = [
        "Mənsubiyyət ölkəsi",
        "Gömrük orqanı",
        "Malın çəkisi (tonla)",
        "Marşrutun başlanğıcı",
        "Marşrutun təyinatı",
        "NV-nin nömrəsi",
        "Tarix",
        "Ödənilən məbləğ",
        "Hərəkətin marşrutu"
    ]

    data['FROMTO'] = data['From'] + " - " + data['To']
    data.columns = column_names
    data['İl'] = data['Tarix'].apply(lambda x: x.year)
    return data


df = read_data()


@st.cache
def unique_countries():
    values1 = df["Marşrutun başlanğıcı"].unique()
    values2 = df["Marşrutun təyinatı"].unique()
    values = sorted(set(np.concatenate((values1, values2))))
    return values


unique_countries_values = unique_countries()
country = st.sidebar.selectbox("Ölkəni seçin", unique_countries_values, index=75)


pivot1 = (pd.pivot_table(
    df[df['Marşrutun başlanğıcı'] == country],
    columns=["İl"],
    values="Malın çəkisi (tonla)",
    aggfunc="sum"
)/1000)

st.dataframe(pivot1)
