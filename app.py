import streamlit as st

st.set_page_config(page_title='LLM Request API')

# 读取 Markdown 文件
with open("openai_api_instruct.md", "r", encoding="utf-8") as file:
    markdown_text = file.read()

# 在 Streamlit 应用中显示 Markdown 内容
st.markdown(markdown_text)
