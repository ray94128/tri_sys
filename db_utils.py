import streamlit as st
import pandas as pd
from sqlalchemy import text

def get_connection():
    """透過 Streamlit 的 connection 機制建立連線"""
    return st.connection("my_mssql", type="sql")

def execute_query(query, params=None):
    """執行 SELECT 查詢並傳回結果 (List of Dicts)"""
    conn = get_connection()
    # 支援 SQL Server 的中括號
    df = conn.query(query, params=params, ttl=0)
    # 將 DataFrame 轉回原本模組期待的 dict 格式
    return df.to_dict('records')

def execute_modify(query, params=None):
    """執行 INSERT, UPDATE, DELETE"""
    conn = get_connection()
    with conn.session as session:
        result = session.execute(text(query), params)
        session.commit()
        return result.rowcount
