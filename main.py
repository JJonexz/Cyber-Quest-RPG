# main.py
import tkinter as tk
from game.game_manager import CyberQuestGame

def main():
    """Función principal del juego"""
    try:
        root = tk.Tk()
        root.title("⚡ CYBER QUEST RPG")
        root.geometry("1200x800")
        
        # Crear instancia del juego
        game = CyberQuestGame(root)
        
        # Iniciar loop principal
        root.mainloop()
        
    except Exception as e:
        print(f"Error iniciando el juego: {e}")
        input("Presiona Enter para salir...")

if __name__ == "__main__":
    main()