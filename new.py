import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Get all models
models = list(genai.list_models()) 
print("Available models:")
for m in models:
    print(m)
