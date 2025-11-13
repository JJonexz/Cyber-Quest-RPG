# ui/screens.py - VERSIÓN COMPLETA Y MEJORADA
import tkinter as tk
from tkinter import messagebox
import random
import time
from config.colors import COLORS
from models.character import CharacterDatabase

class GameScreens:
    """Clase que contiene todas las pantallas del juego - Versión Mejorada"""
    
    def __init__(self, game_manager):
        self.game = game_manager

    def _create_scrollable_container(self, parent, bg=None):
        """Crea un contenedor con scroll vertical reutilizable.

        Retorna el frame interno donde añadir widgets y el canvas (por si se necesita).
        """
        outer = tk.Frame(parent, bg=bg or parent['bg'])
        outer.pack(expand=True, fill='both')

        canvas = tk.Canvas(outer, bg=bg or parent['bg'], highlightthickness=0)
        vsb = tk.Scrollbar(outer, orient='vertical', command=canvas.yview)
        canvas.configure(yscrollcommand=vsb.set)

        vsb.pack(side='right', fill='y')
        canvas.pack(side='left', fill='both', expand=True)

        inner = tk.Frame(canvas, bg=bg or parent['bg'])
        canvas.create_window((0, 0), window=inner, anchor='nw')

        def _on_configure(event):
            canvas.configure(scrollregion=canvas.bbox('all'))

        def _on_canvas_configure(event):
            # Ajustar el ancho del frame interno al ancho del canvas
            canvas.itemconfig(1, width=event.width)

        inner.bind('<Configure>', _on_configure)
        canvas.bind('<Configure>', _on_canvas_configure)

        # Soporte para rueda del ratón
        def _on_mousewheel(event):
            # Windows uses event.delta, on Linux event.num/4/-4 sometimes; normalize
            delta = 0
            try:
                delta = -1 * int(event.delta / 120)
            except Exception:
                if event.num == 5:
                    delta = 1
                elif event.num == 4:
                    delta = -1
            canvas.yview_scroll(delta, 'units')

        # Windows and Mac
        canvas.bind_all('<MouseWheel>', _on_mousewheel)
        # Linux
        canvas.bind_all('<Button-4>', _on_mousewheel)
        canvas.bind_all('<Button-5>', _on_mousewheel)

        return inner, canvas
        
    def save_customization_and_start(self, accessories):
        """Guarda la personalización y comienza el juego"""
        try:
            customization = {
                'accessories': [acc['id'] for acc in accessories if acc],
                'timestamp': time.time()
            }
            
            self.game.customization_system.save_customization(
                self.game.player_name.get(),
                self.game.selected_character,
                customization
            )
            
            self.game.player_customization = customization
            print(f"✅ Personalización guardada: {len(customization['accessories'])} accesorios")
            self.game.start_game()
        except Exception as e:
            print(f"⚠️ Error guardando personalización: {e}")
            self.game.start_game()  # Iniciar de todos modos
    
    def _lighten_color(self, color, factor=0.2):
        """Aclara un color hexadecimal"""
        try:
            color = color.lstrip('#')
            rgb = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
            light_rgb = tuple(min(255, int(c + (255 - c) * factor)) for c in rgb)
            return '#{:02x}{:02x}{:02x}'.format(*light_rgb)
        except Exception as e:
            print(f"⚠️ Error aclarando color {color}: {e}")
            return color
    
    # ========================================================================
    # MENÚ PRINCIPAL
    # ========================================================================
    
    def show_main_menu(self):
        """Menú principal con diseño en dos columnas horizontales"""
        self.game.clear_screen()
        
        # Frame principal sin scroll
        main_frame = tk.Frame(self.game.root, bg=COLORS['bg'])
        main_frame.pack(expand=True, fill='both', padx=20, pady=10)
        
        # Título principal (arriba, centrado)
        title_container = tk.Frame(main_frame, bg=COLORS['bg'])
        title_container.pack(side='top', pady=15)
        
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
            text="━━━ UNIVERSO CYBERPUNK INTERACTIVO ━━━",
            font=self.game.small_font,
            bg=COLORS['bg'],
            fg=COLORS['text_secondary']
        )
        subtitle_label.pack(pady=(5, 0))
        
        # Contenedor principal horizontal
        horizontal_frame = tk.Frame(main_frame, bg=COLORS['bg'])
        horizontal_frame.pack(expand=True, fill='both', pady=20)
        
        # ============== COLUMNA IZQUIERDA - CONTENIDO ==============
        left_column = tk.Frame(horizontal_frame, bg=COLORS['bg'])
        left_column.pack(side='left', expand=True, fill='both', padx=(0, 15))
        
        # Panel de características
        features_frame = tk.Frame(left_column, bg=COLORS['modal'], relief='groove', bd=3)
        features_frame.pack(fill='both', expand=True, pady=(0, 15))
        
        features_title = tk.Label(
            features_frame,
            text="🎮 CARACTERÍSTICAS",
            font=self.game.header_font,
            bg=COLORS['modal'],
            fg=COLORS['accent']
        )
        features_title.pack(pady=15)
        
        features = [
            "⚔️ Competencia en tiempo real contra IAs",
            "🎯 Sistema de progresión por niveles",
            "💾 Múltiples personajes jugables",
            "🌐 Mundo cyberpunk inmersivo",
            "🏆 Tabla de clasificación global"
        ]
        
        for feature in features:
            feature_label = tk.Label(
                features_frame,
                text=feature,
                font=self.game.small_font,
                bg=COLORS['modal'],
                fg=COLORS['text']
            )
            feature_label.pack(pady=3)
        
        # Preview de personajes
        preview_frame = tk.Frame(left_column, bg=COLORS['modal'], relief='ridge', bd=3)
        preview_frame.pack(fill='both', expand=True)
        
        preview_label = tk.Label(
            preview_frame,
            text="👥 HÉROES DEL CIBERESPACIO",
            font=self.game.header_font,
            bg=COLORS['modal'],
            fg=COLORS['accent']
        )
        preview_label.pack(pady=15)
        
        characters = [
            {'icon': '👤', 'name': 'USUARIO', 'desc': 'Supervivencia', 'diff': 'FÁCIL', 'color': '#00b894'},
            {'icon': '💻', 'name': 'HACKER', 'desc': 'Justicia', 'diff': 'MEDIO', 'color': '#E67E22'},
            {'icon': '🎭', 'name': 'CYBERDELINCUENTE', 'desc': 'Sigilo', 'diff': 'DIFÍCIL', 'color': '#e74c3c'}
        ]
        
        # Frame para organizar personajes horizontalmente - CON TAMAÑO FIJO
        chars_container = tk.Frame(preview_frame, bg=COLORS['modal'])
        chars_container.pack(fill='both', expand=True, padx=15, pady=10)
        
        # Configurar grid para que todas las columnas tengan el mismo peso
        for i in range(len(characters)):
            chars_container.grid_columnconfigure(i, weight=1, uniform="char_columns")
        
        for i, char in enumerate(characters):
            # Frame con tamaño fijo para todos los personajes
            char_frame = tk.Frame(
                chars_container, 
                bg=COLORS['container_bg2'], 
                relief='raised', 
                bd=2,
                highlightbackground=char['color'],
                highlightthickness=2,
                width=180,  # Ancho fijo
                height=180  # Alto fijo
            )
            char_frame.grid(row=0, column=i, padx=5, pady=5, sticky='nsew')
            char_frame.pack_propagate(False)  # Evita que se redimensione automáticamente
            
            # Contenido vertical centrado
            content_frame = tk.Frame(char_frame, bg=COLORS['container_bg2'])
            content_frame.pack(expand=True, fill='both', padx=10, pady=15)
            
            icon_label = tk.Label(
                content_frame,
                text=char['icon'],
                font=('Arial', 24),
                bg=COLORS['container_bg2']
            )
            icon_label.pack(pady=(5, 10))
            
            name_label = tk.Label(
                content_frame,
                text=char['name'],
                font=self.game.normal_font,
                bg=COLORS['container_bg2'],
                fg=char['color'],
                anchor='center',
                wraplength=140  # Para que el texto largo se ajuste
            )
            name_label.pack(fill='x', pady=2)
            
            desc_label = tk.Label(
                content_frame,
                text=char['desc'],
                font=self.game.tiny_font,
                bg=COLORS['container_bg2'],
                fg=COLORS['text_secondary'],
                anchor='center',
                wraplength=140
            )
            desc_label.pack(fill='x', pady=2)
            
            diff_label = tk.Label(
                content_frame,
                text=char['diff'],
                font=self.game.tiny_font,
                bg=COLORS['container_bg2'],
                fg=char['color'],
                anchor='center'
            )
            diff_label.pack(fill='x', pady=2)
        
        # ============== COLUMNA DERECHA - BOTONES ==============
        right_column = tk.Frame(horizontal_frame, bg=COLORS['bg'])
        right_column.pack(side='right', expand=True, fill='both', padx=(15, 0))
        
        # Botones del menú
        button_container = tk.Frame(right_column, bg=COLORS['modal'], relief='groove', bd=3)
        button_container.pack(expand=True, fill='both')
        
        button_title = tk.Label(
            button_container,
            text="🎯 MENÚ PRINCIPAL",
            font=self.game.header_font,
            bg=COLORS['modal'],
            fg=COLORS['accent']
        )
        button_title.pack(pady=25)
        
        button_frame = tk.Frame(button_container, bg=COLORS['modal'])
        button_frame.pack(expand=True, fill='both', padx=30, pady=20)
        
        # MANTENIENDO EXACTAMENTE LOS MISMOS BOTONES Y FUNCIONALIDAD
        menu_buttons = [
            ("🎮 NUEVA AVENTURA", self.show_character_selection, COLORS['primary']),
            ("✨ PERSONALIZAR", lambda: self.show_customization_screen(start_after=False), COLORS['accent']),
            ("🏆 HALL OF FAME", self.show_ranking, '#f1c40f'),
            ("❓ GUÍA DEL SISTEMA", self.show_help, COLORS['container_bg2']),
            ("🚪 SALIR", self.game.root.quit, COLORS['secondary'])
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
                bd=3
            )
            btn.pack(pady=8)
        
        # Footer (abajo, centrado)
        footer_label = tk.Label(
            main_frame,
            text="v1.0 | Desarrollado por RBSC | 2024",
            font=self.game.tiny_font,
            bg=COLORS['bg'],
            fg=COLORS['text_secondary']
        )
        footer_label.pack(side='bottom', pady=5)

    def show_character_selection(self):
        """Pantalla de selección de personaje - MANTENIENDO FUNCIONALIDAD ORIGINAL"""
        self.game.clear_screen()
        
        # Usar un contenedor con padding y scroll si el contenido es mayor que la ventana
        outer = tk.Frame(self.game.root, bg=COLORS['bg'])
        outer.pack(expand=True, fill='both', padx=20, pady=20)
        main_frame, _ = self._create_scrollable_container(outer, bg=COLORS['bg'])
        
        # Título
        title = tk.Label(
            main_frame,
            text="🎭 SELECCIONA TU IDENTIDAD DIGITAL",
            font=self.game.title_font,
            bg=COLORS['bg'],
            fg=COLORS['accent']
        )
        title.pack(pady=30)
        
        # Entrada de nombre
        name_frame = tk.Frame(main_frame, bg=COLORS['modal'], relief='groove', bd=2)
        name_frame.pack(pady=20, padx=200, fill='x')
        
        name_label = tk.Label(
            name_frame,
            text="👤 NOMBRE DE USUARIO:",
            font=self.game.normal_font,
            bg=COLORS['modal'],
            fg=COLORS['text']
        )
        name_label.pack(side='left', padx=20, pady=15)
        
        name_entry = tk.Entry(
            name_frame,
            textvariable=self.game.player_name,
            font=self.game.normal_font,
            bg=COLORS['container_bg2'],
            fg=COLORS['text'],
            insertbackground=COLORS['accent'],
            width=30,
            relief='sunken',
            bd=2
        )
        name_entry.pack(side='left', padx=20, pady=15)
        name_entry.focus()
        
        # Frame de personajes
        characters_frame = tk.Frame(main_frame, bg=COLORS['bg'])
        characters_frame.pack(pady=20, expand=True, fill='both')
        
        # Usando datos locales en lugar de CharacterDatabase
        characters = [
            {
                'type': 'usuario',
                'name': 'USUARIO', 
                'icon': '👤',
                'description': 'Especialista en supervivencia y defensa',
                'difficulty': 'FÁCIL',
                'color': '#00b894'
            },
            {
                'type': 'hacker', 
                'name': 'HACKER',
                'icon': '💻',
                'description': 'Experto en justicia digital y ataques precisos',
                'difficulty': 'MEDIO', 
                'color': '#E67E22'
            },
            {
                'type': 'cyberdelincuente',
                'name': 'CYBERDELINCUENTE',
                'icon': '🎭', 
                'description': 'Maestro del sigilo y ataques sorpresa',
                'difficulty': 'DIFÍCIL',
                'color': '#e74c3c'
            }
        ]
        
        for i, char in enumerate(characters):
            char_container = tk.Frame(
                characters_frame,
                bg=COLORS['modal'],
                highlightbackground=char['color'],
                highlightthickness=3,
                relief='raised',
                bd=3
            )
            char_container.grid(row=0, column=i, padx=25, pady=10, sticky='nsew')
            characters_frame.grid_columnconfigure(i, weight=1)
            
            # Icono
            icon_label = tk.Label(
                char_container,
                text=char['icon'],
                font=('Arial', 56),
                bg=COLORS['modal']
            )
            icon_label.pack(pady=15)
            
            # Nombre
            name_label = tk.Label(
                char_container,
                text=char['name'].upper(),
                font=self.game.header_font,
                bg=COLORS['modal'],
                fg=char['color']
            )
            name_label.pack(pady=8)
            
            # Dificultad
            diff_frame = tk.Frame(char_container, bg=char['color'])
            diff_frame.pack(fill='x', padx=20, pady=5)
            
            diff_label = tk.Label(
                diff_frame,
                text=f"⚡ {char['difficulty']}",
                font=self.game.small_font,
                bg=char['color'],
                fg='white'
            )
            diff_label.pack(pady=3)
            
            # Descripción
            desc_label = tk.Label(
                char_container,
                text=char['description'],
                font=self.game.small_font,
                bg=COLORS['modal'],
                fg=COLORS['text'],
                wraplength=280,
                justify='center'
            )
            desc_label.pack(pady=15, padx=15)
            
            # Estadísticas
            stats_frame = tk.Frame(char_container, bg=COLORS['container_bg2'])
            stats_frame.pack(fill='x', padx=20, pady=10)
            
            stats = {
                'usuario': {'⚡ Velocidad': '★★★☆☆', '🛡️ Defensa': '★★★★☆', '💪 Ataque': '★★☆☆☆'},
                'hacker': {'⚡ Velocidad': '★★★★☆', '🛡️ Defensa': '★★★☆☆', '💪 Ataque': '★★★★☆'},
                'cyberdelincuente': {'⚡ Velocidad': '★★★★★', '🛡️ Defensa': '★★☆☆☆', '💪 Ataque': '★★★★★'}
            }
            
            for stat, value in stats[char['type']].items():
                stat_label = tk.Label(
                    stats_frame,
                    text=f"{stat}: {value}",
                    font=self.game.tiny_font,
                    bg=COLORS['container_bg2'],
                    fg=COLORS['text_secondary'],
                    anchor='w'
                )
                stat_label.pack(fill='x', padx=5, pady=2)
            
            # Botón seleccionar - MANTENIENDO LA FUNCIÓN ORIGINAL
            select_btn = tk.Button(
                char_container,
                text="🎯 SELECCIONAR",
                font=self.game.normal_font,
                bg=char['color'],
                fg='white',
                activebackground=self._lighten_color(char['color']),
                command=lambda c=char['type']: self.select_character(c),
                cursor='hand2',
                height=2,
                relief='raised',
                bd=3
            )
            select_btn.pack(pady=15, padx=20, fill='x')
        
        # Botón volver
        back_btn = tk.Button(
            main_frame,
            text="⬅️ VOLVER AL MENÚ",
            font=self.game.normal_font,
            bg=COLORS['container_bg2'],
            fg=COLORS['text_secondary'],
            command=self.show_main_menu,
            cursor='hand2',
            width=20,
            height=2
        )
        back_btn.pack(pady=20)

    def select_character(self, character_type: str):
        """Selecciona un personaje - FUNCIÓN ORIGINAL EXACTA"""
        if not self.game.player_name.get().strip():
            messagebox.showwarning("⚠️ Nombre requerido", "Por favor ingresa tu nombre de usuario")
            return
        
        self.game.selected_character = character_type
        print(f"✅ Personaje seleccionado: {character_type}")
        self.show_customization_screen(start_after=True)
    
    # ========================================================================
    # PERSONALIZACIÓN
    # ========================================================================
    
    def show_customization_screen(self, start_after=False):
        """Pantalla de personalización de personaje"""
        if not start_after:
            messagebox.showinfo("🎨 Personalización", 
                              "Primero debes seleccionar un personaje para personalizarlo.\n\n"
                              "Ve a 'Nueva Aventura' y elige tu héroe digital.")
            return
        
        self.game.clear_screen()
        
        # Outer container to hold scrollable content and a fixed footer
        outer = tk.Frame(self.game.root, bg=COLORS['bg'])
        outer.pack(expand=True, fill='both', padx=0, pady=0)

        # Scrollable main content (padding applied inside)
        main_frame, _ = self._create_scrollable_container(outer, bg=COLORS['bg'])
        main_frame.pack_configure(padx=20, pady=20)
        
        title = tk.Label(
            main_frame,
            text="✨ PERSONALIZACIÓN DE PERSONAJE",
            font=self.game.title_font,
            bg=COLORS['bg'],
            fg=COLORS['accent']
        )
        title.pack(pady=20)
        
        # Preview del personaje
        preview_frame = tk.Frame(main_frame, bg=COLORS['modal'], relief='groove', bd=3)
        preview_frame.pack(pady=20)
        
        char_data = next((c for c in CharacterDatabase.get_all_characters() 
                         if c['type'] == self.game.selected_character), None)
        
        if char_data:
            preview_icon = tk.Label(
                preview_frame,
                text=char_data['icon'],
                font=('Arial', 72),
                bg=COLORS['modal']
            )
            preview_icon.pack(pady=20)
            
            preview_name = tk.Label(
                preview_frame,
                text=char_data['name'].upper(),
                font=self.game.header_font,
                bg=COLORS['modal'],
                fg=char_data['color']
            )
            preview_name.pack(pady=10)
        
        # Accesorios disponibles
        accessories_frame = tk.Frame(main_frame, bg=COLORS['modal'])
        accessories_frame.pack(pady=20, padx=50, fill='both', expand=True)
        
        accessories_label = tk.Label(
            accessories_frame,
            text="🎁 ACCESORIOS DISPONIBLES",
            font=self.game.header_font,
            bg=COLORS['modal'],
            fg=COLORS['accent']
        )
        accessories_label.pack(pady=15)
        
        accessories = self.game.customization_system.get_available_accessories(
            self.game.selected_character
        )
        
        selected_accessories = []
        
        for acc in accessories:
            acc_frame = tk.Frame(accessories_frame, bg=COLORS['container_bg2'], relief='raised', bd=2)
            acc_frame.pack(fill='x', padx=50, pady=8)
            
            acc_var = tk.BooleanVar()
            
            def toggle_accessory(a=acc, v=acc_var, sl=selected_accessories):
                if v.get():
                    if a not in sl:
                        sl.append(a)
                else:
                    if a in sl:
                        sl.remove(a)
            
            acc_check = tk.Checkbutton(
                acc_frame,
                text=f"{acc['icon']} {acc['name']} - {acc['effect']}",
                font=self.game.normal_font,
                bg=COLORS['container_bg2'],
                fg=COLORS['text'],
                selectcolor=COLORS['primary'],
                variable=acc_var,
                command=toggle_accessory
            )
            acc_check.pack(pady=10, padx=20, anchor='w')
        
        # Botones
        button_frame = tk.Frame(main_frame, bg=COLORS['bg'])
        button_frame.pack(pady=20)
        
        start_btn = tk.Button(
            button_frame,
            text="🚀 COMENZAR AVENTURA",
            font=self.game.normal_font,
            bg=COLORS['primary'],
            fg=COLORS['text_secondary'],
            command=lambda: self.save_customization_and_start(selected_accessories),
            cursor='hand2',
            width=25,
            height=2
        )
        start_btn.pack(side='left', padx=10)
        
        back_btn = tk.Button(
            button_frame,
            text="⬅️ VOLVER",
            font=self.game.normal_font,
            bg=COLORS['container_bg2'],
            fg=COLORS['text_secondary'],
            command=self.show_character_selection,
            cursor='hand2',
            width=15,
            height=2
        )
        back_btn.pack(side='left', padx=10)
    
    # ========================================================================
    # PANTALLA DE JUEGO
    # ========================================================================
    
    def show_game_screen(self):
        """Muestra la pantalla de juego"""
        self.game.clear_screen()
        
        # Verificar si hay etapas disponibles
        if (self.game.current_stage >= len(self.game.current_story['stages']) or 
            self.game.player_progress >= 100):
            self.game.end_game(completed=(self.game.player_progress >= 100))
            return
        
        stage = self.game.current_story['stages'][self.game.current_stage]
        
        main_frame = tk.Frame(self.game.root, bg=COLORS['bg'])
        main_frame.pack(expand=True, fill='both')
        
        # Panel superior
        header_frame = tk.Frame(main_frame, bg=COLORS['header_bg'])
        header_frame.pack(fill='x', pady=(0, 10))
        
        info_text = f"👤 {self.game.player_name.get()} | 🎭 {self.game.selected_character.title()} | ⏱️ {self.game.get_elapsed_time()}s | ❌ Errores: {self.game.player_errors}"
        info_label = tk.Label(
            header_frame,
            text=info_text,
            font=self.game.small_font,
            bg=COLORS['header_bg'],
            fg=COLORS['text']
        )
        info_label.pack(pady=10)

        # Botón para volver al menú siempre visible en la cabecera
        def _confirm_back_to_menu():
            if messagebox.askyesno("Volver al menú", "¿Seguro que quieres volver al menú? Se perderá el progreso actual."):
                # Indicar al game que el usuario pidió el menú y mostrarlo
                setattr(self.game, '_user_requested_menu', False)
                self.game.screens.show_main_menu()

        menu_btn = tk.Button(
            header_frame,
            text="🏠 MENÚ",
            font=self.game.tiny_font,
            bg=COLORS['secondary'],
            fg='white',
            command=_confirm_back_to_menu,
            cursor='hand2'
        )
        menu_btn.pack(side='right', padx=10, pady=8)
        
        # Contenedor principal
        content_frame = tk.Frame(main_frame, bg=COLORS['bg'])
        content_frame.pack(expand=True, fill='both', padx=10)
        
        # COLUMNA IZQUIERDA: Visualización de personajes
        left_frame = tk.Frame(content_frame, bg=COLORS['modal'], width=400, relief='groove', bd=3)
        left_frame.pack(side='left', fill='both', padx=(0, 10), pady=10)
        left_frame.pack_propagate(False)
        
        self.create_character_visualization_panel(left_frame)
        
        # COLUMNA DERECHA: Historia y opciones
        right_frame = tk.Frame(content_frame, bg=COLORS['bg'])
        right_frame.pack(side='right', expand=True, fill='both', pady=10)
        
        # Barra de progreso
        progress_container = tk.Frame(right_frame, bg=COLORS['modal'], relief='sunken', bd=2)
        progress_container.pack(fill='x', padx=20, pady=10)
        
        progress_label = tk.Label(
            progress_container,
            text=f"📊 PROGRESO: {self.game.player_progress}%",
            font=self.game.normal_font,
            bg=COLORS['modal'],
            fg=COLORS['accent']
        )
        progress_label.pack(pady=5)
        
        progress_canvas = tk.Canvas(progress_container, height=30, bg=COLORS['container_bg2'], highlightthickness=0)
        progress_canvas.pack(fill='x', padx=20, pady=5)
        
        self.game.root.update_idletasks()
        canvas_width = progress_canvas.winfo_width()
        if canvas_width > 1:
            fill_width = int((self.game.player_progress / 100) * canvas_width)
            progress_canvas.create_rectangle(0, 0, fill_width, 30, fill=COLORS['accent'], outline='')
            progress_canvas.create_text(
                canvas_width // 2, 15,
                text=f"{self.game.player_progress}%",
                fill=COLORS['text'],
                font=self.game.normal_font
            )
        
        # Eventos globales
        if self.game.global_events:
            events_frame = tk.Frame(right_frame, bg=COLORS['secondary'], relief='raised', bd=2)
            events_frame.pack(fill='x', padx=20, pady=10)
            
            latest_event = self.game.global_events[-1]
            event_label = tk.Label(
                events_frame,
                text=f"🌍 {latest_event['description']}\n{latest_event['effect']}",
                font=self.game.small_font,
                bg=COLORS['secondary'],
                fg='white',
                justify='center'
            )
            event_label.pack(pady=10)
        
        # Área de historia
        story_frame = tk.Frame(right_frame, bg=COLORS['modal'], relief='groove', bd=2)
        story_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        stage_label = tk.Label(
            story_frame,
            text=f"ETAPA {stage['stage']} - {stage['location'].upper()}",
            font=self.game.header_font,
            bg=COLORS['modal'],
            fg=COLORS['accent']
        )
        stage_label.pack(pady=15)
        
        desc_label = tk.Label(
            story_frame,
            text=stage['description'],
            font=self.game.normal_font,
            bg=COLORS['modal'],
            fg=COLORS['text'],
            wraplength=700,
            justify='left'
        )
        desc_label.pack(pady=10, padx=30)
        
        obj_label = tk.Label(
            story_frame,
            text=f"🎯 Objetivo: {self.game.current_story['objective']}",
            font=self.game.normal_font,
            bg=COLORS['modal'],
            fg=COLORS['secondary'],
            wraplength=700
        )
        obj_label.pack(pady=10, padx=30)
        
        # Opciones
        options_label = tk.Label(
            story_frame,
            text="⚡ ¿QUÉ HARÁS?",
            font=self.game.header_font,
            bg=COLORS['modal'],
            fg=COLORS['text']
        )
        options_label.pack(pady=15)
        
        options_container = tk.Frame(story_frame, bg=COLORS['modal'])
        options_container.pack(pady=10, padx=30, fill='both', expand=True)
        
        for i, option in enumerate(stage['options']):
            opt_frame = tk.Frame(
                options_container,
                bg=COLORS['container_bg2'],
                highlightbackground=COLORS['accent'],
                highlightthickness=2,
                relief='raised',
                bd=2
            )
            opt_frame.pack(fill='x', pady=8)
            
            risk_colors = {'bajo': '#00b894', 'medio': '#f39c12', 'alto': '#e74c3c'}
            risk_color = risk_colors.get(option['risk'], COLORS['text_secondary'])
            
            info_text = f"⏱️ {option['time']}min | 🎲 Éxito: {option['success']}% | ⚠️ Riesgo: {option['risk'].upper()}"
            
            opt_btn = tk.Button(
                opt_frame,
                text=f"{i+1}. {option['text']}\n{info_text}",
                font=self.game.normal_font,
                bg=COLORS['container_bg2'],
                fg=COLORS['text'],
                activebackground=risk_color,
                activeforeground='white',
                command=lambda o=option: self.game.process_player_action(o),
                cursor='hand2',
                justify='left',
                anchor='w',
                padx=20,
                pady=12,
                relief='flat'
            )
            opt_btn.pack(fill='x')
    
    def create_character_visualization_panel(self, parent):
        """Panel de visualización de personajes"""
        title_label = tk.Label(
            parent,
            text="🎭 ESTADO DE LOS AGENTES",
            font=self.game.header_font,
            bg=COLORS['modal'],
            fg=COLORS['accent']
        )
        title_label.pack(pady=15)
        
        # Jugador principal
        self.create_character_display(
            parent,
            self.game.selected_character,
            self.game.player_progress,
            self.game.character_states[self.game.selected_character],
            is_player=True
        )
        
        separator = tk.Frame(parent, bg=COLORS['accent'], height=2)
        separator.pack(fill='x', padx=20, pady=15)
        
        # IAs competidoras
        ai_label = tk.Label(
            parent,
            text="🤖 COMPETIDORES IA",
            font=self.game.normal_font,
            bg=COLORS['modal'],
            fg=COLORS['text_secondary']
        )
        ai_label.pack(pady=10)
        
        for ai in self.game.ai_players:
            self.create_character_display(
                parent,
                ai.character_type,
                ai.progress,
                self.game.character_states[ai.character_type],
                is_player=False,
                completed=ai.completed
            )
        
        # Efectos activos
        if self.game.active_effects:
            effects_frame = tk.Frame(parent, bg=COLORS['secondary'], relief='raised', bd=2)
            effects_frame.pack(fill='x', padx=20, pady=10)
            
            effects_title = tk.Label(
                effects_frame,
                text="⚡ EFECTOS ACTIVOS",
                font=self.game.small_font,
                bg=COLORS['secondary'],
                fg='white'
            )
            effects_title.pack(pady=5)
            
            for effect in self.game.active_effects:
                effect_label = tk.Label(
                    effects_frame,
                    text=f"{effect['description']} ({effect['duration']} turnos)",
                    font=self.game.tiny_font,
                    bg=COLORS['secondary'],
                    fg='white'
                )
                effect_label.pack(pady=2)
    
    def create_character_display(self, parent, char_type, progress, state, is_player=False, completed=False):
        """Crea la visualización de un personaje"""
        char_data = next((c for c in CharacterDatabase.get_all_characters() 
                         if c['type'] == char_type), None)
        
        if not char_data:
            return
        
        # Frame del personaje
        char_frame = tk.Frame(
            parent, 
            bg=COLORS['container_bg2'] if is_player else COLORS['bg'],
            relief='raised' if is_player else 'sunken',
            bd=3 if is_player else 2,
            highlightbackground=char_data['color'] if is_player else COLORS['text_secondary'],
            highlightthickness=2 if is_player else 1
        )
        char_frame.pack(fill='x', padx=15, pady=8)
        
        # Header con icono y nombre
        header_frame = tk.Frame(char_frame, bg=char_frame['bg'])
        header_frame.pack(fill='x', pady=5)
        
        # Determinar icono según estado
        icon = char_data['icon']
        if state['health'] < 30:
            icon = '🤕'
        elif state['detection'] > 70:
            icon = '🚨'
        elif completed:
            icon = '🏆'
        elif progress > 80:
            icon = '⚡'
        
        icon_label = tk.Label(
            header_frame,
            text=icon,
            font=('Arial', 32 if is_player else 24),
            bg=header_frame['bg']
        )
        icon_label.pack(side='left', padx=10)
        
        info_frame = tk.Frame(header_frame, bg=header_frame['bg'])
        info_frame.pack(side='left', fill='x', expand=True)
        
        name_label = tk.Label(
            info_frame,
            text=char_data['name'].upper() + (" (TÚ)" if is_player else ""),
            font=self.game.normal_font if is_player else self.game.small_font,
            bg=info_frame['bg'],
            fg=char_data['color']
        )
        name_label.pack(anchor='w')
        
        progress_label = tk.Label(
            info_frame,
            text=f"Progreso: {progress}%",
            font=self.game.tiny_font,
            bg=info_frame['bg'],
            fg=COLORS['text']
        )
        progress_label.pack(anchor='w')
        
        # Barras de estado
        stats_frame = tk.Frame(char_frame, bg=char_frame['bg'])
        stats_frame.pack(fill='x', padx=10, pady=5)
        
        self.create_stat_bar(stats_frame, "💚 Salud", state['health'], '#00b894')
        self.create_stat_bar(stats_frame, "🚨 Detección", state['detection'], '#e74c3c')
        self.create_stat_bar(stats_frame, "💎 Recursos", state['resources'], '#E67E22')
        
        # Estado especial
        if completed:
            status_frame = tk.Frame(char_frame, bg='#f1c40f')
            status_frame.pack(fill='x', pady=5)
            status_label = tk.Label(
                status_frame,
                text="✅ OBJETIVO COMPLETADO",
                font=self.game.small_font,
                bg='#f1c40f',
                fg='white'
            )
            status_label.pack(pady=3)
        
        return char_frame
    
    def create_stat_bar(self, parent, label, value, color):
        """Crea una barra de estadística"""
        stat_container = tk.Frame(parent, bg=parent['bg'])
        stat_container.pack(fill='x', pady=3)
        
        label_widget = tk.Label(
            stat_container,
            text=label,
            font=self.game.tiny_font,
            bg=parent['bg'],
            fg=COLORS['text'],
            width=12,
            anchor='w'
        )
        label_widget.pack(side='left')
        
        bar_canvas = tk.Canvas(stat_container, height=12, bg=COLORS['modal'], highlightthickness=0)
        bar_canvas.pack(side='left', fill='x', expand=True, padx=5)
        
        self.game.root.update_idletasks()
        bar_width = bar_canvas.winfo_width()
        if bar_width > 1:
            fill_width = int((value / 100) * bar_width)
            bar_canvas.create_rectangle(0, 0, fill_width, 12, fill=color, outline='')
        
        value_label = tk.Label(
            stat_container,
            text=f"{value}%",
            font=self.game.tiny_font,
            bg=parent['bg'],
            fg=COLORS['text'],
            width=5
        )
        value_label.pack(side='right')
    
    # ========================================================================
    # RESULTADO DE ACCIÓN
    # ========================================================================
    
    def show_action_result(self, result_text: str, result_color: str, option: dict, success: bool, dialog: str = ""):
        """Muestra el resultado de una acción"""
        result_window = tk.Toplevel(self.game.root)
        result_window.title("Resultado de Acción")
        result_window.geometry("850x600")
        result_window.configure(bg=COLORS['modal'])
        result_window.transient(self.game.root)
        result_window.grab_set()
        
        # Centrar ventana
        result_window.update_idletasks()
        x = (result_window.winfo_screenwidth() // 2) - (result_window.winfo_width() // 2)
        y = (result_window.winfo_screenheight() // 2) - (result_window.winfo_height() // 2)
        result_window.geometry(f"+{x}+{y}")
        
        # Icono de resultado
        icon = "✅" if success else "❌"
        icon_label = tk.Label(
            result_window,
            text=icon,
            font=('Arial', 64),
            bg=COLORS['modal']
        )
        icon_label.pack(pady=20)
        
        # Título del resultado
        title_label = tk.Label(
            result_window,
            text=result_text,
            font=self.game.header_font,
            bg=COLORS['modal'],
            fg=result_color
        )
        title_label.pack(pady=10)
        
        # Diálogo del personaje
        if dialog:
            dialog_frame = tk.Frame(result_window, bg=COLORS['container_bg2'], relief='groove', bd=2)
            dialog_frame.pack(pady=15, padx=40, fill='x')
            
            char_data = next((c for c in CharacterDatabase.get_all_characters() 
                             if c['type'] == self.game.selected_character), None)
            
            if char_data:
                dialog_header = tk.Label(
                    dialog_frame,
                    text=f"{char_data['icon']} {char_data['name']} dice:",
                    font=self.game.normal_font,
                    bg=COLORS['container_bg2'],
                    fg=char_data['color']
                )
                dialog_header.pack(pady=8)
            
            dialog_label = tk.Label(
                dialog_frame,
                text=f'"{dialog}"',
                font=('Arial', 12, 'italic'),
                bg=COLORS['container_bg2'],
                fg=COLORS['text'],
                wraplength=550,
                justify='center'
            )
            dialog_label.pack(pady=10, padx=20)
        
        # Información de la acción
        action_label = tk.Label(
            result_window,
            text=f"Acción realizada: {option['text']}",
            font=self.game.normal_font,
            bg=COLORS['modal'],
            fg=COLORS['text'],
            wraplength=600
        )
        action_label.pack(pady=10)
        
        # Consecuencias
        consequences_frame = tk.Frame(result_window, bg=COLORS['bg'], relief='sunken', bd=2)
        consequences_frame.pack(pady=15, padx=50, fill='x')
        
        if success:
            consequence_texts = [
                "✅ Progreso significativo logrado",
                "✅ No se detectó actividad sospechosa",
                "✅ Recursos mantenidos estables"
            ]
        else:
            consequence_texts = [
                "⚠️ Error registrado en el sistema",
                "⚠️ Nivel de detección aumentado",
                "⚠️ Pérdida de recursos"
            ]
        
        for text in consequence_texts:
            cons_label = tk.Label(
                consequences_frame,
                text=text,
                font=self.game.small_font,
                bg=COLORS['bg'],
                fg=COLORS['text'],
                anchor='w'
            )
            cons_label.pack(pady=3, padx=20, anchor='w')
        
        # Mostrar efectos aplicados
        if self.game.active_effects:
            effects_frame = tk.Frame(result_window, bg=COLORS['secondary'], relief='raised', bd=2)
            effects_frame.pack(pady=10, padx=50, fill='x')
            
            effects_label = tk.Label(
                effects_frame,
                text="⚡ Nuevos efectos activos:",
                font=self.game.small_font,
                bg=COLORS['secondary'],
                fg='white'
            )
            effects_label.pack(pady=5)
            
            for effect in self.game.active_effects[-2:]:
                effect_text = tk.Label(
                    effects_frame,
                    text=effect['description'],
                    font=self.game.tiny_font,
                    bg=COLORS['secondary'],
                    fg='white'
                )
                effect_text.pack(pady=2)
        
        # Progreso actual
        progress_label = tk.Label(
            result_window,
            text=f"📊 Progreso total: {self.game.player_progress}%",
            font=self.game.normal_font,
            bg=COLORS['modal'],
            fg=COLORS['accent']
        )
        progress_label.pack(pady=10)
        
        # Botones: continuar y volver al menú
        btn_frame = tk.Frame(result_window, bg=COLORS['modal'])
        btn_frame.pack(pady=20)

        continue_btn = tk.Button(
            btn_frame,
            text="➡️ SIGUIENTE",
            font=self.game.normal_font,
            bg=COLORS['primary'],
            fg=COLORS['text_secondary'],
            command=lambda: result_window.destroy(),
            cursor='hand2',
            width=20,
            height=2
        )
        continue_btn.pack(side='left', padx=10)

        menu_btn = tk.Button(
            btn_frame,
            text="🏠 MENÚ",
            font=self.game.normal_font,
            bg=COLORS['secondary'],
            fg=COLORS['text_secondary'],
            command=lambda: [setattr(self.game, '_user_requested_menu', True), result_window.destroy()],
            cursor='hand2',
            width=12,
            height=2
        )
        menu_btn.pack(side='left', padx=10)

        # Esperar a que el usuario cierre el modal (bloqueante) antes de volver
        result_window.wait_window()
    
    # ========================================================================
    # PANTALLA DE RESULTADOS
    # ========================================================================
    
    def show_results_screen(self, completed: bool, elapsed_time: int, winner: str = None):
        """Muestra la pantalla de resultados finales"""
        self.game.clear_screen()

        # Outer container to hold scrollable content and a fixed footer
        outer = tk.Frame(self.game.root, bg=COLORS['bg'])
        outer.pack(expand=True, fill='both', padx=0, pady=0)

        # Scrollable main content (padding applied inside)
        main_frame, _ = self._create_scrollable_container(outer, bg=COLORS['bg'])
        main_frame.pack_configure(padx=20, pady=20)

        # Determinar resultado
        if completed:
            title_text = "🏆 ¡VICTORIA TOTAL!"
            title_color = COLORS['accent']
            icon = "🎉"
            message = "¡Felicitaciones! Has completado tu objetivo exitosamente y superaste a todos tus competidores."
        else:
            title_text = "❌ MISIÓN FALLIDA"
            title_color = COLORS['secondary']
            icon = "💔"
            if winner == "system_failure":
                message = "Tu salud llegó a cero. El sistema te ha neutralizado."
            elif winner == "detected":
                message = "Fuiste detectado por el sistema de seguridad. Misión comprometida."
            elif winner == "time_out":
                message = "Se acabó el tiempo. No lograste completar el objetivo."
            elif winner:
                message = f"El {winner.title()} (IA) completó el objetivo primero. Mejor suerte la próxima vez."
            else:
                message = "No lograste completar el objetivo a tiempo."

        # Icono grande
        icon_label = tk.Label(
            main_frame,
            text=icon,
            font=('Arial', 80),
            bg=COLORS['bg']
        )
        icon_label.pack(pady=30)

        # Título
        title_label = tk.Label(
            main_frame,
            text=title_text,
            font=self.game.title_font,
            bg=COLORS['bg'],
            fg=title_color
        )
        title_label.pack(pady=10)

        # Mensaje
        message_label = tk.Label(
            main_frame,
            text=message,
            font=self.game.normal_font,
            bg=COLORS['bg'],
            fg=COLORS['text'],
            wraplength=800,
            justify='center'
        )
        message_label.pack(pady=15)

        # Panel de estadísticas
        stats_frame = tk.Frame(main_frame, bg=COLORS['modal'], relief='groove', bd=3)
        stats_frame.pack(pady=20, padx=100, fill='both')

        stats_title = tk.Label(
            stats_frame,
            text="📊 ESTADÍSTICAS DE LA MISIÓN",
            font=self.game.header_font,
            bg=COLORS['modal'],
            fg=COLORS['accent']
        )
        stats_title.pack(pady=20)

        # Estadísticas detalladas
        stats_data = [
            ("👤 Jugador", self.game.player_name.get()),
            ("🎭 Personaje", self.game.selected_character.title()),
            ("⏱️ Tiempo total", f"{elapsed_time} segundos"),
            ("❌ Errores cometidos", str(self.game.player_errors)),
            ("📈 Progreso final", f"{self.game.player_progress}%"),
            ("🎯 Etapas completadas", f"{self.game.current_stage}/{len(self.game.current_story['stages'])}"),
            ("🔄 Turnos jugados", str(self.game.turn_count))
        ]

        for label, value in stats_data:
            stat_container = tk.Frame(stats_frame, bg=COLORS['container_bg2'])
            stat_container.pack(pady=5, padx=40, fill='x')

            stat_label = tk.Label(
                stat_container,
                text=label,
                font=self.game.normal_font,
                bg=COLORS['container_bg2'],
                fg=COLORS['text_secondary'],
                anchor='w',
                width=20
            )
            stat_label.pack(side='left', padx=10)

            stat_value = tk.Label(
                stat_container,
                text=value,
                font=self.game.normal_font,
                bg=COLORS['container_bg2'],
                fg=COLORS['accent'],
                anchor='e'
            )
            stat_value.pack(side='right', padx=10)

        # Puntuación final
        if completed:
            score = self.game.ranking_system._calculate_score(elapsed_time, self.game.player_errors, completed)
            score_frame = tk.Frame(stats_frame, bg=COLORS['primary'], relief='raised', bd=3)
            score_frame.pack(pady=20, padx=40, fill='x')

            score_label = tk.Label(
                score_frame,
                text=f"⭐ PUNTUACIÓN FINAL: {int(score)} PUNTOS",
                font=self.game.header_font,
                bg=COLORS['primary'],
                fg='white'
            )
            score_label.pack(pady=15)

        # Estado final de personajes
        final_states_frame = tk.Frame(main_frame, bg=COLORS['modal'], relief='sunken', bd=2)
        final_states_frame.pack(pady=15, padx=100, fill='x')

        final_states_title = tk.Label(
            final_states_frame,
            text="🎭 ESTADO FINAL DE AGENTES",
            font=self.game.normal_font,
            bg=COLORS['modal'],
            fg=COLORS['text_secondary']
        )
        final_states_title.pack(pady=10)

        # Mostrar estados finales
        all_chars = [self.game.selected_character] + [ai.character_type for ai in self.game.ai_players]
        for char_type in all_chars:
            state = self.game.character_states[char_type]
            is_player = (char_type == self.game.selected_character)

            char_state_frame = tk.Frame(final_states_frame, bg=COLORS['container_bg2'])
            char_state_frame.pack(pady=3, padx=20, fill='x')

            char_name = char_type.title() + (" (TÚ)" if is_player else " (IA)")
            progress = self.game.player_progress if is_player else next((ai.progress for ai in self.game.ai_players if ai.character_type == char_type), 0)

            state_text = f"{char_name}: {progress}% | 💚 {state['health']}% | 🚨 {state['detection']}%"

            state_label = tk.Label(
                char_state_frame,
                text=state_text,
                font=self.game.small_font,
                bg=COLORS['container_bg2'],
                fg=COLORS['text']
            )
            state_label.pack(pady=5)

        # Footer fijo con botones para que siempre sean visibles
        footer = tk.Frame(outer, bg=COLORS['bg'])
        footer.pack(side='bottom', fill='x', pady=12)

        button_frame = tk.Frame(footer, bg=COLORS['bg'])
        button_frame.pack(pady=5)

        buttons = [
            ("🎮 NUEVA PARTIDA", self.show_character_selection, COLORS['primary']),
            ("🏆 VER RANKING", self.show_ranking, '#f1c40f'),
            ("🏠 MENÚ PRINCIPAL", self.show_main_menu, COLORS['secondary'])
        ]

        for text, command, color in buttons:
            btn = tk.Button(
                button_frame,
                text=text,
                font=self.game.normal_font,
                bg=color,
                fg=COLORS['text_secondary'],
                command=command,
                cursor='hand2',
                width=20,
                height=2
            )
            btn.pack(side='left', padx=10)
    
    # ========================================================================
    # RANKING
    # ========================================================================
    
    def show_ranking(self):
        """Muestra el ranking de jugadores"""
        self.game.clear_screen()
        
        main_frame = tk.Frame(self.game.root, bg=COLORS['bg'])
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Título
        title_label = tk.Label(
            main_frame,
            text="🏆 HALL OF FAME",
            font=self.game.title_font,
            bg=COLORS['bg'],
            fg='#f1c40f'
        )
        title_label.pack(pady=30)
        
        subtitle_label = tk.Label(
            main_frame,
            text="Los mejores agentes del ciberespacio",
            font=self.game.normal_font,
            bg=COLORS['bg'],
            fg=COLORS['text_secondary']
        )
        subtitle_label.pack(pady=10)
        
        # Contenedor de tabla
        table_container = tk.Frame(main_frame, bg=COLORS['modal'], relief='groove', bd=3)
        table_container.pack(pady=20, fill='both', expand=True, padx=50)
        
        # Canvas para scroll
        canvas = tk.Canvas(table_container, bg=COLORS['modal'], highlightthickness=0)
        scrollbar = tk.Scrollbar(table_container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=COLORS['modal'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Encabezados
        headers_frame = tk.Frame(scrollable_frame, bg=COLORS['header_bg'])
        headers_frame.pack(fill='x', pady=(10, 5))
        
        headers = [
            ('🏅', 5),
            ('Jugador', 15),
            ('Personaje', 15),
            ('Tiempo', 10),
            ('Errores', 8),
            ('Puntuación', 12),
            ('Fecha', 12)
        ]
        
        for i, (header, width) in enumerate(headers):
            label = tk.Label(
                headers_frame,
                text=header,
                font=self.game.normal_font,
                bg=COLORS['header_bg'],
                fg=COLORS['text_secondary'],
                width=width
            )
            label.grid(row=0, column=i, padx=5, pady=10)
        
        # Cargar rankings
        rankings = self.game.ranking_system.get_top_rankings(20)
        
        if rankings:
            for idx, entry in enumerate(rankings):
                row_bg = COLORS['container_bg2'] if idx % 2 == 0 else COLORS['bg']
                
                medal = ""
                if idx == 0:
                    medal = "🥇"
                    row_bg = '#ffd700'
                elif idx == 1:
                    medal = "🥈"
                    row_bg = '#c0c0c0'
                elif idx == 2:
                    medal = "🥉"
                    row_bg = '#cd7f32'
                
                row_frame = tk.Frame(scrollable_frame, bg=row_bg)
                row_frame.pack(fill='x', pady=2)
                
                data = [
                    f"{medal} #{idx + 1}",
                    entry['player'][:15],
                    entry['character'][:15],
                    f"{entry['time']}s",
                    str(entry['errors']),
                    str(int(entry['score'])),
                    entry['date'].split()[0]
                ]
                
                for i, (value, (_, width)) in enumerate(zip(data, headers)):
                    label = tk.Label(
                        row_frame,
                        text=value,
                        font=self.game.small_font,
                        bg=row_bg,
                        fg='black' if idx < 3 else COLORS['text'],
                        width=width
                    )
                    label.grid(row=0, column=i, padx=5, pady=8)
        else:
            no_data_label = tk.Label(
                scrollable_frame,
                text="🔭 No hay partidas registradas aún\n\n¡Sé el primero en el ranking!",
                font=self.game.header_font,
                bg=COLORS['modal'],
                fg=COLORS['text_secondary'],
                justify='center'
            )
            no_data_label.pack(pady=80)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Botones
        button_frame = tk.Frame(main_frame, bg=COLORS['bg'])
        button_frame.pack(pady=20)
        
        back_btn = tk.Button(
            button_frame,
            text="⬅️ VOLVER",
            font=self.game.normal_font,
            bg=COLORS['container_bg2'],
            fg=COLORS['text_secondary'],
            command=self.show_main_menu,
            cursor='hand2',
            width=15,
            height=2
        )
        back_btn.pack(side='left', padx=10)
        
        clear_btn = tk.Button(
            button_frame,
            text="🗑️ LIMPIAR RANKING",
            font=self.game.normal_font,
            bg=COLORS['secondary'],
            fg=COLORS['text_secondary'],
            command=self.clear_ranking_confirm,
            cursor='hand2',
            width=18,
            height=2
        )
        clear_btn.pack(side='left', padx=10)
    
    def clear_ranking_confirm(self):
        """Confirma antes de limpiar el ranking"""
        if messagebox.askyesno("⚠️ Confirmar", "¿Estás seguro de que quieres eliminar todos los registros del ranking?"):
            self.game.ranking_system.clear_rankings()
            messagebox.showinfo("✅ Completado", "Ranking limpiado exitosamente")
            self.show_ranking()
    
    # ========================================================================
    # AYUDA
    # ========================================================================
    
    def show_help(self):
        """Muestra la pantalla de ayuda"""
        self.game.clear_screen()
        
        main_frame = tk.Frame(self.game.root, bg=COLORS['bg'])
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Título
        title_label = tk.Label(
            main_frame,
            text="❓ GUÍA DEL SISTEMA",
            font=self.game.title_font,
            bg=COLORS['bg'],
            fg=COLORS['accent']
        )
        title_label.pack(pady=20)
        
        # Frame con scroll
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
                'content': 'Completa tu objetivo antes que los competidores IA. Cada personaje tiene una misión única basada en su rol. Toma decisiones estratégicas considerando tiempo, éxito y riesgo. Gestiona tu salud, detección y recursos para mantenerte en el juego.'
            },
            {
                'title': '👥 PERSONAJES DISPONIBLES',
                'content': '• USUARIO (Fácil): Ciudadano común que debe sobrevivir y proteger su información personal.\n\n• HACKER ÉTICO (Medio): Experto en seguridad que expone vulnerabilidades para proteger sistemas.\n\n• CYBERDELINCUENTE (Difícil): Maestro del sigilo que opera en las sombras sin ser detectado.'
            },
            {
                'title': '🎲 MECÁNICAS DE JUEGO',
                'content': 'Cada decisión tiene:\n• PORCENTAJE DE ÉXITO: Probabilidad de completar la acción\n• TIEMPO REQUERIDO: Minutos que toma la acción\n• NIVEL DE RIESGO: Bajo, Medio o Alto\n\nLas acciones exitosas otorgan más progreso. Los errores te penalizan pero aún otorgan progreso mínimo.'
            },
            {
                'title': '💚 SISTEMA DE ESTADOS',
                'content': '• SALUD: Tu vitalidad digital. Si llega a 0, pierdes automáticamente.\n• DETECCIÓN: Nivel de alerta del sistema. A 100%, serás expulsado.\n• RECURSOS: Tu capacidad de operar. Afecta el éxito de acciones futuras.\n\nManeja estos tres valores cuidadosamente para sobrevivir.'
            },
            {
                'title': '⚡ EFECTOS Y ESTADOS',
                'content': '• VIRUS: Reduce tu tasa de éxito temporalmente\n• FIREWALL BLOQUEADO: Penaliza tu próxima acción\n• SOBRECARGA DEL SISTEMA: Aumenta tu tasa de éxito\n• ENCRIPTACIÓN: Fortalece tus defensas\n\nLos efectos duran varios turnos y se acumulan.'
            },
            {
                'title': '🌍 EVENTOS GLOBALES',
                'content': 'Durante el juego ocurren eventos que afectan a TODOS los jugadores:\n• Alertas de seguridad\n• Vulnerabilidades descubiertas\n• Corrupción de datos\n• Mejoras de red\n\nEstos eventos crean una experiencia dinámica e impredecible.'
            },
            {
                'title': '🏆 SISTEMA DE PUNTUACIÓN',
                'content': 'Tu puntuación se calcula según:\n• Tiempo empleado (menos es mejor)\n• Errores cometidos (menos es mejor)\n• Si completaste el objetivo\n• Bonificaciones por tiempo récord\n\nLas mejores puntuaciones aparecen en el Hall of Fame.'
            },
            {
                'title': '🤖 COMPETIDORES IA',
                'content': 'Los personajes no seleccionados son controlados por IA avanzada. Compiten simultáneamente contigo y pueden:\n• Tomar decisiones estratégicas\n• Verse afectados por eventos globales\n• Completar el objetivo antes que tú\n\nSi una IA gana, pierdes la partida.'
            },
            {
                'title': '✨ PERSONALIZACIÓN',
                'content': 'Antes de cada partida puedes equipar accesorios que otorgan ventajas:\n• Escudos digitales\n• Analizadores avanzados\n• Herramientas especiales\n• Capas de sigilo\n\nElige sabiamente según tu estrategia.'
            },
            {
                'title': '💡 CONSEJOS ESTRATÉGICOS',
                'content': '• Balancea riesgo y recompensa según tu situación\n• Monitorea constantemente los estados de todos los jugadores\n• Usa acciones de bajo riesgo cuando tu detección es alta\n• Aprovecha los eventos globales a tu favor\n• No subestimes a las IAs, especialmente en dificultad alta'
            }
        ]
        
        for section in help_sections:
            section_frame = tk.Frame(scrollable_frame, bg=COLORS['container_bg2'], relief='raised', bd=2)
            section_frame.pack(fill='x', pady=10, padx=30)
            
            title_label = tk.Label(
                section_frame,
                text=section['title'],
                font=self.game.normal_font,
                bg=COLORS['container_bg2'],
                fg=COLORS['accent']
            )
            title_label.pack(anchor='w', pady=8, padx=20)
            
            content_label = tk.Label(
                section_frame,
                text=section['content'],
                font=self.game.small_font,
                bg=COLORS['container_bg2'],
                fg=COLORS['text'],
                wraplength=1000,
                justify='left'
            )
            content_label.pack(anchor='w', padx=30, pady=10)
        
        # Créditos
        credits_frame = tk.Frame(scrollable_frame, bg=COLORS['modal'])
        credits_frame.pack(pady=30)
        
        credits_label = tk.Label(
            credits_frame,
            text="💻 Desarrollado por RBSC | 2024\n🎮 Cyber Quest RPG v1.0\n🤖 Powered by AI",
            font=self.game.small_font,
            bg=COLORS['modal'],
            fg=COLORS['text_secondary'],
            justify='center'
        )
        credits_label.pack(pady=20)
        
        canvas.pack(side="left", fill="both", expand=True, padx=50)
        scrollbar.pack(side="right", fill="y")
        
        # Botón volver
        back_btn = tk.Button(
            main_frame,
            text="⬅️ VOLVER AL MENÚ",
            font=self.game.normal_font,
            bg=COLORS['container_bg2'],
            fg=COLORS['text_secondary'],
            command=self.show_main_menu,
            cursor='hand2',
            width=20,
            height=2
        )
        back_btn.pack(pady=20)