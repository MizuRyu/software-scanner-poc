import sys
import os

import streamlit as st
import tempfile


from app.azure_client.azure_openai_client import AzureOpenAIClient
from app.utils.encodeimage import encode_image
from app.utils.fileutils import save_uploaded_file

# パスが通らないので明示的にsys.pathに追加
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

st.set_page_config(
    page_title="Software Scanner",
    page_icon="📤",
    layout="centered",
    initial_sidebar_state="expanded"
)

client = AzureOpenAIClient()


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
    uploaded_file = st.file_uploader("Upload Files", type=["pdf", "pptx", "png", "jpg", "jpeg", "webp"])

    model_temp = st.slider("Temperature", min_value=0.0, max_value=1.0, value=0.3, step=0.1)
    st.button(
        "🗑 Reset Conversation",
        on_click=reset_conversation
    )
    run_button = st.button("Run")

if run_button:
    if uploaded_file is None:
        st.warning("File has not been uploaded")
        st.stop()
        
    st.write(user_input_text)
    with tempfile.TemporaryDirectory() as temp_dir:

        path = save_uploaded_file(uploaded_file, temp_dir)

        base64_image = encode_image(path)
        # res = client.llm_response(user_input_text, base64_image, model_temp)
        res = client.dummy_response(user_input_text, base64_image)
        st.markdown(f"```\n{res}\n```")
        st.divider()
        # st.write_stream(res)