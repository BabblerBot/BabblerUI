import streamlit as st
import replicate
import os
import requests


# st.title('🎈 App Name')

# st.write('Hello world!')
# App title
st.set_page_config(page_title='Babbler', page_icon='🤖')

# Replicate Credentials
# with st.sidebar:
#     st.title('Babbler🤖')
#     if 'REPLICATE_API_TOKEN' in st.secrets:
#         st.success('API key already provided!', icon='✅')
#         replicate_api = st.secrets['REPLICATE_API_TOKEN']
#     else:
#         replicate_api = st.text_input('Enter Replicate API token:', type='password')
#         if not (replicate_api.startswith('r8_') and len(replicate_api)==40):
#             st.warning('Please enter your credentials!', icon='⚠️')
#         else:
#             st.success('Proceed to entering your prompt message!', icon='👉')
#     st.markdown('📖 Learn how to build this app in this [blog](#link-to-blog)!')
# os.environ['REPLICATE_API_TOKEN'] = replicate_api

# Store LLM generated responses
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]
st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

# Function for generating LLaMA2 response
# Refactored from <https://github.com/a16z-infra/llama2-chatbot>
def generate_llama2_response(prompt_input):
    string_dialogue = "You are a helpful assistant. You do not respond as 'User' or pretend to be 'User'. You only respond once as 'Assistant'."
    for dict_message in st.session_state.messages:
        if dict_message["role"] == "user":
            string_dialogue += "User: " + dict_message["content"] + "\\n\\n"
        else:
            string_dialogue += "Assistant: " + dict_message["content"]+ "\\n\\n"
    url = 'https://ishvalin-babbler.hf.space/generate'
    headers = {'accept': 'application/json'}
    data = {'query': string_dialogue + prompt_input}
    response = requests.post(url, headers=headers, data=data)

    return response.json()['output']

# User-provided prompt
if prompt := st.chat_input(disabled=not replicate_api):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

# Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = generate_llama2_response(prompt)
            placeholder = st.empty()
            full_response = ''
            for item in response:
                full_response += item
                placeholder.markdown(full_response)
            placeholder.markdown(full_response)
    message = {"role": "assistant", "content": full_response}
    st.session_state.messages.append(message)

    # st.write('Hello')