# main.py - VERSIÓN CORREGIDA
import tkinter as tk
import os
import sys
from game.game_manager import CyberQuestGame

def main():
    """Función principal del juego"""
    try:
        # Configurar API key de Gemini
        os.environ['GEMINI_API_KEY'] = 'AIzaSyA0KzSkYvmfzYxMqLBp9CHnkFjtgzHjvyY'
        
        print("=" * 60)
        print("⚡ INICIANDO CYBER QUEST RPG ⚡")
        print("=" * 60)
        print("✅ Configurando entorno...")
        
        # Crear ventana principal
        root = tk.Tk()
        root.title("⚡ CYBER QUEST RPG")
        root.geometry("1400x900")
        
        # Centrar ventana
        root.update_idletasks()
        width = root.winfo_width()
        height = root.winfo_height()
        x = (root.winfo_screenwidth() // 2) - (width // 2)
        y = (root.winfo_screenheight() // 2) - (height // 2)
        root.geometry(f'{width}x{height}+{x}+{y}')
        
        print("✅ Ventana creada correctamente")
        
        # Crear instancia del juego
        print("✅ Inicializando sistemas del juego...")
        game = CyberQuestGame(root)
        
        print("✅ Juego inicializado correctamente")
        print("=" * 60)
        print("🎮 ¡Disfruta el juego!")
        print("=" * 60)
        
        # Iniciar loop principal
        root.mainloop()
        
    except Exception as e:
        print(f"❌ Error iniciando el juego: {e}")
        import traceback
        traceback.print_exc()
        input("\nPresiona Enter para salir...")

if __name__ == "__main__":
    main()