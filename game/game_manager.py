# ============================================================================
# ARCHIVO: game/game_manager.py
# DESCRIPCIÓN: Gestor principal del juego. Coordina todas las pantallas,
#              el flujo del juego y la lógica principal.
# ============================================================================

import tkinter as tk
from tkinter import font as tkfont
import time
import random

from config.colors import COLORS
from models.story import StoryGenerator
from ai.ai_player import AIPlayer
from utils.ranking_system import RankingSystem
from ui.screens import GameScreens

class CyberQuestGame:
    """Clase principal del juego"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("CYBER QUEST RPG - by RBSC")
        self.root.geometry("1000x700")
        self.root.configure(bg=COLORS['bg'])
        
        # Sistemas del juego
        self.story_generator = StoryGenerator()
        self.ranking_system = RankingSystem()
        self.ai_players = []
        
        # Variables de juego
        self.player_name = tk.StringVar()
        self.selected_character = None
        self.current_story = None
        self.current_stage = 0
        self.start_time = None
        self.player_progress = 0
        self.player_errors = 0
        self.game_active = False
        
        # Configurar fuentes
        self.setup_fonts()
        
        # Inicializar sistema de pantallas
        self.screens = GameScreens(self)
        
        # Iniciar con pantalla principal
        self.screens.show_main_menu()
    
    def setup_fonts(self):
        """Configura las fuentes del juego"""
        self.title_font = tkfont.Font(family="Courier New", size=24, weight="bold")
        self.header_font = tkfont.Font(family="Courier New", size=16, weight="bold")
        self.normal_font = tkfont.Font(family="Courier New", size=11)
        self.small_font = tkfont.Font(family="Courier New", size=9)
    
    def clear_screen(self):
        """Limpia la pantalla actual"""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def get_elapsed_time(self) -> int:
        """Obtiene el tiempo transcurrido"""
        if self.start_time:
            return int(time.time() - self.start_time)
        return 0
    
    # ========================================================================
    # LÓGICA DEL JUEGO
    # ========================================================================
    
    def start_game(self):
        """Inicia una nueva partida"""
        self.game_active = True
        self.start_time = time.time()
        self.player_progress = 0
        self.player_errors = 0
        self.current_stage = 0
        
        # Generar historia
        self.current_story = self.story_generator.generate_new_story(self.selected_character)
        
        # Crear IA para otros personajes
        self.ai_players = []
        characters = ['usuario', 'hacker', 'cyberdelincuente']
        difficulties = {'usuario': 'facil', 'hacker': 'medio', 'cyberdelincuente': 'dificil'}
        
        for char in characters:
            if char != self.selected_character:
                ai = AIPlayer(char, difficulties[char])
                self.ai_players.append(ai)
        
        self.screens.show_game_screen()
    
    def process_player_action(self, option: dict):
        """Procesa la acción del jugador"""
        if not self.game_active:
            return
        
        # Determinar éxito
        success = random.randint(1, 100) <= option['success']
        
        if success:
            progress_gain = random.randint(15, 25)
            self.player_progress += progress_gain
            result_text = "✅ ¡Acción exitosa!"
            result_color = COLORS['accent']
        else:
            progress_gain = random.randint(5, 10)
            self.player_progress += progress_gain
            self.player_errors += 1
            result_text = "❌ Algo salió mal..."
            result_color = COLORS['secondary']
        
        # Limitar progreso
        self.player_progress = min(100, self.player_progress)
        
        # Mostrar resultado
        self.screens.show_action_result(result_text, result_color, option, success)
        
        # Actualizar IA
        self.update_ai_progress()
        
        # Verificar victoria
        if self.player_progress >= 100:
            self.end_game(completed=True)
            return
        
        # Verificar si alguna IA ganó
        for ai in self.ai_players:
            if ai.completed:
                self.end_game(completed=False, winner=ai.character_type)
                return
        
        # Avanzar a siguiente etapa
        self.current_stage += 1
    
    def update_ai_progress(self):
        """Actualiza el progreso de los jugadores IA"""
        for ai in self.ai_players:
            if ai.completed:
                continue
            
            # La IA toma una decisión
            if self.current_stage < len(self.current_story['stages']):
                stage = self.current_story['stages'][self.current_stage]
                decision = ai.make_decision(stage['options'])
                
                # Procesar decisión de IA
                success = random.randint(1, 100) <= decision['success']
                ai.update_progress(success, decision['time'])
    
    def end_game(self, completed: bool, winner: str = None):
        """Finaliza el juego"""
        self.game_active = False
        elapsed_time = self.get_elapsed_time()
        
        # Guardar puntuación
        self.ranking_system.add_score(
            self.player_name.get(),
            self.selected_character,
            elapsed_time,
            self.player_errors,
            completed
        )
        
        # Mostrar pantalla de resultados
        self.screens.show_results_screen(completed, elapsed_time, winner)# game/game_manager.py (versión mejorada)
import tkinter as tk
from tkinter import font as tkfont
import time
import random

from config.colors import COLORS
from models.story import StoryGenerator
from ai.ai_player import AIPlayer
from utils.ranking_system import RankingSystem
from ui.screens import GameScreens
from utils.dialog_engine import DialogEngine
from utils.effects_system import EffectsSystem
from utils.customization_system import CustomizationSystem

class CyberQuestGame:
    """Clase principal del juego - Versión Mejorada"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("CYBER QUEST RPG - by RBSC")
        self.root.geometry("1200x800")  # Ventana más grande
        self.root.configure(bg=COLORS['bg'])
        
        # Sistemas del juego mejorados
        self.story_generator = StoryGenerator()
        self.ranking_system = RankingSystem()
        self.dialog_engine = DialogEngine()
        self.effects_system = EffectsSystem()
        self.customization_system = CustomizationSystem()
        self.ai_players = []
        
        # Variables de juego expandidas
        self.player_name = tk.StringVar()
        self.selected_character = None
        self.current_story = None
        self.current_stage = 0
        self.start_time = None
        self.player_progress = 0
        self.player_errors = 0
        self.game_active = False
        self.player_customization = {}
        self.active_effects = []
        
        # Configurar fuentes mejoradas
        self.setup_fonts()
        
        # Inicializar sistema de pantallas
        self.screens = GameScreens(self)
        
        # Iniciar con pantalla principal mejorada
        self.screens.show_enhanced_main_menu()
    
    def setup_fonts(self):
        """Configura las fuentes del juego mejoradas"""
        self.title_font = tkfont.Font(family="Courier New", size=28, weight="bold")
        self.header_font = tkfont.Font(family="Courier New", size=18, weight="bold")
        self.normal_font = tkfont.Font(family="Courier New", size=12)
        self.small_font = tkfont.Font(family="Courier New", size=10)
        self.dialog_font = tkfont.Font(family="Arial", size=11, slant="italic")
    
    def apply_game_effect(self, effect_type: str, source: str = "system"):
        """Aplica un efecto de juego"""
        self.active_effects.append({
            'type': effect_type,
            'source': source,
            'applied_at': self.get_elapsed_time()
        })
        
        # Aplicar consecuencias basadas en el efecto
        consequences = {
            'virus': lambda: self._reduce_player_speed(),
            'firewall_blocked': lambda: self._block_next_action(),
            'data_breach': lambda: self._expose_player_info(),
            'system_override': lambda: self._boost_abilities(),
            'encryption': lambda: self._strengthen_defenses()
        }
        
        if effect_type in consequences:
            consequences[effect_type]()
    
    def _reduce_player_speed(self):
        """Reduce la velocidad del jugador por virus"""
        self.player_progress -= 5  # Penalización
        
    def process_player_action(self, option: dict):
        """Procesa la acción del jugador - Versión Mejorada"""
        if not self.game_active:
            return
        
        # Modificadores por personalización
        success_modifier = self._calculate_success_modifier()
        final_success = min(95, option['success'] + success_modifier)
        
        # Determinar éxito
        success = random.randint(1, 100) <= final_success
        
        # Efectos especiales basados en riesgo
        if option['risk'] == 'alto' and success:
            # Recompensa mayor por alto riesgo
            progress_gain = random.randint(20, 30)
            special_effect = random.choice(['system_override', 'encryption'])
            self.apply_game_effect(special_effect, "high_risk_success")
        elif option['risk'] == 'alto' and not success:
            # Penalización mayor por fallo de alto riesgo
            progress_gain = random.randint(3, 8)
            self.apply_game_effect('virus', "high_risk_failure")
        else:
            progress_gain = random.randint(10, 20) if success else random.randint(5, 10)
        
        if success:
            self.player_progress += progress_gain
            result_text = "✅ ¡Acción exitosa!"
            result_color = COLORS['accent']
        else:
            self.player_progress += progress_gain
            self.player_errors += 1
            result_text = "❌ Algo salió mal..."
            result_color = COLORS['secondary']
        
        # Aplicar efectos activos
        self._process_active_effects()
        
        # Limitar progreso
        self.player_progress = max(0, min(100, self.player_progress))
        
        # Generar diálogo contextual
        situation = "acción exitosa" if success else "contratiempo"
        dialog = self.dialog_engine.generate_character_dialog(
            self.selected_character, 
            situation,
            "victory" if success else "stressed"
        )
        
        # Mostrar resultado mejorado
        self.screens.show_enhanced_action_result(result_text, result_color, option, success, dialog)
        
        # Actualizar IA con interconexión
        self.update_ai_progress()
        
        # Verificar condiciones de fin de juego
        self._check_game_end_conditions()
        
        # Avanzar a siguiente etapa
        self.current_stage += 1
    
    def _calculate_success_modifier(self) -> int:
        """Calcula modificadores de éxito basados en personalización"""
        modifier = 0
        customization = self.player_customization
        
        for accessory in customization.get('accessories', []):
            if accessory.get('effect') == 'increase_success':
                modifier += 5
            elif accessory.get('effect') == 'reduce_errors':
                modifier += 3
        
        return modifier
    
    def _check_game_end_conditions(self):
        """Verifica todas las condiciones de fin de juego"""
        if self.player_progress >= 100:
            self.end_game(completed=True)
            return
        
        for ai in self.ai_players:
            if ai.completed:
                self.end_game(completed=False, winner=ai.character_type)
                return
        
        # Nueva condición: demasiados errores
        if self.player_errors >= 10:
            self.end_game(completed=False, winner="system_failure")
            return