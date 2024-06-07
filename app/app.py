import sys
import os

import streamlit as st
import tempfile

# パスが通らないので明示的にsys.pathに追加
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from app.azure_client.azure_openai_client import AzureOpenAIClient
from app.utils.encodefile import encode_file
from app.utils.fileutils import save_uploaded_file

st.set_page_config(
    page_title="Software Scanner",
    page_icon="📤",
    layout="centered",
    initial_sidebar_state="expanded"
)

client = AzureOpenAIClient()


with st.sidebar:
    user_input_text = st.text_area("prompt", value="")
    uploaded_files = st.file_uploader("Upload Files", type=["pdf", "pptx", "png", "jpg", "jpeg", "webp"], accept_multiple_files=True)


    model_temp = st.slider("Temperature", min_value=0.0, max_value=1.0, value=0.3, step=0.1)
    run_button = st.button("Run")

if run_button:
    if uploaded_files is None:
        st.warning("File has not been uploaded")
        st.stop()

    if user_input_text:
        st.write(user_input_text)

    with tempfile.TemporaryDirectory() as temp_dir:

        for idx, uploaded_file in enumerate(uploaded_files):
            path = save_uploaded_file(uploaded_file, temp_dir)
            base64_encoded = encode_file(path)
            res = client.llm_response(user_input_text, base64_encoded, model_temp)
            # res = client.dummy_response(user_input_text, base64_encoded)

            img_col, json_data_col = st.columns(2)
            with img_col:
                st.image(path, caption=uploaded_file.name)

            with json_data_col:
                st.markdown(f"**{uploaded_file.name}**")
                st.markdown(f"```\n{res}\n```")
                st.divider()