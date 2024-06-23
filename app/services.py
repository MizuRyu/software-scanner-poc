import json
import asyncio

from logging import getLogger

from app.azure_client.azure_openai_client import AsyncAzureOpenAIClient
from app.excelsheet.excelmanager import ExcelHandler
from app.sqlite.sqliteDB import DatabaseHandler

logger = getLogger("software-scanner")

async_client = AsyncAzureOpenAIClient()

async def api_requests(document_type, base64_encoded, path, uploaded_file_name, config):
    db_handler = DatabaseHandler()

    if config["ocr_enhance"]: # gpt4o + ocr enhanced
        response = await async_client.async_enhanced_ocr_llm_response(document_type, path, base64_encoded, config["model_temp"]) 
    else:
        response = await async_client.async_llm_response(document_type, base64_encoded, config["model_temp"]) # gpt4o
        # response = await async_client.async_dummy_response() # dummy
    
    json_data = json.loads(response)
    logger.info(f"document type: {document_type}")

    if config["excel_output"]:
        if document_type == "deliveryNote":
            delivery_notes_data = json_data.get("DeliveryNotes", [])
            product_details_list = json_data.get("ProductDetails", [])
            excel_handler = ExcelHandler()
            excel_handler.writer_delivery_notes_data(delivery_notes_data)
            excel_handler.writer_product_data(product_details_list)

    if config["write_db"]:
        if document_type == "deliveryNote":
            logger.info("Inserting delivery note data into database")
            delivery_notes = json_data.get("DeliveryNotes", [])
            product_details = json_data.get("ProductDetails", [])
            db_handler.insert_delivery_note_data(delivery_notes, product_details)

        elif document_type == "bill":
            logger.info("Inserting bill data into database")
            bills = json_data.get("Bill", [])
            bill_details = json_data.get("BillDetails", [])
            db_handler.insert_bill_data(bills, bill_details)

        elif document_type == "quotation":
            logger.info("Inserting quotation data into database")
            quotations = json_data.get("Quotation", [])
            quotation_details = json_data.get("QuotationDetails", [])
            db_handler.insert_quotation_data(quotations, quotation_details)

        else:
            logger.warning(f"Document Type: {document_type} not supported.")
            pass

        db_handler.close()

    return response, uploaded_file_name, path