import streamlit as st
from openai import OpenAI
import numpy as np
from random import randint
import requests

base_url = st.secrets.BASE_URL

# Show title and description.
st.title("💬 Chatbot")
st.write(
    "This is a simple chatbot that uses OpenAI's"
)

# option = st.selectbox(
#     "How would you like to be contacted?",
#     ("Email", "Home phone", "Mobile phone"),
# )
# st.write("You selected:", option)

if "username" not in st.session_state:
    username = st.text_input("Username", type="default", key="username")
    user_id = randint(1000, 10000)
    st.session_state.username = username
    st.session_state.user_id = user_id
    st.experimental_rerun()
    input_json = {
        "userId" : st.session_state.user_id
    }
    requests.post(f"{base_url}/start_thread", json=input_json).json()
else:
    st.text("Hello " + st.session_state.username)

if not st.session_state.username:
    st.info("Please add your Username to continue.", icon="🗝️")
else:
    # Create a session state variable to store the chat messages. This ensures that the
    # messages persist across reruns.
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display the existing chat messages via `st.chat_message`.
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Create a chat input field to allow the user to enter a message. This will display
    # automatically at the bottom of the page.
    if prompt := st.chat_input("What is up?"):

        # Store and display the current prompt.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        input_json = {
            "userId" : st.session_state.user_id,
            "question" : prompt
        }
        data = requests.post(f"{base_url}/chat_advisor", json=input_json).json()

        # Stream the response to the chat using `st.write_stream`, then store it in 
        # session state.
        with st.chat_message("assistant"):
            st.markdown(data)
        st.session_state.messages.append({"role": "assistant", "content": data['answer']})
    
    st.button("Next Step")
