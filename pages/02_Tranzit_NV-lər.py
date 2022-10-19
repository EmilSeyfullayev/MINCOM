import streamlit as st
import pandas as pd
import numpy as np
import sqlite3
from tir_functions import *

# our data and inputs for sidebar selectboxes
tr = read_transit_data()
countries_array = unique_countries_array(tr=tr)
months = monthes_list()
# our sidebar
selected_country = st.sidebar.selectbox("Ölkəni seçin", options=countries_array,
                                        index=countries_array.index("Türkiyə"))
selected_month = st.sidebar.selectbox("İlk neçə ay?", options=months, index=8)

# Our pivot dataframes
sum_pivot = tir_pivot_sum(tr, country_name=selected_country, max_month=selected_month)
count_pivot = tir_pivot_count(tr, country_name=selected_country, max_month=selected_month)

# Show output
st.subheader(f"{selected_country} ölkəsi üzrə ilk {selected_month} ay avtomobil yolu ilə tranzit daşımaların həcmi")
st.dataframe(sum_pivot, use_container_width=True)
st.subheader(f"{selected_country} ölkəsi üzrə ilk {selected_month} ay avtomobil yolu ilə tranzit TIRların sayı")
st.dataframe(count_pivot, use_container_width=True)
