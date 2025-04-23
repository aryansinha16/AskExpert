import openai
import os

client = openai.OpenAI(
    api_key=os.getenv('OPENAI_API'),
    base_url=os.getenv('OPENAI_BASE_URL')
)
