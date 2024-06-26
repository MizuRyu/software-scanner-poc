import sys
import os
import asyncio
import streamlit as st
import tempfile

from logging import getLogger

# パスが通らないので明示的にsys.pathに追加
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from app.azure_client.azure_openai_client import AzureOpenAIClient, AsyncAzureOpenAIClient
from app.services import api_requests
from app.utils import encode_file, save_uploaded_file
from app.config.prompts_ja import SYSTEM_PROMPT_JA
from app.config.config import DOCUMENT_TYPE_MAPPING

logger = getLogger("software-scanner")

st.set_page_config(
    page_title="Software Scanner",
    page_icon="📤",
    layout="wide",
    initial_sidebar_state="expanded"
)

client = AzureOpenAIClient()
async_client = AsyncAzureOpenAIClient()

MAX_OCR_FILE_SIZE = 4 * 1024 * 1024 # DIのFreeプランは4MBが上限

# sidebar
with st.sidebar:
    with st.expander("Show System Prompt"):
        st.markdown(f"```\n{SYSTEM_PROMPT_JA}\n```")

    # user_input_text = st.text_area("prompt", value="")
    uploaded_files = st.file_uploader("ファイルをアップロード", type=["png", "jpg"], accept_multiple_files=True)
    model_temp = st.slider("Temperature", min_value=0.0, max_value=1.0, value=0.3, step=0.1)
    ocr_enhance = st.checkbox("OCR Enhance", value=False)
    excel_output = False
    write_db = st.checkbox("Write Data", value=False)
    run_button = st.button("実行")

    config = {
        "model_temp": model_temp,
        "ocr_enhance": ocr_enhance,
        "excel_output": excel_output,
        "write_db": write_db,
    }
    logger.info(f"config: {config}")

async def display_json_result(result):
    try:
        res, uploaded_file_name, path = result
    except ValueError as e:
        st.error(f"Error: {e}")
        return

    cols = st.columns(2)
    with cols[0]:
        st.image(path, caption=uploaded_file_name)
    with cols[1]:
        st.markdown(f"**{uploaded_file_name}**")
        st.json(res)

async def run_generate_json(document_type, encoded_file, file_path, uploaded_file_name, config):
    res = await api_requests(document_type, encoded_file, file_path, uploaded_file_name, config)
    await display_json_result(res)

async def run_analyze_document_type_process(base64_image, config):
    document_type = await async_client.async_analyze_document_type_llm_response(base64_image, config["model_temp"])
    return document_type

async def main_process(uploaded_files, config):
    encoded_files = []
    file_paths = []
    uploaded_file_names = []
    temp_dir = tempfile.mkdtemp()

    try:
        tasks = []
        for uploaded_file in uploaded_files:
            path = save_uploaded_file(uploaded_file, temp_dir)
            encoded_file = encode_file(path)
            encoded_files.append(encoded_file)
            file_paths.append(path)
            uploaded_file_names.append(uploaded_file.name)

            analyzed_document_type = await run_analyze_document_type_process(encoded_file, config)
            st.write(f"ファイル名: {uploaded_file.name} | 文書Format: {DOCUMENT_TYPE_MAPPING[analyzed_document_type]}")
            tasks.append(run_generate_json(analyzed_document_type, encoded_file, path, uploaded_file.name, config))
        
        await asyncio.gather(*tasks)
    finally:
        try: 
            for path in file_paths:
                os.remove(path)
            os.rmdir(temp_dir)
            logger.info("=============================")
        except FileNotFoundError as e:
            logger.error(f"Error deleting file: {e}")


# View
if run_button:
    logger.info("=============================")
    logger.info(f"uploaded_files: {uploaded_files}")
    if not uploaded_files:
        st.warning("File has not been uploaded")
        st.stop()
    
    if uploaded_files is not None:
        if ocr_enhance:
            for uploaded_file in uploaded_files:
                if uploaded_file.size > MAX_OCR_FILE_SIZE:
                    st.warning(f"OCR処理は4MB以下のファイルのみサポートしています。")
                    st.warning(f"File size is too large: {uploaded_file.name}")
                    st.stop()

    with st.spinner("実行中..."):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(main_process(uploaded_files, config))
        loop.close()