import streamlit as st
import replicate
import os
import requests


# App title
st.set_page_config(page_title='Babbler', page_icon='🤖')

API_URL = "https://ishvalin-babbler.hf.space/generate"



# App title
# App title
st.columns([1])
st.title('Babbler 🤖')


# Sidebar for title
st.sidebar.title('Babbler 🤖')






# App title
# st.title('Babbler 🤖') 
if "message" not in st.session_state:
    st.session_state["message"] = [{"role": "assistant", "content": "Hello, I'm Babbler. I can talk about books. What book do you want to talk about?"}]


# for msg in st.session_state.message:
#     st.chat_message(msg["role"]).write(msg["content"])


# Create a layout with columns
col1, col2 = st.columns([1, 5])

# Display chat history in the main column
with col2:
    for msg in st.session_state.message:
        st.chat_message(msg["role"]).write(msg["content"])

prompt = st.chat_input()
if prompt:
    st.session_state.message.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response = requests.get(API_URL, params={"query": prompt})
    if response.status_code == 200:
        data = response.json()
        output = data["output"]
        st.session_state.message.append({"role": "assistant", "content": output})
        st.chat_message("assistant").write(output)
    else:
        output = "Error: %s" % response.text
        st.session_state.message.append({"role": "assistant", "content": output})
        st.chat_message("assistant").write(output)
