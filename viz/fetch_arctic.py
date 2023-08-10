import os
from arcticdb import Arctic
from dotenv import load_dotenv
import streamlit as st
from arcticdb.version_store.library import ArcticException
load_dotenv()
AC = Arctic(os.getenv('lmdb'))
graph_types = [
    'seasonal',
    'line',
    'balance',
]
for graph_type in graph_types:
    if graph_type not in AC.list_libraries():
        AC.create_library(graph_type)

TTL = 15

@st.cache_data(ttl=TTL)
def artic_list_symbols(lib_name: str):
    return AC[lib_name].list_symbols()


@st.cache_data(ttl=100 * TTL)
def artic_list_libraries():
    return AC.list_libraries()


@st.cache_data(ttl=2 * TTL)
def artic_read_data(lib_name: str, symbol: str, *args, **kwargs):
    return AC[lib_name].read(symbol, *args, **kwargs).data


@st.cache_data(ttl=2 * TTL)
def artic_list_versions(lib_name: str, symbol: str):
    return AC[lib_name].list_versions(symbol)
