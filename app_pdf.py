import streamlit as st
import base64

"""
https://blog.hsuzo.cn/post/tech/python/embedpdf/
"""
# 显示PDF文件的函数
def st_display_pdf(pdf_file):
    with open(pdf_file, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="1000" height="2000" type="application/pdf">'
    st.markdown(pdf_display, unsafe_allow_html=True)

def main():
    st.title("在Streamlit中嵌入PDF文件")
    st.subheader("Learn Streamlit")

    st_display_pdf("openai_api_instruct.pdf")

if __name__ == '__main__':
    main()

