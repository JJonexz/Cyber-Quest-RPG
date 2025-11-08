# dialog_engine.py
import google.generativeai as genai
import os
from typing import Dict, List
import random

class DialogEngine:
    """Motor de diálogos con Gemini AI"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        if self.api_key:
            try:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel('gemini-pro')
                self.enabled = True
            except:
                self.enabled = False
        else:
            self.enabled = False
    
    def generate_character_dialog(self, character_type: str, situation: str, emotion: str = "neutral") -> str:
        """Genera diálogo contextual para personajes"""
        if not self.enabled:
            return self._get_fallback_dialog(character_type, situation, emotion)
        
        try:
            prompt = f"""
            Como {character_type} en un juego cyberpunk, responde brevemente (máximo 15 palabras) a esta situación: {situation}.
            Emoción: {emotion}. Mantén el estilo cyberpunk.
            """
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except:
            return self._get_fallback_dialog(character_type, situation, emotion)
    
    def _get_fallback_dialog(self, character_type: str, situation: str, emotion: str) -> str:
        """Diálogos de respaldo cuando Gemini no está disponible"""
        dialogs = {
            'usuario': {
                'neutral': ["El sistema parece estable... por ahora.", "Verificando protocolos de seguridad."],
                'stressed': ["¡La presión aumenta!", "Necesito mantener la calma..."],
                'victory': ["¡Lo logré! El sistema es seguro.", "Victoria para los usuarios comunes."]
            },
            'hacker': {
                'neutral': ["Analizando vectores de ataque...", "Firewalls detectados."],
                'stressed': ["¡Contramedidas activadas!", "El sistema se defiende..."],
                'victory': ["¡Sistemas expuestos! Justicia digital.", "La verdad sale a la luz."]
            },
            'cyberdelincuente': {
                'neutral': ["Operando en las sombras...", "Rastreo evadido."],
                'stressed': ["¡Casi me detectan!", "Activando protocolos de escape..."],
                'victory': ["¡El botín es mío!", "Operación completada con éxito."]
            }
        }
        return random.choice(dialogs.get(character_type, {}).get(emotion, ["Procesando..."]))

# Agregar al __init__.py de utils