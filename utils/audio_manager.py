

# ============================================================================
# ARCHIVO: utils/audio_manager.py
# DESCRIPCIÓN: Sistema de gestión de audio. Preparado para reproducir música
#              y efectos de sonido (requiere pygame, opcional).
# ============================================================================

class AudioManager:
    """
    Sistema de audio preparado para integración futura.
    Requiere: pygame o playsound
    
    Para usar:
    1. Instalar: pip install pygame
    2. Colocar archivos de audio en carpeta 'assets/audio/'
    3. Descomentar el código de inicialización
    """
    
    def __init__(self):
        self.enabled = False
        self.music_volume = 0.5
        self.sfx_volume = 0.7
        
        # Descomenta para habilitar audio con pygame:
        # try:
        #     import pygame
        #     pygame.mixer.init()
        #     self.enabled = True
        # except:
        #     print("Audio no disponible - pygame no instalado")
    
    def play_music(self, track_name: str, loop: bool = True):
        """Reproduce música de fondo"""
        if not self.enabled:
            return
        # Implementar con pygame.mixer.music.load() y play()
    
    def play_sfx(self, sound_name: str):
        """Reproduce efecto de sonido"""
        if not self.enabled:
            return
        # Implementar con pygame.mixer.Sound()
    
    def stop_music(self):
        """Detiene la música"""
        if not self.enabled:
            return
        # Implementar con pygame.mixer.music.stop()
    
    def set_music_volume(self, volume: float):
        """Ajusta volumen de música (0.0 a 1.0)"""
        self.music_volume = max(0.0, min(1.0, volume))
    
    def set_sfx_volume(self, volume: float):
        """Ajusta volumen de efectos (0.0 a 1.0)"""
        self.sfx_volume = max(0.0, min(1.0, volume))

