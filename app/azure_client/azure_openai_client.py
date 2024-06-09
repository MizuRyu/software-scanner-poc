import os
from openai import AzureOpenAI, AsyncAzureOpenAI
from dotenv import load_dotenv

from app.config.prompts import SYSTEM_PROMPT

load_dotenv()

class AzureOpenAIClient:
    def __init__(self):
        self.client = AzureOpenAI(
            api_version=os.getenv("API_VERSION"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        )

        self.system_prompt = SYSTEM_PROMPT
        self.max_tokens = 800

    def dummy_response(self, user_input, base64_encoded):
        return """
        {
    "date": "2022-01-01",
    "time": "12:00:00",
    "products": [
        {
            "name": "product1",
            "price": 100
        },
        {
            "name": "product2",
            "price": 200
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
        self.client = AsyncAzureOpenAI(
            api_version=os.getenv("API_VERSION"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        )

        self.system_prompt = SYSTEM_PROMPT
        self.max_tokens = 800

    async def async_dummy_response(self, user_input, base64_encoded):
        return """
        {
    "date": "2022-01-01",
    "time": "12:00:00",
    "products": [
        {
            "name": "product1",
            "price": 100
        },
        {
            "name": "product2",
            "price": 200
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