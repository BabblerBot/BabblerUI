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

chat_history = st.empty() 

user_input = st.text_input("Enter a prompt",)

if st.button("Send"):
    if user_input:
        chat_history.append({"sender": "You", "message": user_input})
        response = requests.get(API_URL, params={"query": user_input})


    if response.status_code == 200:
        data = response.json()
        output = data["output"]
        chat_history.append({"sender": "Babbler", "message": output})
    else:
        st.markdown("Error: %s" % response.text)

for chat in chat_history:
    sender = "You" if chat["sender"] == "You" else "Babbler"
    st.text(f"{sender}: {chat['message']}")