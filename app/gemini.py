import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-1.5-flash")

# Non-streaming call (optional, not used now)
async def call_gemini(query: str) -> str:
    try:
        response = model.generate_content(query)
        return response.text.strip()
    except Exception as e:
        return f"[Gemini Error] {str(e)}"

# Streaming response generator
async def stream_gemini_response(query: str):
    try:
        response = model.generate_content(query, stream=True)
        for chunk in response:
            if chunk.text:
                yield chunk.text
    except Exception as e:
        yield f"[Gemini Streaming Error] {str(e)}"
