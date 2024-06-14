import os
from openai import AzureOpenAI, AsyncAzureOpenAI
from dotenv import load_dotenv

from app.config.prompts import SYSTEM_PROMPT_EN, AFTER_OCR_SYSTEM_PROMPT_EN, ENY_SYSTEM_PROMPT, ENY_AFTER_OCR_SYSTEM_PROMPT
from app.azure_client.azure_ocr_client import OCRClient
from logging import getLogger

load_dotenv()

class AzureOpenAIClient:
    def __init__(self):
        self.logger = getLogger("software-scanner")
        self.client = AzureOpenAI(
            api_version=os.getenv("API_VERSION"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        )

        self.system_prompt = SYSTEM_PROMPT_EN
        self.max_tokens = 800

    def dummy_response(self, user_input, base64_encoded):
        return """
{
    "DeliveryNotes": [
        {
            "DeliveryId": "INV12345",
            "Recipient": "Taro Yamada",
            "Address": "Tokyo, Japan",
            "TEL": "012-3456-7890",
            "FAX": "012-3456-7891",
            "DeliveryDate": "2022-01-01",
            "Publisher": "ABC Corporation",
            "Subtotal": "10000",
            "Tax": "1000",
            "Total": "11000",
            "Remarks": "Remarks"
        }
    ],
    "ProductDetails": [
        {
            "DeliveryId": "INV12345",
            "ProductName": "Product A",
            "Quantity": "2",
            "Unit": "pcs",
            "UnitPrice": "5000",
            "TotalPrice": "10000",
            "Origin": "Japan",
            "Remarks": "Remarks"
        },
        {
            "DeliveryId": "INV12345",
            "ProductName": "Product B",
            "Quantity": "3",
            "Unit": "pcs",
            "UnitPrice": "1000",
            "TotalPrice": "3000",
            "Origin": "Japan",
            "Remarks": "Remarks"
        }
    ]
}
        """

    def llm_response(self, user_input, base64_image, model_temp=0.3):
        response = self.client.chat.completions.create(
        model="gpt-4o",
        response_format={ "type": "json_object" },
        messages=[
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": [
                {"type": "text", "text": user_input},
                {"type": "image_url", "image_url": {
                    "url": f"data:image/png;base64, {base64_image}",
                    "detail": "high" # https://platform.openai.com/docs/guides/vision
                }}
            ]}
        ],
        max_tokens=self.max_tokens,
        temperature=model_temp,
    )
        self.logger.info(f"response: {response.choices[0].message.content}")
        return response.choices[0].message.content

    def stream_llm_response(self, user_input, base64_image, model_temp=0.3):
        response_message = ""

        for chunk in self.client.chat.completions.create(
        model="gpt-4o",
        response_format={ "type": "json_object" },
        messages=[
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": [
                {"type": "text", "text": user_input},
                {"type": "image_url", "image_url": {
                    "url": f"data:image/png;base64, {base64_image}"
                }}
            ]}
        ],
        max_tokens=self.max_tokens,
        temperature=model_temp,
        stream=True
        ):
            choice = chunk.choices[0] if hasattr(chunk, 'choices') and chunk.choices else ""
            if hasattr(choice, 'delta') and hasattr(choice.delta, 'content'):
                content = chunk.choices[0].delta.content
                response_message += content if content else ""
                yield content

class AsyncAzureOpenAIClient:
    def __init__(self):
        self.logger = getLogger("software-scanner")
        self.client = AsyncAzureOpenAI(
            api_version=os.getenv("API_VERSION"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        )

        self.system_prompt = SYSTEM_PROMPT_EN
        self.max_tokens = 2048
        self.ocr_client = OCRClient()

    async def async_dummy_response(self, user_input, base64_encoded):
        return """
{
    "DeliveryNotes": [
        {
            "DeliveryId": "INV12345",
            "Recipient": "Taro Yamada",
            "Address": "Tokyo, Japan",
            "TEL": "012-3456-7890",
            "FAX": "012-3456-7891",
            "DeliveryDate": "2022-01-01",
            "Publisher": "ABC Corporation",
            "Subtotal": "10000",
            "Tax": "1000",
            "Total": "11000",
            "Remarks": "Remarks"
        }
    ],
    "ProductDetails": [
        {
            "DeliveryId": "INV12345",
            "ProductName": "Product A",
            "Quantity": "2",
            "Unit": "pcs",
            "UnitPrice": "5000",
            "TotalPrice": "10000",
            "Origin": "Japan",
            "Remarks": "Remarks"
        },
        {
            "DeliveryId": "INV12345",
            "ProductName": "Product B",
            "Quantity": "3",
            "Unit": "pcs",
            "UnitPrice": "1000",
            "TotalPrice": "3000",
            "Origin": "Japan",
            "Remarks": "Remarks"
        }
    ]
}
"""

    async def async_llm_response(self, user_input, base64_image, model_temp=0.3):
        response_json = await self.client.chat.completions.create(
        model="gpt-4o",
        response_format={ "type": "json_object" },
        messages=[
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": [
                {"type": "text", "text": user_input},
                {"type": "image_url", "image_url": {
                    "url": f"data:image/png;base64, {base64_image}",
                    "detail": "high" # https://platform.openai.com/docs/guides/vision
                }}
            ]}
        ],
        max_tokens=self.max_tokens,
        temperature=model_temp,
    )
        self.logger.info(f"usage token: {response_json.usage}")
        self.logger.info(f"response: {response_json.choices[0].message.content}")
        return response_json.choices[0].message.content

    async def async_stream_llm_response(self, user_input, base64_image, model_temp=0.3):
        response_message = ""

        for chunk in await self.client.chat.completions.create(
        model="gpt-4o",
        response_format={ "type": "json_object" },
        messages=[
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": [
                {"type": "text", "text": user_input},
                {"type": "image_url", "image_url": {
                    "url": f"data:image/png;base64, {base64_image}"
                }}
            ]}
        ],
        max_tokens=self.max_tokens,
        temperature=model_temp,
        stream=True
        ):
            choice = chunk.choices[0] if hasattr(chunk, 'choices') and chunk.choices else ""
            if hasattr(choice, 'delta') and hasattr(choice.delta, 'content'):
                content = chunk.choices[0].delta.content
                response_message += content if content else ""
                yield content


    async def async_enhanced_ocr_llm_response(self, image_path, base64_image, model_temp=0.3):
        self.logger.info("*** Running enhanced OCR LLM response ***")
        DEFAULT_OCR_PROMPT = "**OCR text:**"
        OCR_SYSTEM_PROMPT = f"Additional instructions: - You're known to be good at recognizing equations and complete partially occluded text. Additional information has been generated by an OCR model regarding text present in the image in format of {DEFAULT_OCR_PROMPT}. However, you should refrain from incorporating the text information into your description, and only consult the OCR text when the text within the image is unclear to you. Follow your original analysis if OCR text does not help. "

        ocr_client = self.ocr_client
        ocr_result = ocr_client.run_ocr(image_path)
        self.logger.info(f"ocr_result: {ocr_result}")

        response_json = await self.client.chat.completions.create(
        model="gpt-4o",
        response_format={ "type": "json_object" },
        messages=[
            {"role": "system", "content": "You are AI assistant to help extract information"},
            {"role": "system", "content": [
                {"type": "text", "text": OCR_SYSTEM_PROMPT},
            ]},
            {"role": "user", "content": [
                {"type": "text", "text": f"{DEFAULT_OCR_PROMPT} {ocr_result}"},
                {"type": "image_url", "image_url": {
                    "url": f"data:image/png;base64, {base64_image}",
                    "detail": "high" # https://platform.openai.com/docs/guides/vision
                }},
                {"type": "text", "text": AFTER_OCR_SYSTEM_PROMPT_EN}
            ]}
        ],
        max_tokens=self.max_tokens,
        temperature=model_temp,
    )
        self.logger.info(f"usage token: {response_json.usage}")
        self.logger.info(f"response: {response_json.choices[0].message.content}")

        return response_json.choices[0].message.content