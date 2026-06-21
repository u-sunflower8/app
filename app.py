import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# 認証設定
creds_dict = st.secrets["GOOGLE_SHEETS"]
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)

# あなたのスプレッドシートID
SHEET_ID = "101hhNwt1VrR0fn3me63ifsduMqelnVIrY1ozr_Ul74w"
sheet = client.open_by_key(SHEET_ID).sheet1

st.title("ToDoリスト")

# 1. 新規追加フォーム
with st.form("add_todo"):
    title = st.text_input("タスク名")
    due = st.date_input("期限")
    submit = st.form_submit_button("追加")
    if submit:
        sheet.append_row([title, str(due), "未"])
        st.success("追加しました！")
        st.rerun() # 画面を更新して追加したデータを表示

# 2. 一覧表示
st.subheader("現在のタスク")
todos = sheet.get_all_records()
if todos:
    st.table(todos)
else:
    st.write("タスクはありません。")
