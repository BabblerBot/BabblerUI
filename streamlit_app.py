import streamlit as st
import replicate
import os
import requests
import asyncio
from dotenv import load_dotenv
from contextlib import suppress
from utils import search_book
from summarize import get_summary
from qa import prepare_qa

# App title
st.set_page_config(page_title="Babbler", page_icon="🤖")
QA_URL = os.getenv("QA_BACKEND") + "answer"


# App title
# App title
st.columns([1])
prompt = st.empty()


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

if "prevbook_name" not in st.session_state:
    st.session_state["prevbook_name"] = None


def clear_chat():
    prompt.empty()
    st.session_state["message"] = []
    st.session_state["summarized"] = False


if st.session_state.book_name_search:
    if st.session_state["prevbook_name"] != st.session_state.book_name_search:
        print("New book selected... clearning chat")
        clear_chat()
    book_name = st.session_state.book_name_search
    st.session_state["prevbook_name"] = book_name
    error, book = search_book(book_name)
    # print(st.session_state)
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
            st.button("Summarize", key="summarize", on_click=clear_chat)
        # with col2:
        #     st.button("Start Chatting", key="message")


if "summarize" not in st.session_state:
    st.session_state["summarize"] = False

if "summarized" not in st.session_state:
    st.session_state["summarized"] = False


def render_chat():
    for msg in st.session_state.message:
        st.chat_message(msg["role"]).write(msg["content"])

    prompt = st.chat_input()
    if prompt:
        st.session_state.message.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        response = requests.get(
            QA_URL, params={"query": prompt, "book_id": st.session_state.book["id"]}
        )
        # print(QA_URL)
        # print(response.json())
        # print(response.status_code)
        if response.status_code == 200:
            output = response.json()
            st.session_state.message.append({"role": "assistant", "content": output})
            st.chat_message("assistant").write(output)
        else:
            output = "Error: %s" % response.text
            st.session_state.message.append({"role": "assistant", "content": output})
            st.chat_message("assistant").write(output)


if st.session_state.summarized:
    print("summarized")
    render_chat()


async def parallel():
    clear_chat()
    if "book" not in st.session_state:
        print("Select Book")
        return
    book_id = st.session_state.book["id"]
    a = asyncio.gather(prepare_qa(book_id, book_name))
    b = asyncio.gather(get_summary(book_id))
    qa_ready, summary = await asyncio.gather(a, b)
    st.session_state["message"] = [
        {
            "role": "assistant",
            "content": summary[0],
        },
        {
            "role": "assistant",
            "content": f"Hello, I'm Babbler. I can talk about the book {st.session_state.book['title']}. Is there anything you want to know about?",
        },
    ]
    st.session_state["summarized"] = True
    # print(st.session_state)
    render_chat()


if st.session_state.summarize:
    asyncio.run(parallel())
