# ============================================================================
# ARCHIVO: ai/ai_player.py - VERSIÓN MEJORADA
# DESCRIPCIÓN: Sistema de IA mejorado con decisiones estratégicas avanzadas
# ============================================================================

import random
from typing import Dict, List

class AIPlayer:
    """IA mejorada que controla personajes no seleccionados"""
    
    def __init__(self, character_type: str, difficulty: str):
        self.character_type = character_type
        self.difficulty = difficulty
        self.progress = 0
        self.errors = 0
        self.completed = False
        self.conservative_turns = 0
        
    def make_decision(self, options: List[Dict], current_state: Dict = None) -> Dict:
        """La IA toma decisiones inteligentes según su personaje, dificultad y estado actual"""
        
        # Evaluar opciones con pesos estratégicos
        scored_options = []
        
        for option in options:
            score = self._evaluate_option(option, current_state)
            scored_options.append((option, score))
        
        # Ordenar por mejor puntuación
        scored_options.sort(key=lambda x: x[1], reverse=True)
        
        # Seleccionar según dificultad
        if self.difficulty == 'facil':
            # Siempre elige la opción más segura entre las top 3
            safe_options = [opt for opt, score in scored_options[:3] if opt['risk'] == 'bajo']
            return random.choice(safe_options) if safe_options else scored_options[0][0]
            
        elif self.difficulty == 'medio':
            # Balance estratégico - prefiere opciones balanceadas
            if current_state and current_state['detection'] > 60:
                # Si la detección es alta, ser más conservador
                safe_options = [opt for opt, score in scored_options[:3] if opt['risk'] in ['bajo', 'medio']]
                return random.choice(safe_options) if safe_options else scored_options[0][0]
            else:
                # Tomar riesgos calculados
                return scored_options[0][0]
                
        else:  # dificil
            # Estrategia agresiva pero inteligente
            if current_state and current_state['health'] < 40:
                # Si la salud es baja, ser más conservador
                safe_options = [opt for opt, score in scored_options[:2] if opt['risk'] != 'alto']
                return random.choice(safe_options) if safe_options else scored_options[0][0]
            else:
                # Buscar la opción con mejor relación riesgo/recompensa
                high_risk_high_reward = [opt for opt, score in scored_options if opt['risk'] == 'alto' and opt['success'] >= 70]
                if high_risk_high_reward and random.random() < 0.7:
                    return random.choice(high_risk_high_reward)
                return scored_options[0][0]
    
    def _evaluate_option(self, option: Dict, current_state: Dict = None) -> float:
        """Evalúa y puntúa una opción basándose en múltiples factores"""
        base_score = option['success']
        
        # Modificadores basados en riesgo
        risk_modifiers = {'bajo': 1.2, 'medio': 1.0, 'alto': 0.8}
        base_score *= risk_modifiers.get(option['risk'], 1.0)
        
        # Modificadores basados en el personaje
        char_modifiers = {
            'usuario': {'bajo': 1.3, 'medio': 1.0, 'alto': 0.6},
            'hacker': {'bajo': 1.0, 'medio': 1.2, 'alto': 1.0},
            'cyberdelincuente': {'bajo': 0.8, 'medio': 1.0, 'alto': 1.3}
        }
        char_mod = char_modifiers.get(self.character_type, {}).get(option['risk'], 1.0)
        base_score *= char_mod
        
        # Modificadores basados en estado actual (si está disponible)
        if current_state:
            # Si la detección es alta, evitar riesgos
            if current_state['detection'] > 70 and option['risk'] == 'alto':
                base_score *= 0.5
            elif current_state['detection'] > 70 and option['risk'] == 'bajo':
                base_score *= 1.3
            
            # Si los recursos son bajos, evitar opciones que consuman mucho tiempo
            if current_state['resources'] < 30 and option['time'] > 2:
                base_score *= 0.8
            
            # Si la salud es baja, ser conservador
            if current_state['health'] < 40 and option['risk'] == 'alto':
                base_score *= 0.6
        
        # Pequeña variación aleatoria para evitar patrones predecibles
        variation = random.uniform(0.95, 1.05)
        base_score *= variation
        
        return base_score
    
    def update_progress(self, success: bool, time_taken: int):
        """Actualiza el progreso de la IA - MEJORADO"""
        if success:
            progress_gain = random.randint(15, 25)
            # Bonus por dificultad
            if self.difficulty == 'dificil':
                progress_gain += random.randint(5, 10)
            self.progress += progress_gain
        else:
            self.errors += 1
            self.progress += random.randint(5, 10)
        
        self.progress = min(100, self.progress)
        
        if self.progress >= 100:
            self.completed = True
    
    def get_decision_info(self) -> str:
        """Retorna información sobre la estrategia de la IA"""
        strategies = {
            'facil': "Estrategia conservadora - Minimizar riesgos",
            'medio': "Estrategia balanceada - Riesgos calculados", 
            'dificil': "Estrategia agresiva - Maximizar eficiencia"
        }
        return f"IA {self.character_type} ({self.difficulty}): {strategies[self.difficulty]}"