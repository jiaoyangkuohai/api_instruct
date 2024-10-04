from stoc import stoc

import streamlit as st
import re

def main():
    # 读取 Markdown 文件
    with open("openai_api_instruct.md", "r", encoding="utf-8") as file:
        markdown_text = file.read()
    stoc.from_markdown(markdown_text)

if __name__ == "__main__": 
    # md = """
    # # Demo
    # sdfed

    # ## I want to talk about this
    # sdef

    # ### Smaller again
    # ijfds

    # ## Another subtitle
    # 水电费

    # ### I also should address that
    # 暖气费

    # ## Conclusion
    # 总计
    # """

    # # stoc.from_markdown(md)
    # stoc.from_markdown(md)
    main()
