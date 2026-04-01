import streamlit as st
import pandas as pd
from db_utils import execute_query, execute_modify

def show_user_maintenance():
    st.header("用戶資料維護")

    # 1. 查詢功能
    st.subheader("查詢用戶")
    search_term = st.text_input("輸入用戶代碼或名稱進行過濾")
    query = "SELECT userid, username, pwd FROM [user]"
    if search_term:
        query += f" WHERE userid LIKE '%{search_term}%' OR username LIKE '%{search_term}%'"
    
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
    st.subheader("新增用戶")
    with st.form("add_user_form", clear_on_submit=True):
        new_id = st.text_input("用戶代碼")
        new_name = st.text_input("用戶名稱")
        new_pwd = st.text_input("用戶密碼", type="password")
        submitted = st.form_submit_button("新增")
        if submitted:
            if not new_id or not new_name or not new_pwd:
                st.warning("所有欄位均為必填")
            else:
                try:
                    execute_modify("INSERT INTO [user] (userid, username, pwd) VALUES (:uid, :name, :pwd)", 
                                   {"uid": new_id, "name": new_name, "pwd": new_pwd})
                    st.success("新增成功！")
                    st.rerun()
                except Exception as e:
                    st.error(f"新增失敗: {e}")

    # 3. 修改/刪除功能
    st.subheader("修改/刪除用戶")
    if data:
        target_id = st.selectbox("選擇要處理的用戶代碼", [d['userid'] for d in data])
        selected_user = next((d for d in data if d['userid'] == target_id), None)
        
        if selected_user:
            with st.form("edit_user_form"):
                edit_name = st.text_input("用戶名稱", value=selected_user['username'])
                edit_pwd = st.text_input("用戶密碼", value=selected_user['pwd'], type="password")
                col1, col2 = st.columns(2)
                with col1:
                    if st.form_submit_button("更新"):
                        try:
                            execute_modify("UPDATE [user] SET username = :name, pwd = :pwd WHERE userid = :uid", 
                                           {"name": edit_name, "pwd": edit_pwd, "uid": target_id})
                            st.success("更新成功！")
                            st.rerun()
                        except Exception as e:
                            st.error(f"更新失敗: {e}")
                with col2:
                    if st.form_submit_button("刪除"):
                        try:
                            execute_modify("DELETE FROM [user] WHERE userid = :uid", {"uid": target_id})
                            st.success("刪除成功！")
                            st.rerun()
                        except Exception as e:
                            st.error(f"刪除失敗: {e}")
