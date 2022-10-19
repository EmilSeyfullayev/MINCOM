import streamlit as st
import sqlite3
import pandas as pd
from ady_functions import *
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
sns.set_style('whitegrid')

st.header("Seçilmiş ölkə üzrə Dəmiryolları ilə daşınan tranzit yüklər haqqında məlumat")
df = read_ady_data()[0]
max_month = df['Tarix'].max().month
countries = read_ady_data()[1]
selected_country = st.sidebar.selectbox("Seçilmiş ölkə", countries, 0)
index = st.sidebar.selectbox("Bölgünü seçin", ['Dəhliz', 'Yük qrupu (ümumi bölgü)'], 0)
dovriyye_dehlizler = dehlizler_uzre_dovriyye(df, selected_country, index)
dovriyye_dehlizler_gonderen = dehlizler_uzre_gonderen(df, selected_country, index)
dovriyye_dehlizler_teyinat = dehlizler_uzre_teyinat(df, selected_country, index)


def show_dehlizler_uzre_dovriyye(data_to_show):
    data_to_show = data_to_show.fillna(0)
    if str(datetime.datetime.today().year)+"*" in data_to_show.columns:
        st.dataframe(data_to_show)
        st.write(f"*Qeyd: ilk {max_month} ay")
    else:
        st.dataframe(data_to_show)


st.write("**Yüklərin ümumi dövriyyəsi**")
show_dehlizler_uzre_dovriyye(dovriyye_dehlizler)


def show_dehlizler_uzre_gonderen(data_to_show):
    data_to_show = data_to_show.fillna(0)
    if str(datetime.datetime.today().year)+"*" in data_to_show.columns:
        st.dataframe(data_to_show)
        st.write(f"*Qeyd: ilk {max_month} ay")
    else:
        st.dataframe(data_to_show)


st.write(f"**Yüklərin daşınması, göndərən ölkə - {selected_country}**")
show_dehlizler_uzre_dovriyye(dovriyye_dehlizler_gonderen)


def show_dehlizler_uzre_teyinat(data_to_show):
    data_to_show = data_to_show.fillna(0)
    if str(datetime.datetime.today().year)+"*" in data_to_show.columns:
        st.dataframe(data_to_show)
        st.write(f"*Qeyd: ilk {max_month} ay")
    else:
        st.dataframe(data_to_show)


st.write(f"**Yüklərin daşınması, təyinat ölkəsi - {selected_country}**")
show_dehlizler_uzre_teyinat(dovriyye_dehlizler_teyinat)
