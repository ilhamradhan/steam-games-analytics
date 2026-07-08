"""DuckDB connection and cached query helpers."""
import os
from pathlib import Path

import duckdb
import pandas as pd
import streamlit as st


DB_PATH = Path(__file__).resolve().parent.parent / "steam_games.duckdb"


@st.cache_resource
def get_connection() -> duckdb.DuckDBPyConnection:
    return duckdb.connect(str(DB_PATH), read_only=True)


@st.cache_data(ttl=600)
def query(sql: str) -> pd.DataFrame:
    con = get_connection()
    return con.execute(sql).df()
