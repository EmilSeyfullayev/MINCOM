import streamlit as st
import pandas as pd
import numpy as np
import sqlite3


@st.cache(ttl=60*60*24)
def read_data_tir_ceki():
    df = pd.read_excel("Avtomobil yollari 2019-2022.xlsx", sheet_name='''Çəki (ton)''')
    df = df.iloc[:-3, :]
    df['Cemi_min_ton'] = df['Cəm']/1000
    df['From'] = df['Hərəkətin marşrutu'].apply(lambda x: x.split("-")[0])
    df['To'] = df['Hərəkətin marşrutu'].apply(lambda x: x.split("-")[1])

    return df

# aggregated = 'Cəm'
# aggregated = 'Cemi_min_ton'


country_selected = st.sidebar.selectbox("Seçilmiş ölkə")
