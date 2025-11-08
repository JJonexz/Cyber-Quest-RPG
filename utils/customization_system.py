# customization_system.py
import json
import os
from typing import Dict, List

class CustomizationSystem:
    """Sistema de personalización de personajes"""
    
    def __init__(self, filename='data/customization.json'):
        self.filename = filename
        self._ensure_data_folder()
        self.customizations = self._load_customizations()
    
    def _ensure_data_folder(self):
        os.makedirs('data', exist_ok=True)
    
    def _load_customizations(self) -> Dict:
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def save_customization(self, player_name: str, character_type: str, customization: Dict):
        """Guarda la personalización del personaje"""
        key = f"{player_name}_{character_type}"
        self.customizations[key] = customization
        
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(self.customizations, f, indent=2, ensure_ascii=False)
    
    def get_customization(self, player_name: str, character_type: str) -> Dict:
        """Obtiene la personalización del personaje"""
        key = f"{player_name}_{character_type}"
        return self.customizations.get(key, self.get_default_customization(character_type))
    
    def get_default_customization(self, character_type: str) -> Dict:
        """Obtiene personalización por defecto"""
        return {
            'color_scheme': 'default',
            'accessories': [],
            'title': 'Novato',
            'special_ability': None
        }
    
    def get_available_accessories(self, character_type: str) -> List[Dict]:
        """Obtiene accesorios disponibles para el personaje"""
        accessories = {
            'usuario': [
                {'id': 'shield', 'name': 'Escudo Digital', 'icon': '🛡️', 'effect': 'reduce_errors'},
                {'id': 'analyzer', 'name': 'Analizador', 'icon': '🔍', 'effect': 'increase_success'}
            ],
            'hacker': [
                {'id': 'toolkit', 'name': 'Kit Herramientas', 'icon': '🔧', 'effect': 'boost_progress'},
                {'id': 'cloak', 'name': 'Capa Digital', 'icon': '👻', 'effect': 'reduce_detection'}
            ],
            'cyberdelincuente': [
                {'id': 'mask', 'name': 'Máscara Anónima', 'icon': '🎭', 'effect': 'hide_identity'},
                {'id': 'virus', 'name': 'Virus Controlado', 'icon': '🦠', 'effect': 'sabotage_ai'}
            ]
        }
        return accessories.get(character_type, [])