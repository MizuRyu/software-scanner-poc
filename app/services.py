import json
import asyncio

from logging import getLogger

from app.azure_client.azure_openai_client import AsyncAzureOpenAIClient
from app.excelsheet.excelmanager import ExcelHandler

logger = getLogger("software-scanner")

async_client = AsyncAzureOpenAIClient()

async def api_requests(system_prompt, document_type, base64_encoded, path, uploaded_file_name, config):

    if config["ocr_enhance"]: # gpt4o + ocr enhanced
        response = await async_client.async_enhanced_ocr_llm_response(path, base64_encoded, config["model_temp"]) 
    else:
        response = await async_client.async_llm_response(system_prompt, base64_encoded, config["model_temp"]) # gpt4o
        # response = await async_client.async_dummy_response(system_prompt, base64_encoded) # dummy
    
    json_data = json.loads(response)
    logger.info(f"document type: {document_type}")
    if config["excel_output"]:
        
        if document_type == "deliveryNote":
            delivery_notes_data = json_data.get("DeliveryNotes", [])
            product_details_list = json_data.get("ProductDetails", [])
            excel_handler = ExcelHandler()
            excel_handler.writer_delivery_notes_data(delivery_notes_data)
            excel_handler.writer_product_data(product_details_list)

    return response, uploaded_file_name, path