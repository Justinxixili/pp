
import openai
from django.conf import settings


class LLMService:
    def __init__(self):
        openai.api_key = settings.OPENAI_API_KEY

    def analyze(self, prompt: str):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a patent analysis expert."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            raise