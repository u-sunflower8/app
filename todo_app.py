import streamlit as st
import gspread
import json

# SecretsからGoogleの認証情報を読み込む
def get_sheet():
    # Secretsから設定を取得
    creds_dict = st.secrets["GOOGLE_SHEETS"]
    
    # 辞書型として認証に渡す
    creds = ServiceAccountCredentials.from_json_keyfile_dict(
        creds_dict, 
        ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    )
    client = gspread.authorize(creds)
    return client.open("Todoリスト").sheet1

sheet = init_sheet()

st.title("Web Todoリスト")

# 1. 入力フォーム
with st.form("todo_form"):
    title = st.text_input("タイトル")
    content = st.text_input("内容")
    due_date = st.date_input("期日")
    submit = st.form_submit_button("登録")
    if submit:
        sheet.append_row([title, content, str(due_date), "未完了"])
        st.success("保存しました！")

# 2. 一覧表示
st.subheader("タスク一覧")
data = sheet.get_all_records()
df = pd.DataFrame(data)
st.dataframe(df)
