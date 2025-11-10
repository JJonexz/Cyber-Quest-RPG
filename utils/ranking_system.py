# utils/ranking_system.py - VERSIÓN CORREGIDA Y MEJORADA
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
        try:
            os.makedirs('data', exist_ok=True)
            print(f"✅ Carpeta data verificada/creada")
        except Exception as e:
            print(f"⚠️ Error creando carpeta data: {e}")
    
    def _load_rankings(self) -> List[Dict]:
        """Carga el ranking desde archivo"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        print(f"✅ Ranking cargado: {len(data)} entradas")
                        return data
                    else:
                        print("⚠️ Formato de ranking inválido, inicializando vacío")
                        return []
            except json.JSONDecodeError as e:
                print(f"⚠️ Error decodificando JSON: {e}")
                return []
            except Exception as e:
                print(f"⚠️ Error cargando ranking: {e}")
                return []
        else:
            print("ℹ️ Archivo de ranking no existe, será creado")
            return []
    
    def save_ranking(self):
        """Guarda el ranking en archivo"""
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(self.rankings, f, indent=2, ensure_ascii=False)
            print(f"✅ Ranking guardado: {len(self.rankings)} entradas")
        except Exception as e:
            print(f"❌ Error guardando ranking: {e}")
    
    def add_score(self, player_name: str, character: str, time_taken: float, 
                  errors: int, completed: bool):
        """Añade una nueva puntuación - CORREGIDO"""
        try:
            # Validar datos de entrada
            if not player_name or not player_name.strip():
                print("⚠️ Nombre de jugador vacío, no se guardará puntuación")
                return
            
            # Calcular puntuación
            score = self._calculate_score(time_taken, errors, completed)
            
            score_data = {
                'player': player_name.strip(),
                'character': character,
                'time': round(time_taken, 2),
                'errors': int(errors),
                'completed': bool(completed),
                'score': round(score, 2),
                'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            print(f"📊 Guardando puntuación: {score_data}")
            
            # Añadir nueva puntuación
            self.rankings.append(score_data)
            
            # CORRECCIÓN: Ordenar correctamente
            # Primero por completado (True primero), luego por score descendente
            self.rankings.sort(key=lambda x: (not x['completed'], -x['score']))
            
            # Mantener solo top 100
            self.rankings = self.rankings[:100]
            
            # Guardar inmediatamente
            self.save_ranking()
            
            print(f"✅ Puntuación guardada exitosamente")
            
        except Exception as e:
            print(f"❌ Error añadiendo puntuación: {e}")
            import traceback
            traceback.print_exc()
    
    def _calculate_score(self, time_taken: float, errors: int, completed: bool) -> float:
        """Calcula puntuación final - MEJORADO Y BALANCEADO"""
        if not completed:
            # Si no completó, puntuación mínima basada en progreso
            return 0
        
        # Puntuación base por completar
        base_score = 10000
        
        # Penalización por tiempo (más suave)
        time_penalty = time_taken * 5  # Reducido de 8 a 5
        
        # Penalización por errores (más suave)
        error_penalty = errors * 200   # Reducido de 300 a 200
        
        # Calcular puntuación
        final_score = base_score - time_penalty - error_penalty
        
        # Bonificaciones por desempeño excepcional
        if time_taken < 30 and errors == 0:
            final_score += 3000  # Bonus perfección
        elif time_taken < 30:
            final_score += 2000  # Bonus velocidad
        elif time_taken < 60:
            final_score += 1000  # Bonus buen tiempo
        
        if errors == 0:
            final_score += 1500  # Bonus sin errores
        elif errors <= 2:
            final_score += 500   # Bonus pocos errores
        
        # Asegurar puntuación mínima de 100 para completados
        final_score = max(100, final_score)
        
        return final_score
    
    def get_top_rankings(self, limit=10) -> List[Dict]:
        """Obtiene los mejores rankings"""
        return self.rankings[:limit]
    
    def get_player_best_score(self, player_name: str) -> Dict:
        """Obtiene la mejor puntuación de un jugador"""
        player_scores = [r for r in self.rankings if r['player'] == player_name]
        if player_scores:
            return player_scores[0]  # Ya están ordenados
        return None
    
    def get_character_rankings(self, character: str, limit=10) -> List[Dict]:
        """Obtiene rankings de un personaje específico"""
        char_rankings = [r for r in self.rankings if r['character'] == character]
        return char_rankings[:limit]
    
    def get_ranking_statistics(self) -> Dict:
        """Obtiene estadísticas generales del ranking"""
        if not self.rankings:
            return {
                'total_games': 0,
                'completed_games': 0,
                'average_score': 0,
                'best_time': 0,
                'total_players': 0
            }
        
        completed = [r for r in self.rankings if r['completed']]
        
        return {
            'total_games': len(self.rankings),
            'completed_games': len(completed),
            'average_score': sum(r['score'] for r in completed) / len(completed) if completed else 0,
            'best_time': min(r['time'] for r in completed) if completed else 0,
            'total_players': len(set(r['player'] for r in self.rankings))
        }
    
    def clear_rankings(self):
        """Limpia todos los rankings"""
        self.rankings = []
        self.save_ranking()
        print("🗑️ Ranking limpiado")
    
    def export_rankings_csv(self, filename='data/ranking_export.csv'):
        """Exporta rankings a CSV"""
        try:
            import csv
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                if self.rankings:
                    writer = csv.DictWriter(f, fieldnames=self.rankings[0].keys())
                    writer.writeheader()
                    writer.writerows(self.rankings)
            print(f"✅ Rankings exportados a {filename}")
        except Exception as e:
            print(f"❌ Error exportando rankings: {e}")
    
    def verify_ranking_integrity(self) -> bool:
        """Verifica la integridad del archivo de ranking"""
        try:
            if not os.path.exists(self.filename):
                print("⚠️ Archivo de ranking no existe")
                return False
            
            with open(self.filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            if not isinstance(data, list):
                print("❌ Ranking no es una lista")
                return False
            
            # Verificar estructura de cada entrada
            required_keys = ['player', 'character', 'time', 'errors', 'completed', 'score', 'date']
            for entry in data:
                if not all(key in entry for key in required_keys):
                    print(f"❌ Entrada con estructura inválida: {entry}")
                    return False
            
            print("✅ Integridad del ranking verificada")
            return True
            
        except Exception as e:
            print(f"❌ Error verificando integridad: {e}")
            return False