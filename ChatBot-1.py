import streamlit as st
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ.get("GROQ_API_KEY")
BOT_NAME = "Bob"
MODEL = "llama-3.1-8b-instant"

st.set_page_config(
    page_title = f"{BOT_NAME} AI ChatBot",
    layout = "centered"
)
with st.sidebar:
    st.title("Settings")
    st.markdown(f"Bot:{BOT_NAME}")
    st.markdown(f"Model:{MODEL}")
st.title(f"{BOT_NAME}")
st.info(f"Hi! I am {BOT_NAME}, your AI buddy. Ask me anything!")
user_input = st.chat_input(f"message {BOT_NAME}")
if user_input:
    with st.chat_message("user"):
        st.markdown(user_input)
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                client = Groq(api_key = API_KEY)
                response = client.chat.completions.create(
                    model = MODEL,
                    messages = [{"role": "user", "content": user_input}],
                    max_tokens = 400,

                )
                reply = response.choices[0].message.content
                st.markdown(reply)
            except Exception as error:
                st.error(f"error:{error}")