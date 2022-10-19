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
    return data


df = read_data()
st.dataframe(df.head(1))

@st.cache
def hereket_baslangic():
    values = df["Marşrutun başlanğıcı"].unique()
    return values


@st.cache
def date():
    return df['Tarix'].max(), df['Tarix'].min()


tarix_values = date()
tarix_max = tarix_values[0]
tarix_min = tarix_values[1]
tarix1 = st.sidebar.date_input("Başlanğıc tarixi",
                               value=tarix_min,
                               min_value=tarix_min,
                               max_value=tarix_max)
tarix2 = st.sidebar.date_input("Bitmə tarixi",
                              value=tarix_max,
                              min_value=tarix1,
                              max_value=tarix_max)

hereket_baslangic_values = hereket_baslangic()
hereket_baslangic_selected = st.sidebar.selectbox("Hərəkət marşrutu üzrə başlanğıc",
                                                  hereket_baslangic_values)

filtered_data = df[
    (df["Marşrutun başlanğıcı"] == hereket_baslangic_selected)]


def hereket_teyinat():
    values = filtered_data["Marşrutun təyinatı"].unique()
    return values


hereket_teyinat_values = hereket_teyinat()
hereket_teyinat_selected = st.sidebar.selectbox("Hərəkət marşrutu üzrə təyinat", hereket_teyinat_values)
filtered_data = filtered_data[
    (df["Marşrutun təyinatı"] == hereket_teyinat_selected) &
    (df['Tarix'] >= tarix1) &
    (df['Tarix'] <= tarix2)]


def gomruk_orqani():
    return filtered_data["Gömrük orqanı"].unique()


gomruk_orqanlari_values = gomruk_orqani()
gomruk = st.sidebar.selectbox(
    "Gömrük orqanları",
    gomruk_orqanlari_values
)

filtered_data = filtered_data[(filtered_data['Gömrük orqanı'] == gomruk)].reset_index(drop=True)


col1, col2, col3 = st.columns(3)

col1.metric("Tranzit NV-lərin sayı", filtered_data.shape[0], 500)
col2.metric("Ödənilən məbləğ", round(filtered_data["Ödənilən məbləğ"].sum()), 500)
col3.metric("Malın çəkisi (tonla)", round(filtered_data['Malın çəkisi (tonla)'].sum()), 500)

st.dataframe(filtered_data[["Mənsubiyyət ölkəsi",
    "Malın çəkisi (tonla)",
    "NV-nin nömrəsi",
    "Tarix",
    "Ödənilən məbləğ"]])
