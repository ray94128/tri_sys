import streamlit as st
import pandas as pd
from db_utils import execute_query, execute_modify

def show_fact_maintenance():
    st.header("廠商資料維護")

    # 1. 查詢功能
    st.subheader("查詢廠商")
    search_term = st.text_input("輸入廠商代碼或名稱進行過濾")
    query = "SELECT * FROM fact"
    if search_term:
        query += f" WHERE fact_code LIKE '%{search_term}%' OR fact_name LIKE '%{search_term}%'"
    
    try:
        data = execute_query(query)
        if data:
            df = pd.DataFrame(data)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("查無資料")
    except Exception as e:
        st.error(f"查詢出錯: {e}")

    # 2. 新增功能
    st.subheader("新增廠商")
    with st.form("add_fact_form", clear_on_submit=True):
        new_code = st.text_input("廠商代碼")
        new_name = st.text_input("廠商名稱")
        new_remark = st.text_input("備註")
        submitted = st.form_submit_button("新增")
        if submitted:
            if not new_code or not new_name:
                st.warning("廠商代碼與名稱為必填")
            else:
                try:
                    execute_modify("INSERT INTO fact (fact_code, fact_name, remark) VALUES (:code, :name, :remark)", 
                                   {"code": new_code, "name": new_name, "remark": new_remark})
                    st.success("新增成功！")
                    st.rerun()
                except Exception as e:
                    st.error(f"新增失敗: {e}")

    # 3. 修改/刪除功能
    st.subheader("修改/刪除廠商")
    if data:
        target_code = st.selectbox("選擇要處理的廠商代碼", [d['fact_code'] for d in data])
        selected_fact = next((d for d in data if d['fact_code'] == target_code), None)
        
        if selected_fact:
            with st.form("edit_fact_form"):
                edit_name = st.text_input("廠商名稱", value=selected_fact['fact_name'])
                edit_remark = st.text_input("備註", value=selected_fact['remark'] or "")
                col1, col2 = st.columns(2)
                with col1:
                    if st.form_submit_button("更新"):
                        try:
                            execute_modify("UPDATE fact SET fact_name = :name, remark = :remark WHERE fact_code = :code", 
                                           {"name": edit_name, "remark": edit_remark, "code": target_code})
                            st.success("更新成功！")
                            st.rerun()
                        except Exception as e:
                            st.error(f"更新失敗: {e}")
                with col2:
                    if st.form_submit_button("刪除"):
                        try:
                            execute_modify("DELETE FROM fact WHERE fact_code = :code", {"code": target_code})
                            st.success("刪除成功！")
                            st.rerun()
                        except Exception as e:
                            st.error(f"刪除失敗: {e}")
