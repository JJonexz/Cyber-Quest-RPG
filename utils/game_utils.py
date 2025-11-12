# utils/game_utils.py - NUEVO ARCHIVO CON FUNCIONALIDADES ADICIONALES
import random
import time
from typing import List, Dict
from config.colors import COLORS

class GameUtils:
    """Utilidades adicionales para el juego"""
    
    @staticmethod
    def calculate_difficulty_multiplier(difficulty: str) -> float:
        """Calcula multiplicador de dificultad"""
        multipliers = {
            'facil': 0.8,
            'medio': 1.0,
            'dificil': 1.3
        }
        return multipliers.get(difficulty, 1.0)
    
    @staticmethod
    def generate_random_name() -> str:
        """Genera nombres aleatorios para IAs"""
        names = [
            "Neo", "Trinity", "Morpheus", "Cypher", "Tank", "Apoc", "Switch",
            "Byte", "Crypto", "Vector", "Matrix", "Oracle", "Architect", "Smith",
            "Persephone", "Merovingian", "Seraph", "Niobe", "Lock", "Link",
            "Mifune", "Ghost", "Spark", "Blaze", "Vortex", "Phantom", "Wraith"
        ]
        return random.choice(names)
    
    @staticmethod
    def format_time(seconds: int) -> str:
        """Formatea tiempo en formato legible"""
        if seconds < 60:
            return f"{seconds}s"
        elif seconds < 3600:
            minutes = seconds // 60
            remaining_seconds = seconds % 60
            return f"{minutes}m {remaining_seconds}s"
        else:
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            return f"{hours}h {minutes}m"
    
    @staticmethod
    def calculate_level(score: int) -> int:
        """Calcula nivel basado en puntuación"""
        return min(100, max(1, score // 1000))
    
    @staticmethod
    def get_achievement(progress: int, errors: int, time_taken: int) -> str:
        """Determina logro basado en desempeño"""
        if progress >= 100 and errors == 0 and time_taken < 30:
            return "🏆 PERFECCIÓN ABSOLUTA"
        elif progress >= 100 and errors <= 2:
            return "⭐ ÉLITE CYBER"
        elif progress >= 100:
            return "✅ OPERACIÓN EXITOSA"
        elif progress >= 80:
            return "🎯 CASI PERFECTO"
        elif progress >= 50:
            return "⚡ BUEN ESFUERZO"
        else:
            return "🔍 ENTRENAMIENTO"
    
    @staticmethod
    def create_progress_bar(progress: int, width: int = 50) -> str:
        """Crea una barra de progreso en texto"""
        filled = int(width * progress / 100)
        empty = width - filled
        return f"[{'█' * filled}{'░' * empty}] {progress}%"
    
    @staticmethod
    def analyze_performance(stats: Dict) -> Dict:
        """Analiza el desempeño del jugador"""
        progress = stats.get('progress', 0)
        errors = stats.get('errors', 0)
        time_taken = stats.get('time', 0)
        
        efficiency = (progress / max(1, time_taken)) * 100
        accuracy = max(0, 100 - (errors * 10))
        
        return {
            'efficiency': round(efficiency, 2),
            'accuracy': round(accuracy, 2),
            'overall_score': round((efficiency + accuracy) / 2, 2),
            'grade': 'A' if efficiency > 80 and accuracy > 80 else 
                    'B' if efficiency > 60 and accuracy > 60 else 
                    'C' if efficiency > 40 and accuracy > 40 else 'D'
        }

class AnimationEffects:
    """Efectos de animación para el juego"""
    
    @staticmethod
    def create_glow_effect(color: str, intensity: int = 10) -> str:
        """Crea efecto de resplandor"""
        return f"0 0 {intensity}px {color}"
    
    @staticmethod
    def pulsate_color(base_color: str, phase: float) -> str:
        """Crea efecto de color pulsante"""
        # Implementación básica - puede expandirse
        return base_color
    
    @staticmethod
    def calculate_transition_delay(index: int, base_delay: float = 0.1) -> float:
        """Calcula retraso para efectos secuenciales"""
        return base_delay * index