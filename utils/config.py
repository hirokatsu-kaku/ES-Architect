import os
import streamlit as st
from dotenv import load_dotenv

# Load .env file if present
load_dotenv()

def get_env_var(key: str) -> str:
    """
    Retrieves an environment variable/secret safely.
    Prioritizes os.getenv (local), then checks st.secrets (cloud).
    """
    # 1. Try local environment variable
    val = os.getenv(key)
    if val:
        return val
    
    # 2. Try Streamlit Secrets (for Cloud deployment)
    # st.secrets works like a dict
    if key in st.secrets:
        return st.secrets[key]
    
    return None
