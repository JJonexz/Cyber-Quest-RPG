# game/game_manager.py
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
    """Clase principal del juego - Versión Corregida"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("⚡ CYBER QUEST RPG - by RBSC")
        self.root.geometry("1200x800")
        self.root.configure(bg=COLORS['bg'])
        self.root.resizable(True, True)
        
        # Sistemas del juego
        self.story_generator = StoryGenerator()
        self.ranking_system = RankingSystem()
        self.dialog_engine = DialogEngine()
        self.effects_system = EffectsSystem()
        self.customization_system = CustomizationSystem()
        self.ai_players = []
        
        # Variables de juego
        self.player_name = tk.StringVar(value="Jugador")
        self.selected_character = None
        self.current_story = None
        self.current_stage = 0
        self.start_time = None
        self.player_progress = 0
        self.player_errors = 0
        self.game_active = False
        self.player_customization = {}
        self.active_effects = []
        
        # Configurar fuentes
        self.setup_fonts()
        
        # Inicializar sistema de pantallas - CORREGIDO: pasar self como argumento
        self.screens = GameScreens(self)
        
        # Iniciar con pantalla principal
        self.screens.show_main_menu()
    
    def setup_fonts(self):
        """Configura las fuentes del juego"""
        try:
            self.title_font = tkfont.Font(family="Courier New", size=28, weight="bold")
            self.header_font = tkfont.Font(family="Courier New", size=18, weight="bold")
            self.normal_font = tkfont.Font(family="Courier New", size=12)
            self.small_font = tkfont.Font(family="Courier New", size=10)
        except:
            # Fallback
            self.title_font = tkfont.Font(size=28, weight="bold")
            self.header_font = tkfont.Font(size=18, weight="bold")
            self.normal_font = tkfont.Font(size=12)
            self.small_font = tkfont.Font(size=10)
    
    def clear_screen(self):
        """Limpia la pantalla actual"""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def get_elapsed_time(self) -> int:
        """Obtiene el tiempo transcurrido"""
        if self.start_time:
            return int(time.time() - self.start_time)
        return 0
    
    def start_game(self):
        """Inicia una nueva partida"""
        self.game_active = True
        self.start_time = time.time()
        self.player_progress = 0
        self.player_errors = 0
        self.current_stage = 0
        self.active_effects = []
        
        # Cargar personalización
        if self.player_name.get().strip():
            self.player_customization = self.customization_system.get_customization(
                self.player_name.get(), 
                self.selected_character
            )
        
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
        
        # Generar diálogo
        situation = "acción exitosa" if success else "contratiempo"
        dialog = self.dialog_engine.generate_character_dialog(
            self.selected_character, 
            situation,
            "victory" if success else "stressed"
        )
        
        # Mostrar resultado
        self.screens.show_action_result(result_text, result_color, option, success, dialog)
        
        # Actualizar IA
        self.update_ai_progress()
        
        # Verificar victoria
        if self.player_progress >= 100:
            self.end_game(completed=True)
            return
        
        # Verificar si alguna IA ganó
        for ai in self.game.ai_players:
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
        if self.player_name.get().strip():
            self.ranking_system.add_score(
                self.player_name.get(),
                self.selected_character,
                elapsed_time,
                self.player_errors,
                completed
            )
        
        # Mostrar pantalla de resultados
        self.screens.show_results_screen(completed, elapsed_time, winner)