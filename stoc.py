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
a.h1, a.h2, a.h3, a.h4, a.h5 {
    color: inherit;
    text-decoration: none; /* no underline */
}
a.h2, a.h2{
    font-size: 1.2em;
    font-weight: bold;
}
</style>"""


class stoc:
    def __init__(self, use_basic=False):
        self.toc_items = list()
        self.group_toc_items = list()
        self.threhold = 3
        self.use_basic = use_basic

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
    def toc_basic(self):
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
    def toc(self):
        st.write(DISABLE_LINK_CSS, unsafe_allow_html=True)
        st.sidebar.caption("目录")
        self.group_nodes()
        
        for group in self.group_toc_items:
            markdown_toc = ""
            min_num = int(1000000)
            for title_size, title, norm_text in group:
                h = int(title_size.replace("h", ""))
                min_num = min(min_num, h)
                markdown_toc += (
                    " " * 2 * h
                    + "- "
                    + f'<a href="#{norm_text}" class="toc, {title_size}"> {title}</a> \n'
                )
            if group[0][0] == f'h{self.threhold}':
                with st.sidebar.expander(group[0][1].strip()):
                    st.write(markdown_toc, unsafe_allow_html=True)
            else:
                st.sidebar.write(markdown_toc, unsafe_allow_html=True)
    def toc(self):
        st.write(DISABLE_LINK_CSS, unsafe_allow_html=True)
        st.sidebar.caption("目录")
        self.group_nodes()
        
        for group in self.group_toc_items:
            markdown_toc = ""
            min_num = int(1000000)
            for title_size, title, norm_text in group:
                h = int(title_size.replace("h", ""))
                min_num = min(min_num, h)
                markdown_toc += (
                    " " * 2 * h
                    + "- "
                    + f'<a href="#{norm_text}" class="toc, {title_size}"> {title}</a> \n'
                )
            if group[0][0] == f'h{self.threhold}':
                with st.sidebar.expander(group[0][1].strip()):
                    st.write(markdown_toc, unsafe_allow_html=True)
            else:
                st.sidebar.write(markdown_toc, unsafe_allow_html=True)
    
    def group_nodes(self):
        """用于添加expander"""
        current_group = []

        for node_triple in self.toc_items:
            title_size, title, norm_text = node_triple
            node = int(title_size.replace("h", ""))
            if node <= self.threhold:
                # 如果当前组不为空，说明之前已经有一个组了，需要先保存
                if current_group:
                    self.group_toc_items.append(current_group)
                # 小于等于2的节点单独作为新组
                current_group = [node_triple]
            else:
                # 大于2的节点直接加入当前组
                current_group.append(node_triple)

        # 最后检查是否有未保存的组
        if current_group:
            self.group_toc_items.append(current_group)
    
    @classmethod
    # @st.cache_data
    def from_markdown(cls, text: str, expand_contents: bool = False):
        """创建TOC树, 目前最多支持到h5"""
        self = cls(use_basic=expand_contents)
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
        if self.use_basic:
            self.toc_basic()
        else:
            self.toc()
    def add_span(self, text, n):
        norm_text = normalize(text[n:])
        span_text = text[:n+1] + f'<span id="{norm_text}">{text[n:]}</span>'
        return span_text, norm_text
def render_markdown_with_images(markdown_text):
    """使用st.image显示markdown中的图片"""
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
