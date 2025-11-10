# utils/ranking_system.py
import json
import os
from datetime import datetime
from typing import List, Dict

class RankingSystem:
    """Gestiona el ranking de jugadores - VERSIÓN CORREGIDA"""
    
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
                    data = json.load(f)
                    if isinstance(data, list):
                        return data
                    else:
                        return []
            except (json.JSONDecodeError, Exception) as e:
                print(f"Error cargando ranking: {e}")
                return []
        return []
    
    def save_ranking(self):
        """Guarda el ranking en archivo"""
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(self.rankings, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error guardando ranking: {e}")
    
    def add_score(self, player_name: str, character: str, time_taken: float, 
                  errors: int, completed: bool):
        """Añade una nueva puntuación - CORREGIDO"""
        score_data = {
            'player': player_name.strip(),
            'character': character,
            'time': round(time_taken, 2),
            'errors': errors,
            'completed': completed,
            'score': self._calculate_score(time_taken, errors, completed),
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        self.rankings.append(score_data)
        
        # CORRECCIÓN: Ordenar correctamente (completados primero, luego por score descendente)
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
    
    def get_top_rankings(self, limit=10) -> List[Dict]:
        """Obtiene los mejores rankings"""
        return self.rankings[:limit]
    
    def clear_rankings(self):
        """Limpia todos los rankings (para testing)"""
        self.rankings = []
        self.save_ranking()