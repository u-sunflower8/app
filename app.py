import streamlit as st
import gspread
import requests
from oauth2client.service_account import ServiceAccountCredentials

# 認証設定
creds_dict = st.secrets["GOOGLE_SHEETS"]
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)
SHEET_ID = "101hhNwt1VrR0fn3me63ifsduMqelnVIrY1ozr_Ul74w"
sheet = client.open_by_key(SHEET_ID).sheet1

def send_discord_notification(message):
    url = st.secrets["DISCORD_WEBHOOK_URL"]
    # データを少し詳細にしてみます
    payload = {"content": f"【通知】 {message}"}
    response = requests.post(url, json=payload)
    # 応答コードを確認して、もし失敗ならエラーを出すようにする
    if response.status_code != 200 and response.status_code != 204:
        st.error(f"Discordからエラーが返ってきました: {response.status_code}")

st.title("ToDoリスト")

# 登録フォーム
with st.form("add_todo"):
    title = st.text_input("タスク名")
    due = st.date_input("期限")
    priority = st.selectbox("優先度", ["高", "中", "低"])
    category = st.selectbox("カテゴリ", ["仕事", "プライベート", "買い物", "その他"])
    submit = st.form_submit_button("追加")

if submit:
        # 1. シート書き込み
        sheet.append_row([title, str(due), "未", priority, category])
        
        # 2. Discord通知を詳細に表示する
        st.write("Discordへ送信を試みています...")
        
        try:
            url = st.secrets["DISCORD_WEBHOOK_URL"]
            payload = {"content": f"📝 新タスク: {title}"}
            
            # 応答を確認する
            response = requests.post(url, json=payload)
            
            # 結果を表示
            st.write(f"Discordからの応答コード: {response.status_code}")
            
            if response.status_code == 204:
                st.success("通知がDiscordに送信されました！")
            else:
                st.error(f"Discordへの送信で失敗しました。コード: {response.status_code}")
                st.write(f"詳細: {response.text}")
                
        except Exception as e:
            st.error(f"プログラムの例外エラー: {e}")
            
        st.rerun()

# サイドバー絞り込み
st.sidebar.header("フィルター")
all_todos = sheet.get_all_records()
if all_todos:
    categories = ["すべて"] + list(set([t["カテゴリ"] for t in all_todos]))
    selected_cat = st.sidebar.selectbox("カテゴリで絞り込む", categories)
    
    if selected_cat == "すべて":
        filtered_todos = all_todos
    else:
        filtered_todos = [t for t in all_todos if t["カテゴリ"] == selected_cat]
    st.table(filtered_todos)
else:
    st.write("タスクはありません。")
