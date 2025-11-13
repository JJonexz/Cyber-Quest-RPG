# effects_system.py
import random
from typing import Dict, List

class EffectsSystem:
    """Sistema de efectos visuales y de juego"""
    
    def __init__(self):
        self.active_effects = {}
        self.character_states = {}
    
    def apply_effect(self, player_id: str, effect_type: str, duration: int = 3):
        """Aplica un efecto al jugador"""
        self.active_effects[player_id] = {
            'type': effect_type,
            'duration': duration,
            'applied_at': 0  # Se actualizará con el tiempo del juego
        }
    
    def get_character_appearance(self, character_type: str, effects: List[str]) -> Dict:
        """Obtiene la apariencia del personaje basada en efectos"""
        base_appearances = {
            'usuario': {'icon': '👤', 'color': '#00b894', 'posture': 'normal'},
            'hacker': {'icon': '💻', 'color': '#3498db', 'posture': 'focused'},
            'cyberdelincuente': {'icon': '🎭', 'color': '#e74c3c', 'posture': 'stealth'}
        }
        
        appearance = base_appearances.get(character_type, base_appearances['usuario']).copy()
        
        # Modificar apariencia basada en efectos
        for effect in effects:
            if effect == 'virus':
                appearance['icon'] = '🤢'
                appearance['color'] = '#541170'
                appearance['posture'] = 'infected'
            elif effect == 'firewall_blocked':
                appearance['icon'] = '🚫'
                appearance['posture'] = 'blocked'
            elif effect == 'success':
                appearance['icon'] = '⚡'
                appearance['posture'] = 'empowered'
            elif effect == 'detected':
                appearance['icon'] = '🚨'
                appearance['posture'] = 'alert'
        
        return appearance
    
    def get_effect_description(self, effect_type: str) -> str:
        """Obtiene descripción del efecto"""
        descriptions = {
            'virus': "🔴 VIRUS DETECTADO - Velocidad reducida 30%",
            'firewall_blocked': "🛡️ FIREWALL - Acciones bloqueadas temporalmente",
            'data_breach': "💾 BRECHA DE DATOS - Información expuesta",
            'system_override': "⚡ SOBRECARGA - Habilidades mejoradas",
            'encryption': "🔒 ENCRIPTADO - Defensas fortalecidas"
        }
        return descriptions.get(effect_type, "Efecto desconocido")