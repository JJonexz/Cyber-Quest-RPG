# game/game_manager.py - VERSIÓN CORREGIDA Y MEJORADA
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
    """Clase principal del juego - Versión Mejorada y Corregida"""
    
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
        # Flag usado por modales para indicar que el usuario pidió volver al menú
        self._user_requested_menu = False
        
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
        
        print(f"🎮 Iniciando juego con personaje: {self.selected_character}")
        print(f"📖 Historia generada: {self.current_story['scenario']['name']}")
        print(f"🎯 Objetivo: {self.current_story['objective']}")
        
        self.screens.show_game_screen()
    
    def process_player_action(self, option: dict):
        """Procesa la acción del jugador con sistema de interconexión - CORREGIDO"""
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
        
        # Mostrar resultado (bloqueante: show_action_result ahora espera hasta que el modal se cierre)
        self.screens.show_action_result(result_text, result_color, option, success, dialog)

        # Si el usuario desde el modal pidió volver al menú, hacerlo y abortar la secuencia
        if getattr(self, '_user_requested_menu', False):
            # limpiar flag y volver al menú
            self._user_requested_menu = False
            self.screens.show_main_menu()
            return
        
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
        
        # CORRECCIÓN MEJORADA: Avanzar etapa solo si no hemos completado
        if self.player_progress < 100:
            if self.current_stage < len(self.current_story['stages']) - 1:
                self.current_stage += 1
            else:
                # Si estamos en la última etapa y no hemos ganado, forzar fin del juego
                self.end_game(completed=False, winner="time_out")

        # Refrescar la pantalla de juego si la partida sigue activa
        if self.game_active:
            self.screens.show_game_screen()
    
    def update_character_state(self, character: str, success: bool, option: dict):
        """Actualiza el estado del personaje basado en la acción - MEJORADO"""
        state = self.character_states[character]
        
        # Modificar según resultado
        if success:
            state['resources'] = min(100, state['resources'] + random.randint(5, 15))
            state['detection'] = max(0, state['detection'] - random.randint(5, 10))
        else:
            state['resources'] = max(0, state['resources'] - random.randint(5, 10))
            state['detection'] = min(100, state['detection'] + random.randint(10, 20))
        
        # Modificar según riesgo
        if option['risk'] == 'alto':
            state['detection'] = min(100, state['detection'] + random.randint(15, 25))
            if not success:
                state['health'] = max(0, state['health'] - random.randint(10, 20))
        elif option['risk'] == 'medio':
            state['detection'] = min(100, state['detection'] + random.randint(5, 15))
            if not success:
                state['health'] = max(0, state['health'] - random.randint(5, 10))
        
        # Efectos de accesorios
        if character == self.selected_character and self.player_customization:
            accessories = self.player_customization.get('accessories', [])
            if 'shield' in accessories and not success:
                state['health'] += 5  # Reducción de daño
            if 'analyzer' in accessories and success:
                state['resources'] += 5  # Bonus de recursos
    
    def apply_action_effects(self, option: dict, success: bool):
        """Aplica efectos según la acción realizada - MEJORADO"""
        # Limpiar efectos expirados
        self.active_effects = [e for e in self.active_effects if e['duration'] > 0]
        
        # Reducir duración de efectos activos
        for effect in self.active_effects:
            effect['duration'] -= 1
        
        # Aplicar nuevos efectos basados en riesgo y resultado
        effect_chance = random.random()
        
        if not success:
            if option['risk'] == 'alto' and effect_chance < 0.4:
                self.active_effects.append({
                    'type': 'virus',
                    'duration': 2,
                    'description': '🦠 INFECTADO - Éxito reducido 15%'
                })
            elif option['risk'] == 'medio' and effect_chance < 0.3:
                self.active_effects.append({
                    'type': 'firewall_blocked',
                    'duration': 1,
                    'description': '🛡️ BLOQUEADO - Próxima acción penalizada 25%'
                })
        else:
            # Efectos positivos por éxito
            if option['risk'] == 'alto' and effect_chance < 0.2:
                self.active_effects.append({
                    'type': 'system_override',
                    'duration': 2,
                    'description': '⚡ POTENCIADO - Éxito aumentado 20%'
                })
            elif option['risk'] == 'medio' and effect_chance < 0.15:
                self.active_effects.append({
                    'type': 'encryption',
                    'duration': 2,
                    'description': '🔒 ENCRIPTADO - Detección reducida'
                })
    
    def create_global_event(self, option: dict, success: bool):
        """Crea eventos globales que afectan a todos los jugadores - MEJORADO"""
        event_chance = 0.3 if success else 0.5
        
        if random.random() < event_chance:
            events = [
                {
                    'type': 'security_alert',
                    'description': self.dialog_engine.generate_event_description('security_alert'),
                    'effect': 'Todos los jugadores: +20% detección'
                },
                {
                    'type': 'system_vulnerability',
                    'description': self.dialog_engine.generate_event_description('system_vulnerability'),
                    'effect': 'Todos los jugadores: +10% éxito próxima acción'
                },
                {
                    'type': 'data_corruption',
                    'description': self.dialog_engine.generate_event_description('data_corruption'),
                    'effect': 'Todos los jugadores: -10 recursos'
                },
                {
                    'type': 'network_boost',
                    'description': self.dialog_engine.generate_event_description('network_boost'),
                    'effect': 'Todos los jugadores: -15% detección'
                }
            ]
            
            event = random.choice(events)
            self.global_events.append(event)
            
            # Aplicar efectos a todos los personajes
            for char in self.character_states:
                state = self.character_states[char]
                if event['type'] == 'security_alert':
                    state['detection'] = min(100, state['detection'] + 20)
                elif event['type'] == 'data_corruption':
                    state['resources'] = max(0, state['resources'] - 10)
                elif event['type'] == 'network_boost':
                    state['detection'] = max(0, state['detection'] - 15)
    
    def update_ai_progress(self):
        """Actualiza el progreso de los jugadores IA con interconexión - MEJORADO"""
        for ai in self.ai_players:
            if ai.completed:
                continue
            
            # La IA toma decisiones considerando el estado actual
            if self.current_stage < len(self.current_story['stages']):
                stage = self.current_story['stages'][self.current_stage]
                decision = ai.make_decision(stage['options'], self.character_states[ai.character_type])
                
                # Procesar decisión de IA
                ai_state = self.character_states[ai.character_type]
                success_mod = 0
                
                # Modificar según estado actual
                if ai_state['detection'] > 70:
                    success_mod -= 20
                elif ai_state['detection'] > 40:
                    success_mod -= 10
                
                if ai_state['resources'] < 20:
                    success_mod -= 15
                elif ai_state['resources'] > 80:
                    success_mod += 10
                
                if ai_state['health'] < 30:
                    success_mod -= 10
                
                success = random.randint(1, 100) <= max(10, min(95, decision['success'] + success_mod))
                
                # Actualizar progreso de IA
                if success:
                    ai.progress += random.randint(15, 25)
                else:
                    ai.errors += 1
                    ai.progress += random.randint(5, 10)
                
                ai.progress = min(100, ai.progress)
                
                if ai.progress >= 100:
                    ai.completed = True
                    print(f"🏆 IA {ai.character_type} completó el objetivo!")
                
                # Actualizar estado de la IA
                self.update_character_state(ai.character_type, success, decision)
    
    def end_game(self, completed: bool, winner: str = None):
        """Finaliza el juego - MEJORADO"""
        self.game_active = False
        elapsed_time = self.get_elapsed_time()
        
        # Generar diálogo final
        stats = {
            'progress': self.player_progress,
            'errors': self.player_errors,
            'time': elapsed_time
        }
        final_dialog = self.dialog_engine.generate_ending_dialog(
            self.selected_character, completed, stats
        )
        
        print(f"🎯 Juego terminado - Completado: {completed}, Ganador: {winner}")
        print(f"📊 Estadísticas - Tiempo: {elapsed_time}s, Errores: {self.player_errors}, Progreso: {self.player_progress}%")
        print(f"💬 Diálogo final: {final_dialog}")
        
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