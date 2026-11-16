import os
import streamlit as st
from dotenv import load_dotenv
load_dotenv()
def get_config(key):
    value = os.getenv(key)
    if value:
        return value
    try:
        return st.secrets.get(key)
    except Exception:
        return None
GROQ_API_KEY = get_config("GROQ_API_KEY")
GROQ_MODEL = get_config("GROQ_MODEL") or "openai/gpt-oss-20b"
SERPER_API_KEY = get_config("SERPER_API_KEY")
