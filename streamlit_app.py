import streamlit as st
import replicate
import os
import requests
from dotenv import load_dotenv
from utils import search_book
from summarize import get_summary
from qa import prepare_qa

# App title
st.set_page_config(page_title="Babbler", page_icon="🤖")
QA_URL = os.getenv("QA_BACKEND") + "answer"


# App title
# App title
st.columns([1])


# Sidebar for title
st.sidebar.title("Babbler 🤖")
st.sidebar.text_input("Search Book", key="book_name_search")

m = st.markdown(
    """
<style>
div.stButton > button:first-child {
    color: #ffffff;
    background-color: #373a3d;
}


</style>""",
    unsafe_allow_html=True,
)


if st.session_state.book_name_search:
    book_name = st.session_state.book_name_search
    error, book = search_book(book_name)
    # print(book)
    if error:
        st.sidebar.error(error)
    else:
        st.session_state.book = book
        st.sidebar.success("Book found: %s" % book["title"])
        st.title(book["title"])
        if len(book["authors"]) > 0:
            st.write(f"By {book['authors'][0]['name']}")
        if len(book["languages"]) > 0:
            language_code = book["languages"][0]
            st.write(f"Language: {language_code}")
        st.write(f"Subjects: {', '.join(book['subjects'])}")
        col1, col2 = st.columns(2)
        with col1:
            st.button("Summarize", key="summarize")
        # with col2:
        #     st.button("Start Chatting", key="message")

if "summarize" not in st.session_state:
    st.session_state["summarize"] = False

if "summerized" not in st.session_state:
    st.session_state["summarized"] = False


def render_chat():
    for msg in st.session_state.message:
        st.chat_message(msg["role"]).write(msg["content"])

    prompt = st.chat_input()
    if prompt:
        st.session_state.message.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        response = requests.get(QA_URL, params={"query": prompt})
        print(QA_URL)
        print(response.json())
        print(response.status_code)
        if response.status_code == 200:
            output = response.json()
            st.session_state.message.append({"role": "assistant", "content": output})
            st.chat_message("assistant").write(output)
        else:
            output = "Error: %s" % response.text
            st.session_state.message.append({"role": "assistant", "content": output})
            st.chat_message("assistant").write(output)


if st.session_state.summarize:
    book_id = st.session_state.book["id"]
    prepare_qa(book_id)
    summary = get_summary(book_id)
    if "message" not in st.session_state:
        st.session_state["message"] = [
            {
                "role": "assistant",
                "content": summary,
            },
            {
                "role": "assistant",
                "content": f"Hello, I'm Babbler. I can talk about the book {st.session_state.book['title']}. Is there anything you want to know about?",
            },
        ]
    render_chat()
