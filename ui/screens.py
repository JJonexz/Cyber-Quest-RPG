# ============================================================================
# ARCHIVO: ui/screens.py
# DESCRIPCIÓN: Todas las pantallas de la interfaz de usuario. Incluye menú
#              principal, selección de personaje, gameplay, resultados y ranking.
# ============================================================================

import tkinter as tk
from tkinter import messagebox
import random
from config.colors import COLORS
from models.character import CharacterDatabase

class GameScreens:
    """Clase que contiene todas las pantallas del juego"""
    
    def __init__(self, game_manager):
        self.game = game_manager
    
    # ========================================================================
    # PANTALLA PRINCIPAL
    # ========================================================================
    
    def show_main_menu(self):
        """Muestra el menú principal"""
        self.game.clear_screen()
        
        # Frame principal
        main_frame = tk.Frame(self.game.root, bg=COLORS['bg'])
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Título
        title_label = tk.Label(
            main_frame,
            text="CYBER QUEST",
            font=self.game.title_font,
            bg=COLORS['bg'],
            fg=COLORS['accent']
        )
        title_label.pack(pady=20)
        
        subtitle_label = tk.Label(
            main_frame,
            text="Un juego de rol cyberpunk interactivo",
            font=self.game.normal_font,
            bg=COLORS['bg'],
            fg=COLORS['text']
        )
        subtitle_label.pack(pady=5)
        
        # Créditos
        credit_label = tk.Label(
            main_frame,
            text="Desarrollado por RBSC",
            font=self.game.small_font,
            bg=COLORS['bg'],
            fg=COLORS['text_secondary']
        )
        credit_label.pack(pady=5)
        
        # Botones del menú
        button_frame = tk.Frame(main_frame, bg=COLORS['bg'])
        button_frame.pack(pady=40)
        
        btn_new_game = tk.Button(
            button_frame,
            text="🎮 NUEVA PARTIDA",
            font=self.game.header_font,
            bg=COLORS['primary'],
            fg=COLORS['text_secondary'],
            activebackground=COLORS['accent'],
            command=self.show_character_selection,
            width=20,
            height=2,
            cursor='hand2'
        )
        btn_new_game.pack(pady=10)
        
        btn_ranking = tk.Button(
            button_frame,
            text="🏆 RANKING",
            font=self.game.header_font,
            bg=COLORS['container_bg2'],
            fg=COLORS['text_secondary'],
            activebackground=COLORS['accent'],
            command=self.show_ranking,
            width=20,
            height=2,
            cursor='hand2'
        )
        btn_ranking.pack(pady=10)
        
        btn_help = tk.Button(
            button_frame,
            text="❓ CÓMO JUGAR",
            font=self.game.header_font,
            bg=COLORS['container_bg2'],
            fg=COLORS['text_secondary'],
            activebackground=COLORS['accent'],
            command=self.show_help,
            width=20,
            height=2,
            cursor='hand2'
        )
        btn_help.pack(pady=10)
        
        btn_exit = tk.Button(
            button_frame,
            text="❌ SALIR",
            font=self.game.header_font,
            bg=COLORS['secondary'],
            fg=COLORS['text_secondary'],
            activebackground='#c0392b',
            command=self.game.root.quit,
            width=20,
            height=2,
            cursor='hand2'
        )
        btn_exit.pack(pady=10)
    
    # ========================================================================
    # SELECCIÓN DE PERSONAJE
    # ========================================================================
    
    def show_character_selection(self):
        """Pantalla de selección de personaje"""
        self.game.clear_screen()
        
        main_frame = tk.Frame(self.game.root, bg=COLORS['bg'])
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Título
        title = tk.Label(
            main_frame,
            text="SELECCIONA TU PERSONAJE",
            font=self.game.title_font,
            bg=COLORS['bg'],
            fg=COLORS['accent']
        )
        title.pack(pady=20)
        
        # Entrada de nombre
        name_frame = tk.Frame(main_frame, bg=COLORS['bg'])
        name_frame.pack(pady=20)
        
        name_label = tk.Label(
            name_frame,
            text="Nombre del jugador:",
            font=self.game.normal_font,
            bg=COLORS['bg'],
            fg=COLORS['text']
        )
        name_label.pack(side='left', padx=10)
        
        name_entry = tk.Entry(
            name_frame,
            textvariable=self.game.player_name,
            font=self.game.normal_font,
            bg=COLORS['modal'],
            fg=COLORS['text'],
            insertbackground=COLORS['accent'],
            width=25
        )
        name_entry.pack(side='left', padx=10)
        
        # Frame de personajes
        characters_frame = tk.Frame(main_frame, bg=COLORS['bg'])
        characters_frame.pack(pady=20, expand=True, fill='both')
        
        characters = CharacterDatabase.get_all_characters()
        
        for i, char in enumerate(characters):
            char_frame = tk.Frame(
                characters_frame,
                bg=COLORS['modal'],
                highlightbackground=char['color'],
                highlightthickness=2
            )
            char_frame.grid(row=0, column=i, padx=15, pady=10, sticky='nsew')
            
            # Configurar grid
            characters_frame.grid_columnconfigure(i, weight=1)
            
            # Icono
            icon_label = tk.Label(
                char_frame,
                text=char['icon'],
                font=('Arial', 48),
                bg=COLORS['modal']
            )
            icon_label.pack(pady=10)
            
            # Nombre
            name_label = tk.Label(
                char_frame,
                text=char['name'],
                font=self.game.header_font,
                bg=COLORS['modal'],
                fg=char['color']
            )
            name_label.pack(pady=5)
            
            # Dificultad
            diff_label = tk.Label(
                char_frame,
                text=f"Dificultad: {char['difficulty']}",
                font=self.game.small_font,
                bg=COLORS['modal'],
                fg=COLORS['text']
            )
            diff_label.pack(pady=5)
            
            # Descripción
            desc_label = tk.Label(
                char_frame,
                text=char['description'],
                font=self.game.small_font,
                bg=COLORS['modal'],
                fg=COLORS['text'],
                wraplength=250,
                justify='center'
            )
            desc_label.pack(pady=10, padx=10)
            
            # Botón seleccionar
            select_btn = tk.Button(
                char_frame,
                text="SELECCIONAR",
                font=self.game.normal_font,
                bg=char['color'],
                fg='white',
                command=lambda c=char['type']: self.select_character(c),
                cursor='hand2'
            )
            select_btn.pack(pady=15)
        
        # Botón volver
        back_btn = tk.Button(
            main_frame,
            text="← VOLVER",
            font=self.game.normal_font,
            bg=COLORS['container_bg2'],
            fg=COLORS['text_secondary'],
            command=self.show_main_menu,
            cursor='hand2'
        )
        back_btn.pack(pady=20)
    
    def select_character(self, character_type: str):
        """Selecciona un personaje y comienza el juego"""
        if not self.game.player_name.get().strip():
            messagebox.showwarning("Nombre requerido", "Por favor ingresa tu nombre")
            return
        
        self.game.selected_character = character_type
        self.game.start_game()
    
    # ========================================================================
    # JUEGO PRINCIPAL
    # ========================================================================
    
    def show_game_screen(self):
        """Muestra la pantalla de juego"""
        self.game.clear_screen()
        
        if self.game.current_stage >= len(self.game.current_story['stages']):
            self.game.end_game(completed=True)
            return
        
        stage = self.game.current_story['stages'][self.game.current_stage]
        
        # Frame principal
        main_frame = tk.Frame(self.game.root, bg=COLORS['bg'])
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Barra de progreso superior
        progress_frame = tk.Frame(main_frame, bg=COLORS['header_bg'])
        progress_frame.pack(fill='x', pady=(0, 20))
        
        # Información del jugador
        info_text = f"👤 {self.game.player_name.get()} | 🎭 {self.game.selected_character.title()} | ⏱️ {self.game.get_elapsed_time()}s | ❌ Errores: {self.game.player_errors}"
        info_label = tk.Label(
            progress_frame,
            text=info_text,
            font=self.game.small_font,
            bg=COLORS['header_bg'],
            fg=COLORS['text']
        )
        info_label.pack(pady=10)
        
        # Barra de progreso visual
        progress_bar_frame = tk.Frame(progress_frame, bg=COLORS['bg'], height=30)
        progress_bar_frame.pack(fill='x', padx=20, pady=5)
        
        progress_bar = tk.Canvas(progress_bar_frame, height=20, bg=COLORS['modal'], highlightthickness=0)
        progress_bar.pack(fill='x')
        
        # Dibujar barra después de que se renderice
        self.game.root.update_idletasks()
        bar_width = progress_bar.winfo_width()
        if bar_width > 1:
            fill_width = int((self.game.player_progress / 100) * bar_width)
            progress_bar.create_rectangle(0, 0, fill_width, 20, fill=COLORS['accent'], outline='')
            progress_bar.create_text(
                bar_width // 2, 10,
                text=f"{self.game.player_progress}%",
                fill=COLORS['text'],
                font=self.game.small_font
            )
        
        # Área de historia
        story_frame = tk.Frame(main_frame, bg=COLORS['modal'])
        story_frame.pack(fill='both', expand=True, pady=10)
        
        # Etapa actual
        stage_label = tk.Label(
            story_frame,
            text=f"ETAPA {stage['stage']} - {stage['location']}",
            font=self.game.header_font,
            bg=COLORS['modal'],
            fg=COLORS['accent']
        )
        stage_label.pack(pady=15)
        
        # Descripción
        desc_label = tk.Label(
            story_frame,
            text=stage['description'],
            font=self.game.normal_font,
            bg=COLORS['modal'],
            fg=COLORS['text'],
            wraplength=900,
            justify='left'
        )
        desc_label.pack(pady=10, padx=30)
        
        # Objetivo
        obj_label = tk.Label(
            story_frame,
            text=f"🎯 Objetivo: {self.game.current_story['objective']}",
            font=self.game.normal_font,
            bg=COLORS['modal'],
            fg=COLORS['secondary'],
            wraplength=900
        )
        obj_label.pack(pady=10, padx=30)
        
        # Opciones
        options_label = tk.Label(
            story_frame,
            text="¿Qué harás?",
            font=self.game.header_font,
            bg=COLORS['modal'],
            fg=COLORS['text']
        )
        options_label.pack(pady=15)
        
        options_frame = tk.Frame(story_frame, bg=COLORS['modal'])
        options_frame.pack(pady=10, padx=40, fill='both', expand=True)
        
        for i, option in enumerate(stage['options']):
            opt_frame = tk.Frame(
                options_frame,
                bg=COLORS['bg'],
                highlightbackground=COLORS['accent'],
                highlightthickness=1
            )
            opt_frame.pack(fill='x', pady=8)
            
            # Información de la opción
            info_text = f"⏱️ {option['time']}min | 🎲 Éxito: {option['success']}% | ⚠️ Riesgo: {option['risk'].upper()}"
            
            opt_btn = tk.Button(
                opt_frame,
                text=f"{i+1}. {option['text']}\n{info_text}",
                font=self.game.normal_font,
                bg=COLORS['container_bg2'],
                fg=COLORS['text'],
                activebackground=COLORS['accent'],
                command=lambda o=option: self.game.process_player_action(o),
                cursor='hand2',
                justify='left',
                anchor='w',
                padx=20,
                pady=10
            )
            opt_btn.pack(fill='x')
        
        # Estado de la IA
        ai_frame = tk.Frame(main_frame, bg=COLORS['header_bg'])
        ai_frame.pack(fill='x', pady=(10, 0))
        
        ai_label = tk.Label(
            ai_frame,
            text="🤖 Competidores IA:",
            font=self.game.small_font,
            bg=COLORS['header_bg'],
            fg=COLORS['text']
        )
        ai_label.pack(pady=5)
        
        for ai in self.game.ai_players:
            ai_info = f"  • {ai.character_type.title()}: {ai.progress}% | Errores: {ai.errors}"
            ai_info_label = tk.Label(
                ai_frame,
                text=ai_info,
                font=self.game.small_font,
                bg=COLORS['header_bg'],
                fg=COLORS['text_secondary']
            )
            ai_info_label.pack()
    
    def show_action_result(self, result_text: str, result_color: str, option: dict, success: bool):
        """Muestra el resultado de una acción"""
        result_window = tk.Toplevel(self.game.root)
        result_window.title("Resultado")
        result_window.geometry("500x350")
        result_window.configure(bg=COLORS['modal'])
        result_window.transient(self.game.root)
        result_window.grab_set()
        
        # Centrar ventana
        result_window.update_idletasks()
        x = (result_window.winfo_screenwidth() // 2) - (result_window.winfo_width() // 2)
        y = (result_window.winfo_screenheight() // 2) - (result_window.winfo_height() // 2)
        result_window.geometry(f"+{x}+{y}")
        
        # Contenido
        title_label = tk.Label(
            result_window,
            text=result_text,
            font=self.game.header_font,
            bg=COLORS['modal'],
            fg=result_color
        )
        title_label.pack(pady=20)
        
        action_label = tk.Label(
            result_window,
            text=f"Acción: {option['text']}",
            font=self.game.normal_font,
            bg=COLORS['modal'],
            fg=COLORS['text'],
            wraplength=450
        )
        action_label.pack(pady=10)
        
        if success:
            consequence = random.choice([
                "Has avanzado significativamente en tu objetivo.",
                "Tu estrategia está funcionando perfectamente.",
                "Has ganado ventaja sobre tus competidores.",
                "El sistema no detectó tu presencia.",
                "Obtuviste información valiosa."
            ])
        else:
            consequence = random.choice([
                "El sistema detectó actividad sospechosa.",
                "Perdiste tiempo valioso.",
                "Tus competidores están ganando terreno.",
                "Necesitas replanear tu estrategia.",
                "El riesgo no valió la pena esta vez."
            ])
        
        consequence_label = tk.Label(
            result_window,
            text=consequence,
            font=self.game.normal_font,
            bg=COLORS['modal'],
            fg=COLORS['text'],
            wraplength=450
        )
        consequence_label.pack(pady=15)
        
        # Progreso ganado
        progress_label = tk.Label(
            result_window,
            text=f"Progreso actual: {self.game.player_progress}%",
            font=self.game.normal_font,
            bg=COLORS['modal'],
            fg=COLORS['accent']
        )
        progress_label.pack(pady=10)
        
        # Botón continuar
        continue_btn = tk.Button(
            result_window,
            text="CONTINUAR",
            font=self.game.normal_font,
            bg=COLORS['primary'],
            fg=COLORS['text_secondary'],
            command=lambda: [result_window.destroy(), self.show_game_screen()],
            cursor='hand2',
            width=15
        )
        continue_btn.pack(pady=20)
    
    # ========================================================================
    # PANTALLA DE RESULTADOS
    # ========================================================================
    
    def show_results_screen(self, completed: bool, elapsed_time: int, winner: str = None):
        """Muestra la pantalla de resultados"""
        self.game.clear_screen()
        
        main_frame = tk.Frame(self.game.root, bg=COLORS['bg'])
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        if completed:
            title_text = "🏆 ¡VICTORIA!"
            title_color = COLORS['accent']
            message = "¡Felicidades! Has completado tu objetivo exitosamente."
        else:
            title_text = "❌ DERROTA"
            title_color = COLORS['secondary']
            if winner:
                message = f"El {winner.title()} (IA) completó el objetivo primero."
            else:
                message = "No lograste completar el objetivo a tiempo."
        
        # Título
        title_label = tk.Label(
            main_frame,
            text=title_text,
            font=self.game.title_font,
            bg=COLORS['bg'],
            fg=title_color
        )
        title_label.pack(pady=20)
        
        # Mensaje
        message_label = tk.Label(
            main_frame,
            text=message,
            font=self.game.header_font,
            bg=COLORS['bg'],
            fg=COLORS['text']
        )
        message_label.pack(pady=10)
        
        # Estadísticas
        stats_frame = tk.Frame(main_frame, bg=COLORS['modal'])
        stats_frame.pack(pady=20, padx=100, fill='both')
        
        stats_title = tk.Label(
            stats_frame,
            text="📊 ESTADÍSTICAS",
            font=self.game.header_font,
            bg=COLORS['modal'],
            fg=COLORS['accent']
        )
        stats_title.pack(pady=15)
        
        stats = [
            f"👤 Jugador: {self.game.player_name.get()}",
            f"🎭 Personaje: {self.game.selected_character.title()}",
            f"⏱️ Tiempo total: {elapsed_time} segundos",
            f"❌ Errores cometidos: {self.game.player_errors}",
            f"📈 Progreso final: {self.game.player_progress}%",
            f"🎯 Etapas completadas: {self.game.current_stage}/{len(self.game.current_story['stages'])}"
        ]
        
        for stat in stats:
            stat_label = tk.Label(
                stats_frame,
                text=stat,
                font=self.game.normal_font,
                bg=COLORS['modal'],
                fg=COLORS['text']
            )
            stat_label.pack(pady=5)
        
        # Puntuación
        if completed:
            score = self.game.ranking_system._calculate_score(elapsed_time, self.game.player_errors, completed)
            score_label = tk.Label(
                stats_frame,
                text=f"⭐ Puntuación: {int(score)} puntos",
                font=self.game.header_font,
                bg=COLORS['modal'],
                fg=COLORS['accent']
            )
            score_label.pack(pady=15)
        
        # Botones
        button_frame = tk.Frame(main_frame, bg=COLORS['bg'])
        button_frame.pack(pady=20)
        
        btn_new_game = tk.Button(
            button_frame,
            text="🎮 NUEVA PARTIDA",
            font=self.game.normal_font,
            bg=COLORS['primary'],
            fg=COLORS['text_secondary'],
            command=self.show_character_selection,
            cursor='hand2',
            width=18
        )
        btn_new_game.pack(side='left', padx=10)
        
        btn_ranking = tk.Button(
            button_frame,
            text="🏆 VER RANKING",
            font=self.game.normal_font,
            bg=COLORS['container_bg2'],
            fg=COLORS['text_secondary'],
            command=self.show_ranking,
            cursor='hand2',
            width=18
        )
        btn_ranking.pack(side='left', padx=10)
        
        btn_menu = tk.Button(
            button_frame,
            text="🏠 MENÚ PRINCIPAL",
            font=self.game.normal_font,
            bg=COLORS['secondary'],
            fg=COLORS['text_secondary'],
            command=self.show_main_menu,
            cursor='hand2',
            width=18
        )
        btn_menu.pack(side='left', padx=10)
    
    # ========================================================================
    # PANTALLA DE RANKING
    # ========================================================================
    
    def show_ranking(self):
        """Muestra el ranking de jugadores"""
        self.game.clear_screen()
        
        main_frame = tk.Frame(self.game.root, bg=COLORS['bg'])
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Título
        title_label = tk.Label(
            main_frame,
            text="🏆 RANKING DE JUGADORES",
            font=self.game.title_font,
            bg=COLORS['bg'],
            fg=COLORS['accent']
        )
        title_label.pack(pady=20)
        
        # Tabla de ranking
        table_frame = tk.Frame(main_frame, bg=COLORS['modal'])
        table_frame.pack(pady=10, fill='both', expand=True)
        
        # Encabezados
        headers = ['Pos', 'Jugador', 'Personaje', 'Tiempo (s)', 'Errores', 'Puntuación', 'Fecha']
        header_frame = tk.Frame(table_frame, bg=COLORS['header_bg'])
        header_frame.pack(fill='x')
        
        for i, header in enumerate(headers):
            label = tk.Label(
                header_frame,
                text=header,
                font=self.game.small_font,
                bg=COLORS['header_bg'],
                fg=COLORS['text_secondary'],
                width=12 if i > 0 else 5
            )
            label.grid(row=0, column=i, padx=5, pady=10)
        
        # Datos del ranking
        rankings = self.game.ranking_system.get_top_rankings(10)
        
        if rankings:
            for idx, entry in enumerate(rankings):
                row_bg = COLORS['bg'] if idx % 2 == 0 else COLORS['container_bg2']
                
                data = [
                    f"#{idx + 1}",
                    entry['player'][:12],
                    entry['character'][:12],
                    str(entry['time']),
                    str(entry['errors']),
                    str(int(entry['score'])),
                    entry['date'].split()[0]
                ]
                
                for i, value in enumerate(data):
                    label = tk.Label(
                        table_frame,
                        text=value,
                        font=self.game.small_font,
                        bg=row_bg,
                        fg=COLORS['text'],
                        width=12 if i > 0 else 5
                    )
                    label.grid(row=idx + 1, column=i, padx=5, pady=5)
        else:
            no_data_label = tk.Label(
                table_frame,
                text="No hay partidas registradas aún",
                font=self.game.normal_font,
                bg=COLORS['modal'],
                fg=COLORS['text']
            )
            no_data_label.pack(pady=50)
        
        # Botón volver
        back_btn = tk.Button(
            main_frame,
            text="← VOLVER",
            font=self.game.normal_font,
            bg=COLORS['container_bg2'],
            fg=COLORS['text_secondary'],
            command=self.show_main_menu,
            cursor='hand2',
            width=15
        )
        back_btn.pack(pady=20)
    
    # ========================================================================
    # PANTALLA DE AYUDA
    # ========================================================================
    
    def show_help(self):
        """Muestra la pantalla de ayuda"""
        self.game.clear_screen()
        
        main_frame = tk.Frame(self.game.root, bg=COLORS['bg'])
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Título
        title_label = tk.Label(
            main_frame,
            text="❓ CÓMO JUGAR",
            font=self.game.title_font,
            bg=COLORS['bg'],
            fg=COLORS['accent']
        )
        title_label.pack(pady=20)
        
        # Frame de contenido con scroll
        canvas = tk.Canvas(main_frame, bg=COLORS['modal'], highlightthickness=0)
        scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=COLORS['modal'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        help_sections = [
            {
                'title': '🎮 OBJETIVO DEL JUEGO',
                'content': 'Completa tu objetivo antes que los competidores IA. Cada personaje tiene un objetivo único basado en su rol. Toma decisiones estratégicas para avanzar en la historia.'
            },
            {
                'title': '👥 PERSONAJES',
                'content': 'USUARIO (Fácil): Sobrevive y protege tu información.\nHACKER ÉTICO (Medio): Expón vulnerabilidades y protege sistemas.\nCYBERDELINCUENTE (Difícil): Opera en las sombras sin ser detectado.'
            },
            {
                'title': '🎲 MECÁNICAS',
                'content': 'Cada decisión tiene un porcentaje de éxito, tiempo requerido y nivel de riesgo. Las acciones exitosas otorgan más progreso. Los errores te penalizan en el ranking pero aún otorgan progreso mínimo.'
            },
            {
                'title': '🏆 RANKING',
                'content': 'Tu puntuación se calcula según: tiempo empleado, errores cometidos y si completaste el objetivo. Menos tiempo y menos errores = mejor puntuación.'
            },
            {
                'title': '🤖 IA COMPETIDORES',
                'content': 'Los personajes no seleccionados son controlados por IA. Compiten simultáneamente contigo. Si alguno completa su objetivo primero, pierdes la partida.'
            },
            {
                'title': '🎨 CARACTERÍSTICAS',
                'content': 'Historias generadas dinámicamente cada partida. Múltiples finales según tus decisiones. Sistema de progreso en tiempo real. Diseño retro minimalista.'
            }
        ]
        
        for section in help_sections:
            section_frame = tk.Frame(scrollable_frame, bg=COLORS['bg'])
            section_frame.pack(fill='x', pady=10, padx=20)
            
            title_label = tk.Label(
                section_frame,
                text=section['title'],
                font=self.game.normal_font,
                bg=COLORS['bg'],
                fg=COLORS['accent']
            )
            title_label.pack(anchor='w', pady=5)
            
            content_label = tk.Label(
                section_frame,
                text=section['content'],
                font=self.game.small_font,
                bg=COLORS['bg'],
                fg=COLORS['text'],
                wraplength=850,
                justify='left'
            )
            content_label.pack(anchor='w', padx=20)
        
        # Créditos
        credits_label = tk.Label(
            scrollable_frame,
            text="\n💻 Desarrollado por RBSC\nSoporte para música y efectos de sonido (opcional)",
            font=self.game.small_font,
            bg=COLORS['modal'],
            fg=COLORS['text_secondary']
        )
        credits_label.pack(pady=20)
        
        canvas.pack(side="left", fill="both", expand=True, padx=50)
        scrollbar.pack(side="right", fill="y")
        
        # Botón volver
        back_btn = tk.Button(
            main_frame,
            text="← VOLVER",
            font=self.game.normal_font,
            bg=COLORS['container_bg2'],
            fg=COLORS['text_secondary'],
            command=self.show_main_menu,
            cursor='hand2',
            width=15
        )
        back_btn.pack(pady=20)
        # ui/screens.py (secciones mejoradas)

class GameScreens:
    # ... código existente ...
    
    def show_enhanced_main_menu(self):
        """Menú principal mejorado y más atractivo"""
        self.game.clear_screen()
        
        # Frame principal con fondo mejorado
        main_frame = tk.Frame(self.game.root, bg=COLORS['bg'])
        main_frame.pack(expand=True, fill='both')
        
        # Efecto de título con glow
        title_container = tk.Frame(main_frame, bg=COLORS['bg'])
        title_container.pack(pady=40)
        
        title_label = tk.Label(
            title_container,
            text="⚡ CYBER QUEST ⚡",
            font=self.game.title_font,
            bg=COLORS['bg'],
            fg=COLORS['accent']
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            title_container,
            text="UNIVERSO CYBERPUNK INTERACTIVO",
            font=self.game.small_font,
            bg=COLORS['bg'],
            fg=COLORS['text_secondary']
        )
        subtitle_label.pack(pady=5)
        
        # Panel de personajes preview
        self._create_character_preview(main_frame)
        
        # Botones del menú con mejor diseño
        button_frame = tk.Frame(main_frame, bg=COLORS['bg'])
        button_frame.pack(pady=40)
        
        menu_buttons = [
            ("🎮 NUEVA AVENTURA", self.show_enhanced_character_selection, COLORS['primary']),
            ("✨ PERSONALIZAR", self.show_customization_screen, COLORS['accent']),
            ("🏆 HALL OF FAME", self.show_enhanced_ranking, '#f1c40f'),
            ("❓ GUÍA DEL SISTEMA", self.show_enhanced_help, COLORS['container_bg2']),
            ("🚪 SALIR DEL SISTEMA", self.game.root.quit, COLORS['secondary'])
        ]
        
        for text, command, color in menu_buttons:
            btn = tk.Button(
                button_frame,
                text=text,
                font=self.game.normal_font,
                bg=color,
                fg=COLORS['text_secondary'],
                activebackground=self._lighten_color(color),
                command=command,
                width=25,
                height=2,
                cursor='hand2',
                relief='raised',
                bd=2
            )
            btn.pack(pady=8)
    
    def _create_character_preview(self, parent):
        """Crea preview de personajes en el menú principal"""
        preview_frame = tk.Frame(parent, bg=COLORS['modal'], relief='ridge', bd=2)
        preview_frame.pack(pady=20, padx=100, fill='x')
        
        preview_label = tk.Label(
            preview_frame,
            text="👥 HÉROES DEL CIBERESPACIO",
            font=self.game.header_font,
            bg=COLORS['modal'],
            fg=COLORS['accent']
        )
        preview_label.pack(pady=10)
        
        chars_frame = tk.Frame(preview_frame, bg=COLORS['modal'])
        chars_frame.pack(pady=10, padx=20)
        
        characters = [
            {'icon': '👤', 'name': 'USUARIO', 'desc': 'Supervivencia digital'},
            {'icon': '💻', 'name': 'HACKER', 'desc': 'Justicia cibernética'},
            {'icon': '🎭', 'name': 'OPERATIVO', 'desc': 'Operaciones encubiertas'}
        ]
        
        for char in characters:
            char_frame = tk.Frame(chars_frame, bg=COLORS['container_bg2'], relief='sunken', bd=1)
            char_frame.pack(side='left', padx=15, pady=10)
            
            icon_label = tk.Label(
                char_frame,
                text=char['icon'],
                font=('Arial', 24),
                bg=COLORS['container_bg2']
            )
            icon_label.pack(pady=5)
            
            name_label = tk.Label(
                char_frame,
                text=char['name'],
                font=self.game.small_font,
                bg=COLORS['container_bg2'],
                fg=COLORS['text']
            )
            name_label.pack()
            
            desc_label = tk.Label(
                char_frame,
                text=char['desc'],
                font=('Arial', 8),
                bg=COLORS['container_bg2'],
                fg=COLORS['text_secondary']
            )
            desc_label.pack(pady=2)
    
    def show_character_display_panel(self, parent):
        """Panel de visualización de personajes en tiempo real"""
        display_frame = tk.Frame(parent, bg=COLORS['header_bg'], relief='groove', bd=2)
        display_frame.pack(fill='x', pady=10, padx=20)
        
        title_label = tk.Label(
            display_frame,
            text="🎯 ESTADO DE LOS AGENTES",
            font=self.game.small_font,
            bg=COLORS['header_bg'],
            fg=COLORS['accent']
        )
        title_label.pack(pady=8)
        
        # Mostrar jugador principal
        player_appearance = self.game.effects_system.get_character_appearance(
            self.game.selected_character, 
            self.game.active_effects
        )
        
        player_frame = tk.Frame(display_frame, bg=COLORS['container_bg2'])
        player_frame.pack(fill='x', padx=30, pady=5)
        
        player_icon = tk.Label(
            player_frame,
            text=player_appearance['icon'],
            font=('Arial', 20),
            bg=COLORS['container_bg2']
        )
        player_icon.pack(side='left', padx=10)
        
        player_info = tk.Label(
            player_frame,
            text=f"TÚ ({self.game.selected_character.title()}) - {self.game.player_progress}%",
            font=self.game.small_font,
            bg=COLORS['container_bg2'],
            fg=player_appearance['color']
        )
        player_info.pack(side='left', padx=10)
        
        # Mostrar IAs
        for ai in self.game.ai_players:
            ai_frame = tk.Frame(display_frame, bg=COLORS['modal'])
            ai_frame.pack(fill='x', padx=40, pady=2)
            
            ai_icon = tk.Label(
                ai_frame,
                text=ai.character_type[0].upper(),
                font=('Arial', 16),
                bg=COLORS['modal'],
                fg=ai.character_type_color
            )
            ai_icon.pack(side='left', padx=10)
            
            ai_info = tk.Label(
                ai_frame,
                text=f"{ai.character_type.title()} - {ai.progress}%",
                font=self.game.small_font,
                bg=COLORS['modal'],
                fg=COLORS['text_secondary']
            )
            ai_info.pack(side='left', padx=10)
            
            if ai.completed:
                status_label = tk.Label(
                    ai_frame,
                    text="✅ OBJETIVO CUMPLIDO",
                    font=('Arial', 8, 'bold'),
                    bg=COLORS['modal'],
                    fg=COLORS['secondary']
                )
                status_label.pack(side='right', padx=10)