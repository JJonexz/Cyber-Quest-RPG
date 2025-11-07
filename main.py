# ============================================================================
# ARCHIVO: main.py
# DESCRIPCIÓN: Punto de entrada principal del juego. Inicializa la ventana
#              y coordina todos los módulos del sistema.
# ============================================================================

import tkinter as tk
from game.game_manager import CyberQuestGame
from utils.audio_manager import AudioManager

def main():
    """Función principal del juego"""
    root = tk.Tk()
    
    # Configurar icono de ventana (opcional)
    try:
        # root.iconbitmap('assets/icon.ico')
        pass
    except:
        pass
    
    # Crear instancia del juego
    game = CyberQuestGame(root)
    
    # Iniciar audio manager (opcional)
    audio = AudioManager()
    
    # Iniciar loop principal
    root.mainloop()

if __name__ == "__main__":
    main()

