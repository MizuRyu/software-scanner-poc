import os

def save_uploaded_file(uploaded_file, temp_dir):
    path = os.path.join(temp_dir, uploaded_file.name)
    with open(path, "wb") as f:
        f.write(uploaded_file.getvalue())
    return path