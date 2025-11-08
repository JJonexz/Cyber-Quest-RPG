
# ============================================================================
# ARCHIVO: utils/ranking_system.py
# DESCRIPCIÓN: Sistema de gestión de ranking y puntuaciones. Maneja la
#              persistencia de datos y cálculo de scores.
# ============================================================================

import json
import os
from datetime import datetime
from typing import List, Dict

class RankingSystem:
    """Gestiona el ranking de jugadores"""
    
    def __init__(self, filename='data/ranking.json'):
        self.filename = filename
        self._ensure_data_folder()
        self.rankings = self._load_rankings()
    
    def _ensure_data_folder(self):
        """Crea la carpeta data si no existe"""
        os.makedirs('data', exist_ok=True)
    
    def _load_rankings(self) -> List[Dict]:
        """Carga el ranking desde archivo"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def save_ranking(self):
        """Guarda el ranking en archivo"""
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(self.rankings, f, indent=2, ensure_ascii=False)
    
    def add_score(self, player_name: str, character: str, time_taken: float, 
                  errors: int, completed: bool):
        """Añade una nueva puntuación"""
        score = {
            'player': player_name,
            'character': character,
            'time': round(time_taken, 2),
            'errors': errors,
            'completed': completed,
            'score': self._calculate_score(time_taken, errors, completed),
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        self.rankings.append(score)
        self.rankings.sort(key=lambda x: (-x['completed'], x['score']), reverse=True)
        self.save_ranking()
    
    def _calculate_score(self, time_taken: float, errors: int, completed: bool) -> float:
        """Calcula puntuación final"""
        if not completed:
            return 0
        
        base_score = 10000
        time_penalty = time_taken * 10
        error_penalty = errors * 500
        
        return max(0, base_score - time_penalty - error_penalty)
    
    def get_top_rankings(self, limit=10) -> List[Dict]:
        """Obtiene los mejores rankings"""
        return self.rankings[:limit]
# utils/ranking_system.py (corregido)

class RankingSystem:
    # ... código existente ...
    
    def add_score(self, player_name: str, character: str, time_taken: float, 
                  errors: int, completed: bool):
        """Añade una nueva puntuación - CORREGIDO"""
        score = {
            'player': player_name,
            'character': character,
            'time': round(time_taken, 2),
            'errors': errors,
            'completed': completed,
            'score': self._calculate_score(time_taken, errors, completed),
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        self.rankings.append(score)
        # CORRECCIÓN: Ordenar correctamente
        self.rankings.sort(key=lambda x: (-x['completed'], -x['score']))
        
        # Mantener solo top 50
        self.rankings = self.rankings[:50]
        self.save_ranking()
    
    def _calculate_score(self, time_taken: float, errors: int, completed: bool) -> float:
        """Calcula puntuación final - MEJORADO"""
        if not completed:
            return 0
        
        base_score = 10000
        time_penalty = time_taken * 8  # Reducido de 10 a 8
        error_penalty = errors * 300   # Reducido de 500 a 300
        
        final_score = max(0, base_score - time_penalty - error_penalty)
        
        # Bonus por bajo tiempo
        if time_taken < 30:  # Menos de 30 segundos
            final_score += 2000
        elif time_taken < 60:  # Menos de 1 minuto
            final_score += 1000
        
        return final_score
