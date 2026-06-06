import streamlit as st
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ.get("GROQ_API_KEY")
BOT_NAME = "Bob"
MODEL = "llama-3.1-8b-instant"
MODELS = {

    " LLaMA 3.3 70B  (Best — Default)":  "llama-3.3-70b-versatile",

    " LLaMA 3.1 8B   (Fastest)":          "llama-3.1-8b-instant",

    " Gemma 2 9B     (Google's Model)":   "gemma2-9b-it",

    " Mixtral 8x7B   (Long Context)":    "mixtral-8x7b-32768",

}
SYSTEM_PROMPT = '''
    You are Bob, a friendly AI coding buddy built for young learners!
    
    YOUR PERSONA:

    - Your name is Bob. You are enthusiastic, encouraging, and super fun!
    - You LOVE coding and think Python is the coolest thing ever!
    - You speak with energy and use emojis to keep things lively 
    - You are patient — you NEVER make students feel bad for not knowing something

    YOUR GOAL:

    - Help students learn Python, AI, and coding concepts
    - Make learning feel like playing a game, not studying!
    - Break hard topics into tiny, easy steps

    YOUR TONE:

    - Friendly and enthusiastic — like a cool older sibling who codes
    - Use simple words — no jargon unless you explain it!
    - Short answers — 2 to 4 sentences max unless asked for more
    - End responses with a question or emoji to keep the conversation going

    YOUR RULES:
    - Always start with a friendly greeting if this is the first message
    - NEVER say coding is hard — say it's "a fun puzzle to solve!"
    - If asked something off-topic, gently redirect: "Great question! But as your coding buddy, let's talk about..."
    - NEVER give harmful, rude, or inappropriate content

    STYLE:
    - Use emojis often (but not in every single word — keep it natural)
    - Use  for Python topics,  for AI topics,  for encouragement
    - Celebrate every small win: "You got it!  That's huge!"
'''

st.set_page_config(
    page_title = f"{BOT_NAME} AI ChatBot",
    layout = "centered"
)
with st.sidebar:
    st.title("Settings")
    st.markdown("---")

    model_label = st.selectbox("Choose AI Brain ", options = list(MODELS.keys()), index = 0, help = "Try different models and see how they respond!")
    selected_model = MODELS[model_label]
    st.markdown("---")
    
    temperature = st.slider("Creativity", min_value = 0.0, max_value = 1.5, value = 0.7, step = 0.1, help = "0.0 = Factual & precise  |  1.5 = Wild & creative!")

    if temperature <= 0.3:
        st.caption("very factual.")
    elif temperature <= 0.7:
        st.caption("balanced mode recomended.")
    elif temperature <= 1.0:
        st.caption("creative mode")
    else:
        st.caption("Wild and Unpredictable Mode.")
    st.markdown(f"Bot:{BOT_NAME}")
    st.markdown(f"Model:{MODEL}")
st.title(f"{BOT_NAME}")
st.info(
    f" Hi! I'm **{BOT_NAME}**, your AI coding buddy! "
    f"I now have a real personality — try asking me anything! \n\n"
    f" Try switching AI models in the sidebar and see how answers change!"
)
user_input = st.chat_input(f"message {BOT_NAME}")
if user_input:
    with st.chat_message("user"):
        st.markdown(user_input)
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                client = Groq(api_key = API_KEY)
                response = client.chat.completions.create(
                    model = selected_model,#dynamic model
                    temperature = temperature,#creativity control
                    max_tokens = 500,
                    messages = [
                        {
                            "role":"system", #System prompt!
                            "content": SYSTEM_PROMPT #Bob's personality
                        },
                        {
                            "role":"user",
                            "content": user_input #Student's message
                        }
                    ],
                )
                reply = response.choices[0].message.content
                st.markdown(reply)
                st.caption(f" Replied by: {model_label.split('(')[0].strip()} • Temp: {temperature}")
            except Exception as error:
                st.error(f"error:{error}")