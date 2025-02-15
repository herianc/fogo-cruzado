import os

import pandas as pd
import streamlit as st
from dotenv import load_dotenv

st.set_page_config(layout="wide")

st.logo("assets/fg_black.png")


if "dataframes" not in st.session_state:
    with st.spinner("⏳️ Carregando a base de dados..."):
        st.session_state["ocorrencias"] = pd.read_csv("data/ocorrencias.csv")
        st.session_state["vitimas"] = pd.read_csv("data/vitimas.csv")
        st.session_state["dataframes"] = True

if "credentials" not in st.session_state:
    st.session_state["credentials"] = True
    load_dotenv()


index = st.Page(page="views/1_index.py", icon=":material/home:", title="Home")

dashboard = st.Page(
    page="views/2_dash.py", icon=":material/analytics:", title="Dashboard"
)

pages = {"Páginas": [index, dashboard]}

pg = st.navigation(pages)
pg.run()
