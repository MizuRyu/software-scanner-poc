import json
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
from app.excelsheet.excelmanager import ExcelHandler
from app.utils.encodefile import encode_file
from app.utils.fileutils import save_uploaded_file
from app.config.prompts import SYSTEM_PROMPT_JA

logger = getLogger("software-scanner")

st.set_page_config(
    page_title="Software Scanner",
    page_icon="📤",
    layout="wide",
    initial_sidebar_state="expanded"
)

client = AzureOpenAIClient()
async_client = AsyncAzureOpenAIClient()

user_input_text = ""

# sidebar
with st.sidebar:
    with st.expander("Show System Prompt"):
        st.markdown(f"```\n{SYSTEM_PROMPT_JA}\n```")

    # user_input_text = st.text_area("prompt", value="")
    uploaded_files = st.file_uploader("ファイルをアップロード", type=["pdf", "png", "jpg", "jpeg"], accept_multiple_files=True)
    model_temp = st.slider("Temperature", min_value=0.0, max_value=1.0, value=0.3, step=0.1)
    ocr_enhance = st.checkbox("OCR Enhance", value=False)
    excel_output = st.checkbox("Excel出力(納品書のみ対応)", value=False)
    run_button = st.button("実行")

    config = {
        "model_temp": model_temp,
        "ocr_enhance": ocr_enhance,
        "excel_output": excel_output
    }
    logger.info(f"config: {config}")

async def api_requests(uploaded_file, temp_dir, user_input_text, config):
    path = save_uploaded_file(uploaded_file, temp_dir)
    base64_encoded = encode_file(path)

    if config["ocr_enhance"]: # gpt4o + ocr enhanced
        
        response = await async_client.async_enhanced_ocr_llm_response(path, base64_encoded, config["model_temp"]) 
    else:
        response = await async_client.async_llm_response(user_input_text, base64_encoded, config["model_temp"]) # gpt4o
        # response = await async_client.async_dummy_response(user_input_text, base64_encoded) # dummy
    
    logger.info(f"API response: {response}")
    json_data = json.loads(response)
    delivery_notes_data = json_data.get("DeliveryNotes", [])
    product_details_list = json_data.get("ProductDetails", [])
    logger.info(f"json_data: {json_data}")

    if config["excel_output"]:
        excel_handler = ExcelHandler()
        excel_handler.writer_delivery_notes_data(delivery_notes_data)
        excel_handler.writer_product_data(product_details_list)

    return response, uploaded_file, path

async def process_files(uploaded_files, user_input_text, config):
    with tempfile.TemporaryDirectory() as temp_dir:
        tasks = [api_requests(file, temp_dir, user_input_text, config) for file in uploaded_files]
        results = await asyncio.gather(*tasks)
        display_results(results)

def display_results(results):
    col_idx = 0
    cols = st.columns(4)

    for res, uploaded_file, path in results:
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

def run_asyncio_task(uploaded_files, user_input_text, config):
    asyncio.run(process_files(uploaded_files, user_input_text, config))



# View
if run_button:
    logger.info("=============================")
    logger.info(f"uploaded_files: {uploaded_files}")
    if not uploaded_files:
        st.warning("File has not been uploaded")
        st.stop()

    with st.spinner("実行中..."):
        run_asyncio_task(uploaded_files, user_input_text, config)

        