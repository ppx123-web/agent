from openai import OpenAI
import os

class DeepSeek:
    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv("DEEPSEEK_API_KEY"), 
            base_url="https://api.deepseek.com"
        )

    def ask(self, prompt: str):
        messages = [
            {
                "role": "user",
                "content": prompt,
            }
        ]
        response = self.client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            temperature=0.1,
        )
        return response.choices[0].message.content
