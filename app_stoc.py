from stoc import stoc

import streamlit as st
import re

@st.cache_data
def read_data():
    with open("version.txt", "r", encoding="utf-8") as file:
        version = file.read()
    # 读取 Markdown 文件
    with open("openai_api_instruct.md", "r", encoding="utf-8") as file:
        markdown_text = file.read()
    
    with open("openai_api_instruct.pdf", "rb") as pdf_file:
        PDFbyte = pdf_file.read()
    return version, markdown_text, PDFbyte
def main():
    version, markdown_text, PDFbyte = read_data()
    stoc.from_markdown(markdown_text)

    st.sidebar.download_button(label="下载离线PDF文档",
                        data=PDFbyte,
                        file_name=f"算法接口说明文档_{str(version)}.pdf",
                        mime='application/octet-stream')
    st.sidebar.divider()
    with st.sidebar.expander("管理员操作"):
        if st.button("重新加载所有数据", help='点击后刷新页面'):
            # Clear values from *all* all in-memory and on-disk data caches:
            # i.e. clear values from both square and cube
            st.cache_data.clear()

if __name__ == "__main__": 
    main()
