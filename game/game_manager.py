# game/game_manager.py - VERSION MEJORADA
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
    """Clase principal del juego - Versión Mejorada con Interconexión"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("⚡ CYBER QUEST RPG - by RBSC")
        self.root.geometry("1400x900")
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
        self.turn_count = 0
        
        # Sistema de interconexión entre jugadores
        self.global_events = []
        self.character_states = {
            'usuario': {'health': 100, 'detection': 0, 'resources': 50},
            'hacker': {'health': 100, 'detection': 0, 'resources': 50},
            'cyberdelincuente': {'health': 100, 'detection': 0, 'resources': 50}
        }
        
        # Configurar fuentes
        self.setup_fonts()
        
        # Inicializar sistema de pantallas
        self.screens = GameScreens(self)
        
        # Iniciar con pantalla principal
        self.screens.show_main_menu()
    
    def setup_fonts(self):
        """Configura las fuentes del juego"""
        try:
            self.title_font = tkfont.Font(family="Courier New", size=32, weight="bold")
            self.header_font = tkfont.Font(family="Courier New", size=20, weight="bold")
            self.normal_font = tkfont.Font(family="Courier New", size=13)
            self.small_font = tkfont.Font(family="Courier New", size=11)
            self.tiny_font = tkfont.Font(family="Courier New", size=9)
        except:
            self.title_font = tkfont.Font(size=32, weight="bold")
            self.header_font = tkfont.Font(size=20, weight="bold")
            self.normal_font = tkfont.Font(size=13)
            self.small_font = tkfont.Font(size=11)
            self.tiny_font = tkfont.Font(size=9)
    
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
        self.turn_count = 0
        self.global_events = []
        
        # Reiniciar estados de personajes
        for char in self.character_states:
            self.character_states[char] = {'health': 100, 'detection': 0, 'resources': 50}
        
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
    
    # game/game_manager.py - CORRECCIÓN PARA AVANCE DE ETAPAS
    def process_player_action(self, option: dict):
        """Procesa la acción del jugador con sistema de interconexión"""
        if not self.game_active:
            return
        
        self.turn_count += 1
        
        # Determinar éxito base
        success_chance = option['success']
        
        # Modificar éxito según efectos activos
        for effect in self.active_effects:
            if effect['type'] == 'virus':
                success_chance -= 15
            elif effect['type'] == 'firewall_blocked':
                success_chance -= 25
            elif effect['type'] == 'system_override':
                success_chance += 20
        
        success = random.randint(1, 100) <= max(10, min(95, success_chance))
        
        # Calcular ganancia de progreso
        if success:
            progress_gain = random.randint(18, 28)
            self.player_progress += progress_gain
            result_text = "✅ ¡Acción exitosa!"
            result_color = COLORS['accent']
            emotion = "victory"
        else:
            progress_gain = random.randint(3, 8)
            self.player_progress += progress_gain
            self.player_errors += 1
            result_text = "❌ Algo salió mal..."
            result_color = COLORS['secondary']
            emotion = "stressed"
        
        # Limitar progreso
        self.player_progress = min(100, self.player_progress)
        
        # Actualizar estado del personaje
        self.update_character_state(self.selected_character, success, option)
        
        # Generar efectos según el riesgo y resultado
        self.apply_action_effects(option, success)
        
        # Generar diálogo contextual con Gemini
        situation = f"acción {option['text']} - resultado: {'éxito' if success else 'fallo'}"
        dialog = self.dialog_engine.generate_character_dialog(
            self.selected_character, 
            situation,
            emotion
        )
        
        # Crear evento global que afecta a otros jugadores
        self.create_global_event(option, success)
        
        # Mostrar resultado
        self.screens.show_action_result(result_text, result_color, option, success, dialog)
        
        # Actualizar IA y procesar sus acciones
        self.update_ai_progress()
        
        # Verificar victoria del jugador
        if self.player_progress >= 100:
            self.end_game(completed=True)
            return
        
        # Verificar si alguna IA ganó
        for ai in self.ai_players:
            if ai.completed:
                self.end_game(completed=False, winner=ai.character_type)
                return
        
        # Verificar game over por efectos negativos
        player_state = self.character_states[self.selected_character]
        if player_state['health'] <= 0:
            self.end_game(completed=False, winner="system_failure")
            return
        
        if player_state['detection'] >= 100:
            self.end_game(completed=False, winner="detected")
            return
        
        # CORRECCIÓN: Solo avanzar etapa si no hemos completado el juego
        # y si aún hay etapas disponibles
        if self.current_stage < len(self.current_story['stages']) - 1:
            self.current_stage += 1
        else:
            # Si estamos en la última etapa y no hemos ganado, forzar fin del juego
            if self.player_progress < 100:
                # El jugador no completó en las etapas disponibles
                self.end_game(completed=False, winner="time_out")
    
    def update_character_state(self, character: str, success: bool, option: dict):
        """Actualiza el estado del personaje basado en la acción"""
        state = self.character_states[character]
        
        # Modificar según resultado
        if success:
            state['resources'] += random.randint(5, 15)
            state['detection'] -= random.randint(5, 10)
        else:
            state['resources'] -= random.randint(5, 10)
            state['detection'] += random.randint(10, 20)
        
        # Modificar según riesgo
        if option['risk'] == 'alto':
            state['detection'] += random.randint(15, 25)
            if not success:
                state['health'] -= random.randint(10, 20)
        elif option['risk'] == 'medio':
            state['detection'] += random.randint(5, 15)
            if not success:
                state['health'] -= random.randint(5, 10)
        
        # Limitar valores
        state['health'] = max(0, min(100, state['health']))
        state['detection'] = max(0, min(100, state['detection']))
        state['resources'] = max(0, min(100, state['resources']))
    
    def apply_action_effects(self, option: dict, success: bool):
        """Aplica efectos según la acción realizada"""
        # Limpiar efectos expirados
        self.active_effects = [e for e in self.active_effects if e['duration'] > 0]
        
        # Reducir duración de efectos activos
        for effect in self.active_effects:
            effect['duration'] -= 1
        
        # Aplicar nuevos efectos basados en riesgo y resultado
        if not success:
            if option['risk'] == 'alto':
                if random.random() < 0.4:
                    self.active_effects.append({
                        'type': 'virus',
                        'duration': 2,
                        'description': '🦠 INFECTADO - Éxito reducido'
                    })
            elif option['risk'] == 'medio':
                if random.random() < 0.3:
                    self.active_effects.append({
                        'type': 'firewall_blocked',
                        'duration': 1,
                        'description': '🛡️ BLOQUEADO - Próxima acción penalizada'
                    })
        else:
            # Efectos positivos por éxito
            if option['risk'] == 'alto' and random.random() < 0.2:
                self.active_effects.append({
                    'type': 'system_override',
                    'duration': 2,
                    'description': '⚡ POTENCIADO - Éxito aumentado'
                })
    
    def create_global_event(self, option: dict, success: bool):
        """Crea eventos globales que afectan a todos los jugadores"""
        event_chance = 0.3 if success else 0.5
        
        if random.random() < event_chance:
            events = [
                {
                    'type': 'security_alert',
                    'description': '🚨 ALERTA DE SEGURIDAD GLOBAL',
                    'effect': 'Todos los jugadores: +20% detección'
                },
                {
                    'type': 'system_vulnerability',
                    'description': '🔓 VULNERABILIDAD DESCUBIERTA',
                    'effect': 'Todos los jugadores: +10% éxito próxima acción'
                },
                {
                    'type': 'data_corruption',
                    'description': '💾 CORRUPCIÓN DE DATOS',
                    'effect': 'Todos los jugadores: -10 recursos'
                },
                {
                    'type': 'network_boost',
                    'description': '📡 MEJORA DE RED',
                    'effect': 'Todos los jugadores: -15% detección'
                }
            ]
            
            event = random.choice(events)
            self.global_events.append(event)
            
            # Aplicar efectos a todos los personajes
            for char in self.character_states:
                if event['type'] == 'security_alert':
                    self.character_states[char]['detection'] += 20
                elif event['type'] == 'system_vulnerability':
                    pass  # Se maneja en process_player_action
                elif event['type'] == 'data_corruption':
                    self.character_states[char]['resources'] -= 10
                elif event['type'] == 'network_boost':
                    self.character_states[char]['detection'] -= 15
    
    def update_ai_progress(self):
        """Actualiza el progreso de los jugadores IA con interconexión"""
        for ai in self.ai_players:
            if ai.completed:
                continue
            
            if self.current_stage < len(self.current_story['stages']):
                stage = self.current_story['stages'][self.current_stage]
                decision = ai.make_decision(stage['options'])
                
                # Procesar decisión de IA considerando estado global
                ai_state = self.character_states[ai.character_type]
                success_mod = 0
                
                # Modificar según estado
                if ai_state['detection'] > 70:
                    success_mod -= 20
                if ai_state['resources'] < 20:
                    success_mod -= 15
                
                success = random.randint(1, 100) <= (decision['success'] + success_mod)
                ai.update_progress(success, decision['time'])
                
                # Actualizar estado de la IA
                self.update_character_state(ai.character_type, success, decision)
    
    def end_game(self, completed: bool, winner: str = None):
        """Finaliza el juego"""
        self.game_active = False
        elapsed_time = self.get_elapsed_time()
        
        # Guardar puntuación CORREGIDO
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