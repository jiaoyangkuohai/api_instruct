from stoc import stoc

import streamlit as st
import re

def main():
    with open("version.txt", "r", encoding="utf-8") as file:
        version = file.read()
    # 读取 Markdown 文件
    with open("openai_api_instruct.md", "r", encoding="utf-8") as file:
        markdown_text = file.read()
    stoc.from_markdown(markdown_text)

    with open("openai_api_instruct.pdf", "rb") as pdf_file:
        PDFbyte = pdf_file.read()

    st.sidebar.download_button(label="下载离线PDF文档",
                        data=PDFbyte,
                        file_name=f"算法接口说明文档_{str(version)}.pdf",
                        mime='application/octet-stream')

if __name__ == "__main__": 
    main()
