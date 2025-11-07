
# ============================================================================
# ARCHIVO: ai/ai_player.py
# DESCRIPCIÓN: Sistema de Inteligencia Artificial para controlar personajes
#              no seleccionados por el jugador. Toma decisiones estratégicas.
# ============================================================================

import random
from typing import Dict, List

class AIPlayer:
    """IA que controla personajes no seleccionados"""
    
    def __init__(self, character_type: str, difficulty: str):
        self.character_type = character_type
        self.difficulty = difficulty
        self.progress = 0
        self.errors = 0
        self.completed = False
        
    def make_decision(self, options: List[Dict]) -> Dict:
        """La IA toma decisiones según su personaje y dificultad"""
        if self.difficulty == 'facil':
            # Preferir opciones seguras
            safe_options = [opt for opt in options if opt['risk'] == 'bajo']
            return random.choice(safe_options if safe_options else options)
        elif self.difficulty == 'medio':
            # Balance entre riesgo y recompensa
            return random.choices(options, weights=[opt['success'] for opt in options])[0]
        else:  # dificil
            # Preferir opciones arriesgadas pero efectivas
            risky_options = [opt for opt in options if opt['risk'] == 'alto']
            return random.choice(risky_options if risky_options else options)
    
    def update_progress(self, success: bool, time_taken: int):
        """Actualiza el progreso de la IA"""
        if success:
            self.progress += random.randint(15, 25)
        else:
            self.errors += 1
            self.progress += random.randint(5, 10)
        
        if self.progress >= 100:
            self.completed = True

