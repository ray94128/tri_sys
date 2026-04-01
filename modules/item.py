import streamlit as st
import pandas as pd
from db_utils import execute_query, execute_modify

def show_item_maintenance():
    st.header("商品資料維護")

    # 獲取廠商列表供下拉選單使用
    try:
        facts = execute_query("SELECT fact_code, fact_name FROM fact")
        fact_options = {f"{f['fact_code']} - {f['fact_name']}": f['fact_code'] for f in facts}
    except Exception as e:
        st.error(f"獲取廠商列表出錯: {e}")
        fact_options = {}

    # 1. 查詢功能
    st.subheader("查詢商品")
    search_term = st.text_input("輸入商品代碼或名稱進行過濾")
    query = "SELECT * FROM item"
    if search_term:
        query += f" WHERE item_code LIKE '%{search_term}%' OR item_name LIKE '%{search_term}%'"
    
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
    st.subheader("新增商品")
    with st.form("add_item_form", clear_on_submit=True):
        new_code = st.text_input("商品代碼")
        new_name = st.text_input("商品名稱")
        new_fact_display = st.selectbox("主供應商", options=list(fact_options.keys()))
        new_fact_code = fact_options.get(new_fact_display)
        
        submitted = st.form_submit_button("新增")
        if submitted:
            if not new_code or not new_name:
                st.warning("商品代碼與名稱為必填")
            else:
                try:
                    execute_modify("INSERT INTO item (item_code, item_name, fact_code) VALUES (:code, :name, :fcode)", 
                                   {"code": new_code, "name": new_name, "fcode": new_fact_code})
                    st.success("新增成功！")
                    st.rerun()
                except Exception as e:
                    st.error(f"新增失敗: {e}")

    # 3. 修改/刪除功能
    st.subheader("修改/刪除商品")
    if data:
        target_code = st.selectbox("選擇要處理的商品代碼", [d['item_code'] for d in data])
        selected_item = next((d for d in data if d['item_code'] == target_code), None)
        
        if selected_item:
            with st.form("edit_item_form"):
                edit_name = st.text_input("商品名稱", value=selected_item['item_name'])
                # 預設選中目前的廠商
                current_fact_display = next((k for k, v in fact_options.items() if v == selected_item['fact_code']), None)
                edit_fact_display = st.selectbox("主供應商", options=list(fact_options.keys()), 
                                                 index=list(fact_options.keys()).index(current_fact_display) if current_fact_display else 0)
                edit_fact_code = fact_options.get(edit_fact_display)
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.form_submit_button("更新"):
                        try:
                            execute_modify("UPDATE item SET item_name = :name, fact_code = :fcode WHERE item_code = :code", 
                                           {"name": edit_name, "fcode": edit_fact_code, "code": target_code})
                            st.success("更新成功！")
                            st.rerun()
                        except Exception as e:
                            st.error(f"更新失敗: {e}")
                with col2:
                    if st.form_submit_button("刪除"):
                        try:
                            execute_modify("DELETE FROM item WHERE item_code = :code", {"code": target_code})
                            st.success("刪除成功！")
                            st.rerun()
                        except Exception as e:
                            st.error(f"刪除失敗: {e}")
