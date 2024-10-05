import streamlit as st
import unidecode
import uuid
import re

DISABLE_LINK_CSS = """
<style>
a.toc {
    color: inherit;
    text-decoration: none; /* no underline */
}
</style>"""


class stoc:
    def __init__(self):
        self.toc_items = list()

    def h1(self, text: str, norm_text:str, write: bool = True):
        if write:
            st.write(f"# {text}")
        self.toc_items.append(("h1", text, norm_text))

    def h2(self, text: str, norm_text:str, write: bool = True):
        if write:
            st.write(f"## {text}")
        self.toc_items.append(("h2", text, norm_text))

    def h3(self, text: str, norm_text:str, write: bool = True):
        if write:
            st.write(f"### {text}")
        self.toc_items.append(("h3", text, norm_text))

    def h4(self, text: str, norm_text:str, write: bool = True):
        if write:
            st.write(f"#### {text}")
        self.toc_items.append(("h4", text, norm_text))
    def h5(self, text: str, norm_text:str, write: bool = True):
        if write:
            st.write(f"##### {text}")
        self.toc_items.append(("h5", text, norm_text))
    
    def toc(self):
        st.write(DISABLE_LINK_CSS, unsafe_allow_html=True)
        st.sidebar.caption("目录")
        markdown_toc = ""
        for title_size, title, norm_text in self.toc_items:
            h = int(title_size.replace("h", ""))
            markdown_toc += (
                " " * 2 * h
                + "- "
                + f'<a href="#{norm_text}" class="toc"> {title}</a> \n'
            )
        st.sidebar.write(markdown_toc, unsafe_allow_html=True)
    
    @classmethod
    @st.cache_data
    def from_markdown(cls, text: str):
        self = cls()
        new_text = ""
        for line in text.splitlines():
            if line.startswith("#####"):
                span_text, norm_text = self.add_span(line, 5)
                self.h5(line[5:], norm_text, write=False)
                new_text += span_text + "\n"
            elif line.startswith("####"):
                span_text, norm_text = self.add_span(line, 4)
                self.h4(line[4:], norm_text, write=False)
                new_text += span_text + "\n"
            elif line.startswith("###"):
                span_text, norm_text = self.add_span(line, 3)
                self.h3(line[3:], norm_text, write=False)
                new_text += span_text + "\n"
            elif line.startswith("##"):
                span_text, norm_text = self.add_span(line, 2)
                self.h2(line[2:], norm_text, write=False)
                new_text += span_text + "\n"
            elif line.startswith("#"):
                span_text, norm_text = self.add_span(line, 1)
                self.h1(line[1:], norm_text, write=False)
                new_text += span_text + "\n"
            else:
                new_text += line + "\n"
        # st.markdown(new_text, unsafe_allow_html=True)
        render_markdown_with_images(new_text)
        self.toc()
    def add_span(self, text, n):
        norm_text = normalize(text[n:])
        span_text = text[:n+1] + f'<span id="{norm_text}">{text[n:]}</span>'
        return span_text, norm_text
def render_markdown_with_images(markdown_text):
    # 匹配 Markdown 图片语法 ![alt text](image_url)
    pattern = re.compile(r'!\[.*?\]\((.*?)\)')

    # 记录上一个位置
    last_pos = 0

    # 查找所有匹配项
    for match in pattern.finditer(markdown_text):
        # 显示上一个位置到匹配位置之间的文本
        st.markdown(markdown_text[last_pos:match.start()], unsafe_allow_html=True)

        # 显示图片
        img_url = match.group(1)
        st.image(img_url)

        # 更新上一个位置
        last_pos = match.end()

    # 显示剩余的文本
    st.markdown(markdown_text[last_pos:], unsafe_allow_html=True)
def normalize(s):
    """
    Normalize titles as valid HTML ids for anchors
    >>> normalize("it's a test to spot how Things happ3n héhé")
    "it-s-a-test-to-spot-how-things-happ3n-h-h"
    """

    # Replace accents with "-"
    s_wo_accents = unidecode.unidecode(s)
    accents = [s for s in s if s not in s_wo_accents]
    for accent in accents:
        s = s.replace(accent, "-")

    # Lowercase
    s = s.lower()

    # Keep only alphanum and remove "-" suffix if existing
    normalized = (
        "".join([char if char.isalnum() else "-" for char in s]).strip("-").lower()
    )

    return normalized + str(uuid.uuid4())[:8]
