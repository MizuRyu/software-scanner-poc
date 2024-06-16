import base64
import os

def encode_file(file_path: str) -> str:
    with open(file_path, "rb") as file:
        encoded_string = base64.b64encode(file.read()).decode("utf-8")
    return encoded_string

def save_uploaded_file(uploaded_file: str, temp_dir: str) -> str:
    path = os.path.join(temp_dir, uploaded_file.name)
    with open(path, "wb") as f:
        f.write(uploaded_file.getvalue())
    return path
