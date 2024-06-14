import os
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential

from PIL import Image
from io import BytesIO

import streamlit as st

from logging import getLogger
from dotenv import load_dotenv

load_dotenv()

class OCRClient:
    def __init__(self):
        self.logger = getLogger("software-scanner")
        self.azure_di_endpoint = os.getenv("DI_ENDPOINT")
        self.azure_di_key = os.getenv("DI_KEY")

        if not self.azure_di_endpoint or not self.azure_di_key:
            raise ValueError("Azure DI endpoint and key are required.")
        
        self.client = DocumentIntelligenceClient(endpoint=self.azure_di_endpoint, credential=AzureKeyCredential(self.azure_di_key))
    
    def resize_image(self, image_bytes, max_size=(1024, 1024)):
        self.logger.info(f"resize_image() {type(image_bytes)}")

        image = Image.open(BytesIO(image_bytes))
        image.thumbnail(max_size, Image.LANCZOS)
        
        output = BytesIO()
        image.save(output, format="PNG")
        return output.getvalue()
    
    def check_and_resize_image(self, image_bytes, max_size=(1024, 1024)):
        self.logger.info(f"check_and_resize_image() {type(image_bytes)}")
        self.logger.info(f"image_bytes: {image_bytes[:10]}...")
        file_size = len(image_bytes)
        self.logger.info(f"File size: {file_size} bytes")
        if file_size > 4 * 1024 * 1024:
            self.logger.info("Resizing image...")
            image_bytes = self.resize_image(image_bytes, max_size)
            self.logger.info(f"Resized image size: {len(image_bytes)} bytes")
        return image_bytes

    def run_ocr(self, image_path, model='prebuilt-read'):
        try:
            with open(image_path, "rb") as image_file:
                image_bytes = image_file.read()

            self.logger.info(f"run_ocr() {type(image_bytes)}")
            image_bytes = self.check_and_resize_image(image_bytes)
            poller = self.client.begin_analyze_document(model, analyze_request=image_bytes, content_type='application/octet-stream')
            result = poller.result()

            with st.sidebar:
                st.write("OCR Result:")
                st.write(result.content)
            return result.content
        except Exception as e:
            self.logger.error("Failed to run OCR")
            raise

