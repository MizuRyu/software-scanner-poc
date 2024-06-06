import base64
import os
from openai import AzureOpenAI
import pandas as pd
import streamlit as st
from PIL import Image
import tempfile
import re

from dotenv import load_dotenv

load_dotenv()


client = AzureOpenAI(
    api_version=os.getenv("API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
)

st.set_page_config(
    page_title="Software Scanner",
    page_icon="📤",
    layout="centered",
    initial_sidebar_state="expanded"
)


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

# st.title('Software Scanner')
# st.write('This is a simple Streamlit app.')
# st.caption("注釈")
# st.warning("warning")
# st.error("error")
# st.info("info")
# st.success("success")


def reset_conversation():
    if "messages" in st.session_state and len(st.session_state.messages) > 0:
        st.session_state.pop("messages", None)

with st.sidebar:
    user_input_text = st.text_area("prompt", value="")
    uploaded_file = st.file_uploader("Upload Files", type=["png", "jpg", "jpeg", "webp"])

    model_temp = st.slider("Temperature", min_value=0.0, max_value=1.0, value=0.3, step=0.1)
    st.button(
        "🗑 Reset Conversation",
        on_click=reset_conversation
    )


def stream_llm_response(user_input_text, base64_image, model_temp=0.3):
    response_message = ""
    system_prompt = "あなたは画像を読み取るエキスパートです。アップロードされた画像について詳細に説明します。"

    for chunk in client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": [
                    {"type": "text", "text": user_input_text},
                    {"type": "image_url", "image_url": {
                        "url": f"data:image/png;base64, {base64_image}"
                    }}
                ]}
            ],
            max_tokens=150,
            temperature=model_temp,
            stream=True
        ):
        choice = chunk.choices[0] if hasattr(chunk, 'choices') and chunk.choices else ""
        if hasattr(choice, 'delta') and hasattr(choice.delta, 'content'):
            content = chunk.choices[0].delta.content
            response_message += content if content else ""
            yield content



def save_uploaded_file(uploaded_file, temp_dir):
        st.write(temp_dir) # filename
        path = os.path.join(temp_dir, uploaded_file.name)
        with open(path, "wb") as f:
            f.write(uploaded_file.getvalue())
        return path

if uploaded_file is not None:

    st.write(user_input_text)
    with tempfile.TemporaryDirectory() as temp_dir:

        path = save_uploaded_file(uploaded_file, temp_dir)

        base64_image = encode_image(path)
        
        st.write_stream(stream_llm_response(user_input_text, base64_image, model_temp))
