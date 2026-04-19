from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

# Use the actual API key from .env
api_key = os.getenv('GROQ_API_KEY')
if not api_key:
    print("Error: GROQ_API_KEY not found in .env file")
    exit(1)

print(f"Using API key: {api_key[:10]}...")  # Show first 10 chars for verification
client = Groq(api_key=api_key)

response = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[
        {"role": "user", "content": "Hello, Groq! Give me a short AI quote."}
    ],
)

print(response.choices[0].message.content)