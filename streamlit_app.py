import streamlit as st
import replicate
import os
import requests


# st.title('🎈 App Name')

# st.write('Hello world!')
# App title
st.set_page_config(page_title='Babbler', page_icon='🤖')

API_URL = "https://ishvalin-babbler.hf.space/generate"

# App title
st.title('Babbler 🤖') 
if "message" not in st.session_state:
    st.session_state["message"] = [{"role": "Babbler", "content": "Hello, I'm Babbler. I can talk about books. What book do you want to talk about?"}]


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
        st.session_state.message.append({"role": "Babbler", "content": output})
        st.chat_message("Babbler").write(output)
    else:
        output = "Error: %s" % response.text
        st.session_state.message.append({"role": "Babbler", "content": output})
        st.chat_message("Babbler").write(output)

# chat_history = st.empty() 

# user_input = st.text_input("Enter a prompt",)

# if st.button("Send"):
#     if user_input:
#         chat_history.append({"sender": "You", "message": user_input})
#         response = requests.get(API_URL, params={"query": user_input})


#     if response.status_code == 200:
#         data = response.json()
#         output = data["output"]
#         chat_history.append({"sender": "Babbler", "message": output})
#     else:
#         st.markdown("Error: %s" % response.text)

# for chat in chat_history:
#     sender = "You" if chat["sender"] == "You" else "Babbler"
#     st.text(f"{sender}: {chat['message']}")



# # First
# import openai import streamlit as st
# with st.sidebar:
#     openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
#     "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
#     "[View the source code](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"
#     "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"

# st.title("💬 Chatbot") if "messages" not in st.session_state:
#     st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

# for msg in st.session_state.messages:
#     st.chat_message(msg["role"]).write(msg["content"])

# if prompt := st.chat_input():
#     if not openai_api_key:
#         st.info("Please add your OpenAI API key to continue.")
#         st.stop()

#     openai.api_key = openai_api_key
#     st.session_state.messages.append({"role": "user", "content": prompt})
#     st.chat_message("user").write(prompt)
#     response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
#     msg = response.choices[0].message
#     st.session_state.messages.append(msg)
#     st.chat_message("assistant").write(msg.content)