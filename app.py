import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials

st.title("デバッグ中...")

try:
    # 認証情報の読み込み
    creds_dict = st.secrets["GOOGLE_SHEETS"]
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)
    
    # 【最重要】IDで直接指定（ここをあなたのスプレッドシートIDに変えてください）
    TARGET_ID = "101hhNwt1VrR0fn3me63ifsduMqelnVIrY1ozr_Ul74w"
    
    sheet = client.open_by_key(TARGET_ID).sheet1
    
    st.success("接続成功！")
    st.write("ファイル名:", client.open_by_key(TARGET_ID).title)
    st.write("セルA1の値:", sheet.cell(1, 1).value)

except Exception as e:
    st.error(f"エラー発生: {e}")
    st.write("ヒント：もし 'Permission Denied' が出る場合、"
             "共有設定したメールアドレスが、JSONファイル内の 'client_email' と完全に一致しているか再確認してください。")
