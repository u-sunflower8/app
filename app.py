import streamlit as st
import gspread

# 設定をSecretsから読み込む部分はそのままとして...
st.title("接続テスト")

try:
    # 接続試行
    # (ここに必要な認証コードを記述)
    sheet = client.open("Todoリスト").sheet1
    st.write("成功！シートに接続できました。")
    st.write("セルA1の内容:", sheet.cell(1, 1).value) # 1行1列目の値を表示
except Exception as e:
    st.error(f"接続失敗: {e}")
