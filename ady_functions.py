import streamlit as st
import pandas as pd
import numpy as np
import sqlite3


@st.cache(ttl=30*60*60*24)
def read_ady_data():
    connection = sqlite3.connect('transit_ady_2017_2022_8Months.db')
    df = pd.read_sql(''' select * from 'transit_data_ady' ''', connection)
    df['Tarix'] = pd.to_datetime(df['Tarix'])
    df['İl üzrə'] = df['Tarix'].dt.year
    df['Ay üzrə'] = df['Tarix'].dt.month
    sixty_countries_gonderen = df['Göndərən ölkə'].value_counts().head(60).index
    sixty_countries_teyinat = df['Təyinat ölkə'].value_counts().head(60).index
    not_common_countries = [i for i in sixty_countries_teyinat if i not in sixty_countries_gonderen]
    unique_countries = np.concatenate([sixty_countries_gonderen, not_common_countries])
    unique_countries = np.extract((unique_countries != '№3-cü ölkələr'), unique_countries)
    unique_countries = np.extract((unique_countries != 'Digər'), unique_countries)
    df = df[
        (df['Göndərən ölkə'].isin(unique_countries)) |
        (df['Təyinat ölkə'].isin(unique_countries))
        ]

    return df, unique_countries


def dehlizler_uzre_dovriyye(df, country_name, index):
    df = df[(df['Göndərən ölkə'].str.contains(country_name)) |
            (df['Təyinat ölkə'].str.contains(country_name))]
    full_year = (pd.pivot_table(df,
                                index=index,
                                columns='İl üzrə',
                                values="Ton",
                                aggfunc='sum') / 1000).reset_index()
    try:
        max_month = df['Tarix'].max().month

        eight_month = (pd.pivot_table(df[df['Ay üzrə'] <= max_month],
                                      index=index,
                                      columns='İl üzrə',
                                      values="Ton",
                                      aggfunc='sum') / 1000).reset_index()
        full_year['2021*'] = eight_month[2021]
        full_year = full_year[[
            index, 2017, 2018, 2019, 2020, 2021, '2021*', 2022
        ]].sort_values(2022, ascending=False).reset_index(drop=True)
        full_year.columns = [index, '2017', '2018', '2019', '2020', '2021', '2021*', '2022*']

        return full_year
    except KeyError:
        return full_year


def dehlizler_uzre_gonderen(df, country_name, index):
    df = df[df['Göndərən ölkə'].str.contains(country_name)]
    full_year = (pd.pivot_table(df,
                                index=index,
                                columns='İl üzrə',
                                values="Ton",
                                aggfunc='sum') / 1000).reset_index()
    try:
        max_month = df['Tarix'].max().month

        eight_month = (pd.pivot_table(df[df['Ay üzrə'] <= max_month],
                                      index=index,
                                      columns='İl üzrə',
                                      values="Ton",
                                      aggfunc='sum') / 1000).reset_index()
        full_year['2021*'] = eight_month[2021]
        full_year = full_year[[
            index, 2017, 2018, 2019, 2020, 2021, '2021*', 2022
        ]].sort_values(2022, ascending=False).reset_index(drop=True)
        full_year.columns = [index, '2017', '2018', '2019', '2020', '2021', '2021*', '2022*']

        return full_year
    except KeyError:
        return full_year


def dehlizler_uzre_teyinat(df, country_name, index):
    df = df[df['Təyinat ölkə'].str.contains(country_name)]
    full_year = (pd.pivot_table(df,
                                index=index,
                                columns='İl üzrə',
                                values="Ton",
                                aggfunc='sum') / 1000).reset_index()
    try:
        max_month = df['Tarix'].max().month

        eight_month = (pd.pivot_table(df[df['Ay üzrə'] <= max_month],
                                      index=index,
                                      columns='İl üzrə',
                                      values="Ton",
                                      aggfunc='sum') / 1000).reset_index()
        full_year['2021*'] = eight_month[2021]
        full_year = full_year[[
            index, 2017, 2018, 2019, 2020, 2021, '2021*', 2022
        ]].sort_values(2022, ascending=False).reset_index(drop=True)
        full_year.columns = [index, '2017', '2018', '2019', '2020', '2021', '2021*', '2022*']

        return full_year
    except KeyError:
        return full_year
