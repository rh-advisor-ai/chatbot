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
# st.info(f"user name: {st.session_state.get('user_name')}")
# st.info(f"user ID: {st.session_state.get('user_id')}")

# option = st.selectbox(
#     "How would you like to be contacted?",
#     ("Email", "Home phone", "Mobile phone"),
# )
# st.write("You selected:", option)

def start_thread_ai():
    if st.session_state.username and st.session_state.username != '':
        user_id = randint(1000, 10000)
        print(f"creating user ID: {str(user_id)}")
        st.session_state.user_name = st.session_state.username
        st.session_state.user_id = user_id
        # st.rerun()
        input_json = {
            "userId" : st.session_state.user_id
        }
        requests.post(f"{base_url}/start_thread", json=input_json).json()

def exit_chat():
    st.session_state.messages = []
    st.session_state.user_id = None
    del st.session_state['user_name']
    del st.session_state['user_id']
    # st.sidebar.empty()
    # st.sidebar.status(expanded=False)
    # del st.sidebar
    # st.rerun()

def run_chat():
    # Store and display the current prompt.
    st.session_state.messages.append({"role": "user", "content": st.session_state.prompt})
    # with st.chat_message("user"):
    #     st.markdown(st.session_state.prompt)
    input_json = {
        "userId" : st.session_state.user_id,
        "question" : st.session_state.prompt
    }
    data = requests.post(f"{base_url}/chat_advisor", json=input_json).json()

    # Stream the response to the chat using `st.write_stream`, then store it in 
    # session state.
    # with st.chat_message("assistant"):
    #     st.markdown(data['answer'])
    st.session_state.messages.append({"role": "assistant", "content": data['answer']})
    st.session_state.prompt = None


def phase_two():
    print()
    st.session_state.messages = []

if "user_name" not in st.session_state or not st.session_state.user_name:
    username = st.text_input("Username", type="default", key="username", on_change=start_thread_ai)
else:
    st.text("Hello " + st.session_state.user_name)

if "user_name" not in st.session_state or not st.session_state.user_name:
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

    # if st.sidebar.button("Next Steps", key='next_chat_button'):
    #     st.session_state.messages = []
    #     # move_focus()

    # st.sidebar.button("Exit", key='clear_chat_button', on_click=exit_chat)
        

    # Create a chat input field to allow the user to enter a message. This will display
    # automatically at the bottom of the page.
    # st.chat_input("What is up?", key="prompt", on_submit=run_chat)
    st.text_input("Chat", type="default", key="prompt", on_change=run_chat)
    
    col1, col2 = st.columns([1,1])  # Adjust column ratios as needed
    with col1:
        st.button("Exit", key='clear_chat_button', on_click=exit_chat)

    with col2:
        st.button("Next Step", key='next_chat_button', on_click=exit_chat)
