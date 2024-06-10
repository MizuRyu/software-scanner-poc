import os
from openai import AzureOpenAI, AsyncAzureOpenAI
from dotenv import load_dotenv

from app.config.prompts import SYSTEM_PROMPT_EN
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
            "DeliveryDate": "2022-01-01",
            "Publisher": "ABC Corporation",
            "Subtotal": "10000",
            "Tax": "1000",
            "Total": "11000"
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
            "Origin": "Japan"
        },
        {
            "DeliveryId": "INV12345",
            "ProductName": "Product B",
            "Quantity": "3",
            "Unit": "pcs",
            "UnitPrice": "1000",
            "TotalPrice": "3000",
            "Origin": "Japan"
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

    async def async_dummy_response(self, user_input, base64_encoded):
        return """
{
    "DeliveryNotes": [
        {
            "DeliveryId": "INV12345",
            "Recipient": "Taro Yamada",
            "DeliveryDate": "2022-01-01",
            "Publisher": "ABC Corporation",
            "Subtotal": "10000",
            "Tax": "1000",
            "Total": "11000"
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
            "Origin": "Japan"
        },
        {
            "DeliveryId": "INV12345",
            "ProductName": "Product B",
            "Quantity": "3",
            "Unit": "pcs",
            "UnitPrice": "1000",
            "TotalPrice": "3000",
            "Origin": "Japan"
        }
    ]
}
        """

    async def async_llm_response(self, user_input, base64_image, model_temp=0.3):
        response = await self.client.chat.completions.create(
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