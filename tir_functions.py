import streamlit as st
import pandas as pd
import numpy as np
import sqlite3

CUST_NAME = "Gömrük postu"
DATESIGN = "Yazılma tarixi"
PERMISSION_PRICE = "Ödənilən məbləğ"
From = "Göndərən ölkə"
To = "Təyinat ölkəsi"
Avto_number = "Nəqliiyat vasitəsinin nömrəsi"
WEIGHT_THOUSAND_TONS = "Çəki (min tonla)"
Year = "İl üzrə"
Month = "Ay üzrə"
Count = "NV-lərin sayı"


@st.cache(ttl=30*60*60*24)
def read_transit_data():
    new_month = 'September'
    connection = sqlite3.connect(f'{new_month}_tir_transit.db')
    tr = pd.read_sql(''' select * from 'tir_transit' ''', connection)
    tr['DATESIGN'] = pd.to_datetime(tr['DATESIGN'])
    tr['Year'] = tr['DATESIGN'].apply(lambda x: x.year)
    tr['Month'] = tr['DATESIGN'].apply(lambda x: x.month)
    tr['Count'] = 1

    column_names = {
        'CUST_NAME': "Gömrük postu",
        'DATESIGN': "Yazılma tarixi",
        'PERMISSION_PRICE': "Ödənilən məbləğ",
        'From': "Göndərən ölkə",
        'To': "Təyinat ölkəsi",
        'Avto_number': "Nəqliiyat vasitəsinin nömrəsi",
        'WEIGHT_THOUSAND_TONS': "Çəki (min tonla)",
        'Year': "İl üzrə",
        'Month': "Ay üzrə",
        'Count': "NV-lərin sayı"}

    tr.rename(columns=column_names, inplace=True)

    return tr


def tir_pivot_sum(df, country_name, max_month):
    df = df[df[Month] <= max_month]

    pivot_table_from = pd.pivot_table(
        df[df[From] == country_name],
        columns=Year,
        values=WEIGHT_THOUSAND_TONS,
        aggfunc="sum")
    pivot_table_from = pivot_table_from.rename(index={"Çəki (min tonla)":
                                                          "Ölkədən - Çəki (min tonla)"})

    pivot_table_to = pd.pivot_table(
        df[df[To] == country_name],
        columns=Year,
        values=WEIGHT_THOUSAND_TONS,
        aggfunc="sum")
    pivot_table_to = pivot_table_to.rename(index={"Çəki (min tonla)":
                                                      "Ölkəyə - Çəki (min tonla)"})
    pivot_table = pd.concat([pivot_table_from,
                             pivot_table_to], axis=0)
    pivot_table.loc['Cəmi:'] = pivot_table.sum(numeric_only=True, axis=0)
    return pivot_table


def tir_pivot_count(df, country_name, max_month):
    df = df[df[Month] <= max_month]

    pivot_table_from = pd.pivot_table(
        df[df[From] == country_name],
        columns=Year,
        values=Count,
        aggfunc="sum")
    pivot_table_from = pivot_table_from.rename(index={"NV-lərin sayı":
                                                          "Ölkədən - NV-lərin sayı"})

    pivot_table_to = pd.pivot_table(
        df[df[To] == country_name],
        columns=Year,
        values=Count,
        aggfunc="sum")
    pivot_table_to = pivot_table_to.rename(index={"NV-lərin sayı":
                                                      "Ölkəyə - NV-lərin sayı"})
    pivot_table = pd.concat([pivot_table_from,
                             pivot_table_to], axis=0)
    pivot_table.loc['Cəmi:'] = pivot_table.sum(numeric_only=True, axis=0)
    return pivot_table


@st.cache(ttl=30*60*60*24)
def unique_countries_array(tr):
    unique_countries_1 = tr[From].unique()
    unique_countries_2 = tr[To].unique()
    array = np.unique(np.concatenate([unique_countries_1, unique_countries_2]))
    return sorted(list(array))


@st.cache()
def monthes_list():
    return [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

