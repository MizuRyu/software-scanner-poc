import sys
import os
import asyncio
import tempfile
import streamlit as st

from logging import getLogger


# パスが通らないので明示的にsys.pathに追加
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from app.azure_client.azure_openai_client import AzureOpenAIClient, AsyncAzureOpenAIClient
from app.utils.encodefile import encode_file
from app.utils.fileutils import save_uploaded_file
from app.config.prompts import SYSTEM_PROMPT

logger = getLogger("software-scanner")

st.set_page_config(
    page_title="Software Scanner",
    page_icon="📤",
    layout="wide",
    initial_sidebar_state="expanded"
)

client = AzureOpenAIClient()
async_client = AsyncAzureOpenAIClient()


# sidebar
with st.sidebar:
    with st.expander("Show System Prompt"):
        st.write(SYSTEM_PROMPT)
    user_input_text = st.text_area("prompt", value="")
    uploaded_files = st.file_uploader("Upload Files", type=["pdf", "pptx", "png", "jpg", "jpeg", "webp"], accept_multiple_files=True)
    model_temp = st.slider("Temperature", min_value=0.0, max_value=1.0, value=0.3, step=0.1)
    run_button = st.button("Run")

async def process_files(uploaded_files, user_input_text, model_temp):
    with tempfile.TemporaryDirectory() as temp_dir:
        tasks = create_api_request_tasks(uploaded_files, temp_dir, user_input_text, model_temp)
        results = await asyncio.gather(*[task[0] for task in tasks])
        display_results(results, tasks)
    
def create_api_request_tasks(uploaded_files, temp_dir, user_input_text, model_temp):
    tasks = []
    for uploaded_file in uploaded_files:
        path = save_uploaded_file(uploaded_file, temp_dir)
        base64_encoded = encode_file(path)
        # task = async_client.async_llm_response(user_input_text, base64_encoded, model_temp)
        task = async_client.async_dummy_response(user_input_text, base64_encoded)
        tasks.append((task, uploaded_file, path))
    return tasks

def display_results(results, tasks):
    col_idx = 0
    cols = st.columns(4)

    for res, (task, uploaded_file, path) in zip(results, tasks):
        with cols[col_idx]:
            st.image(path, caption=uploaded_file.name)
        with cols[col_idx + 1]:
            st.markdown(f"**{uploaded_file.name}**")
            st.markdown(f"```\n{res}\n```")
            st.divider()
        
        col_idx += 2
        if col_idx >= 4:
            col_idx = 0
            cols = st.columns(4)

if run_button:
    logger.info(f"uploaded_files: {uploaded_files}")
    if not uploaded_files:
        st.warning("File has not been uploaded")
        st.stop()

    if user_input_text:
        st.write(user_input_text)
    
    with st.spinner("実行中..."):
        asyncio.run(process_files(uploaded_files, user_input_text, model_temp))