# config/gemini_config.py
# Este archivo puede quedar para uso futuro si decides instalar google-generativeai
import os

GEMINI_CONFIG = {
    'api_key': os.getenv('GEMINI_API_KEY'),
    'model': 'gemini-pro',
    'max_tokens': 50
}