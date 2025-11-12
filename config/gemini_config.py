# config/gemini_config.py
# Este archivo puede quedar para uso futuro si decides instalar google-generativeai
import os

GEMINI_CONFIG = {
    'api_key': os.getenv('AIzaSyA0KzSkYvmfzYxMqLBp9CHnkFjtgzHjvyY'),
    'model': 'gemini-2.5',
    'max_tokens': 50
}