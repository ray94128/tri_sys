import streamlit as st
import pandas as pd
from db_utils import execute_query, execute_modify

def show_cust_maintenance():
    st.header("客戶資料維護")

    # 1. 查詢功能
    st.subheader("查詢客戶")
    search_term = st.text_input("輸入客戶代碼或名稱進行過濾")
    query = "SELECT * FROM cust"
    if search_term:
        query += f" WHERE cust_code LIKE '%{search_term}%' OR cust_name LIKE '%{search_term}%'"
    
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
    st.subheader("新增客戶")
    with st.form("add_cust_form", clear_on_submit=True):
        new_code = st.text_input("客戶代碼")
        new_name = st.text_input("客戶名稱")
        new_remark = st.text_input("備註")
        submitted = st.form_submit_button("新增")
        if submitted:
            if not new_code or not new_name:
                st.warning("客戶代碼與名稱為必填")
            else:
                try:
                    execute_modify("INSERT INTO cust (cust_code, cust_name, remark) VALUES (?, ?, ?)", 
                                   (new_code, new_name, new_remark))
                    st.success("新增成功！")
                    st.rerun()
                except Exception as e:
                    st.error(f"新增失敗: {e}")

    # 3. 修改/刪除功能
    st.subheader("修改/刪除客戶")
    if data:
        target_code = st.selectbox("選擇要處理的客戶代碼", [d['cust_code'] for d in data])
        selected_cust = next((d for d in data if d['cust_code'] == target_code), None)
        
        if selected_cust:
            with st.form("edit_cust_form"):
                edit_name = st.text_input("客戶名稱", value=selected_cust['cust_name'])
                edit_remark = st.text_input("備註", value=selected_cust['remark'] or "")
                col1, col2 = st.columns(2)
                with col1:
                    if st.form_submit_button("更新"):
                        try:
                            execute_modify("UPDATE cust SET cust_name = ?, remark = ? WHERE cust_code = ?", 
                                           (edit_name, edit_remark, target_code))
                            st.success("更新成功！")
                            st.rerun()
                        except Exception as e:
                            st.error(f"更新失敗: {e}")
                with col2:
                    if st.form_submit_button("刪除"):
                        try:
                            execute_modify("DELETE FROM cust WHERE cust_code = ?", (target_code,))
                            st.success("刪除成功！")
                            st.rerun()
                        except Exception as e:
                            st.error(f"刪除失敗: {e}")
