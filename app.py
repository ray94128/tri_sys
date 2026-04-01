import streamlit as st
from db_utils import execute_query
from modules.cust import show_cust_maintenance
from modules.fact import show_fact_maintenance
from modules.item import show_item_maintenance
from modules.user import show_user_maintenance

# 設置頁面配置
st.set_page_config(page_title="資料維護系統", layout="centered")

# 初始化 Session State
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "current_page" not in st.session_state:
    st.session_state.current_page = "Main"

# 登入畫面
def show_login():
    st.title("系統登入")
    userid = st.text_input("用戶代碼")
    pwd = st.text_input("密碼", type="password")
    if st.button("登入"):
        try:
            # 檢查用戶
            result = execute_query("SELECT * FROM [user] WHERE userid = ? AND pwd = ?", (userid, pwd))
            if result:
                st.session_state.logged_in = True
                st.session_state.username = result[0]['username']
                st.rerun()
            else:
                st.error("代碼或密碼錯誤")
        except Exception as e:
            st.error(f"登入失敗: {e}")

# 主選單 (4 個大按鈕)
def show_main_menu():
    st.title(f"歡迎, {st.session_state.username}")
    st.write("請選擇要執行的功能：")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("👥 客戶資料維護", use_container_width=True, key="btn_cust"):
            st.session_state.current_page = "CUST"
            st.rerun()
        if st.button("📦 商品資料維護", use_container_width=True, key="btn_item"):
            st.session_state.current_page = "ITEM"
            st.rerun()
            
    with col2:
        if st.button("🏭 廠商資料維護", use_container_width=True, key="btn_fact"):
            st.session_state.current_page = "FACT"
            st.rerun()
        if st.button("👤 用戶資料維護", use_container_width=True, key="btn_user"):
            st.session_state.current_page = "USER"
            st.rerun()

    st.divider()
    if st.button("登出", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.current_page = "Main"
        st.rerun()

# 頁面跳轉邏輯
if not st.session_state.logged_in:
    show_login()
else:
    if st.session_state.current_page == "Main":
        show_main_menu()
    else:
        if st.button("⬅️ 回主選單"):
            st.session_state.current_page = "Main"
            st.rerun()
        
        if st.session_state.current_page == "CUST":
            show_cust_maintenance()
        elif st.session_state.current_page == "FACT":
            show_fact_maintenance()
        elif st.session_state.current_page == "ITEM":
            show_item_maintenance()
        elif st.session_state.current_page == "USER":
            show_user_maintenance()
