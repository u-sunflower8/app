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

# --- 登録フォーム ---
with st.form("add_todo"):
    title = st.text_input("タスク名")
    due = st.date_input("期限")
    # 追加：選択肢を作る
    priority = st.selectbox("優先度", ["高", "中", "低"])
    category = st.selectbox("カテゴリ", ["仕事", "プライベート", "買い物", "その他"])
    
    submit = st.form_submit_button("追加")
    
    if submit:
        # スプレッドシートへ書き込む行を5項目に増やす
        sheet.append_row([title, str(due), "未", priority, category])
        st.success("追加しました！")
        st.rerun()
# --- サイドバーで絞り込み機能 ---
st.sidebar.header("フィルター")
all_todos = sheet.get_all_records()

# カテゴリの選択肢を作る
categories = ["すべて"] + list(set([t["カテゴリ"] for t in all_todos]))
selected_cat = st.sidebar.selectbox("カテゴリで絞り込む", categories)

# 表示用データの抽出
if selected_cat == "すべて":
    filtered_todos = all_todos
else:
    filtered_todos = [t for t in all_todos if t["カテゴリ"] == selected_cat]

# 4. 表を表示（filtered_todos を表示するように変更）
st.subheader("現在のタスク")
st.table(filtered_todos)

# 2. 一覧表示
st.subheader("現在のタスク")
todos = sheet.get_all_records()
if todos:
    st.table(todos)
else:
    st.write("タスクはありません。")

# --- Discord通知用の関数 ---
def send_discord_notification(message):
    url = st.secrets["DISCORD_WEBHOOK_URL"]
    payload = {"content": message} # Discordは "content" というキーで送ります
    requests.post(url, json=payload)

# --- 登録時の処理 ---
if submit:
    sheet.append_row([title, str(due), "未", priority, category])
    
    # 呼び出しをDiscord用に変更
    send_discord_notification(f"📝 新しいタスク: {title} ({category})")
    
    st.success("追加しました！")
    st.rerun()
