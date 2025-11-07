# ============================================================================
# ARCHIVO: models/character.py
# DESCRIPCIÓN: Define las clases de personajes del juego y sus atributos.
#              Incluye configuración de dificultad y características únicas.
# ============================================================================

from typing import Dict, List

class Character:
    """Clase base para personajes del juego"""
    
    def __init__(self, char_type: str, name: str, difficulty: str):
        self.type = char_type
        self.name = name
        self.difficulty = difficulty
        self.progress = 0
        self.errors = 0
        self.completed = False
    
    def update_progress(self, amount: int):
        """Actualiza el progreso del personaje"""
        self.progress = min(100, self.progress + amount)
        if self.progress >= 100:
            self.completed = True
    
    def add_error(self):
        """Registra un error"""
        self.errors += 1

class CharacterDatabase:
    """Base de datos de personajes disponibles"""
    
    @staticmethod
    def get_all_characters() -> List[Dict]:
        """Retorna información de todos los personajes"""
        return [
            {
                'name': 'Usuario',
                'type': 'usuario',
                'icon': '👤',
                'difficulty': 'FÁCIL',
                'description': 'Un ciudadano común atrapado en una situación peligrosa. Debe sobrevivir y proteger su información.',
                'color': '#00b894'
            },
            {
                'name': 'Hacker Ético',
                'type': 'hacker',
                'icon': '💻',
                'difficulty': 'MEDIO',
                'description': 'Experto en seguridad informática. Usa sus habilidades para exponer vulnerabilidades y proteger sistemas.',
                'color': '#3498db'
            },
            {
                'name': 'Cyberdelincuente',
                'type': 'cyberdelincuente',
                'icon': '🎭',
                'difficulty': 'DIFÍCIL',
                'description': 'Maestro del sigilo digital. Opera en las sombras para lograr objetivos complejos sin ser detectado.',
                'color': '#e74c3c'
            }
        ]
