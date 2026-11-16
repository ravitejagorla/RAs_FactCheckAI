import os
from dotenv import load_dotenv
load_dotenv()
GROQ_MODEL = os.getenv('GROQ_MODEL')
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
SERPER_API_KEY = os.getenv("SERPER_API_KEY")