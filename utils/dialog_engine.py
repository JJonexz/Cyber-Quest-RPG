# utils/dialog_engine.py
import random
from typing import Dict, List

class DialogEngine:
    """Motor de diálogos - Versión sin dependencias externas"""
    
    def __init__(self):
        self.enabled = True  # Siempre habilitado con diálogos locales
    
    def generate_character_dialog(self, character_type: str, situation: str, emotion: str = "neutral") -> str:
        """Genera diálogo contextual para personajes usando base local mejorada"""
        return self._get_enhanced_dialog(character_type, situation, emotion)
    
    def _get_enhanced_dialog(self, character_type: str, situation: str, emotion: str) -> str:
        """Diálogos mejorados locales sin dependencia de API externa"""
        dialogs = {
            'usuario': {
                'neutral': [
                    "El sistema parece estable... por ahora.", 
                    "Verificando protocolos de seguridad.",
                    "Todo en orden, procediendo con cautela.",
                    "Monitoreando actividad del sistema.",
                    "Revisando integridad de los datos."
                ],
                'stressed': [
                    "¡La presión aumenta! Necesito mantener la calma...",
                    "El sistema se está volviendo impredecible.",
                    "¡Algo no anda bien! Debo actuar con cuidado.",
                    "Las defensas se están activando, ¡cuidado!",
                    "¡La situación se complica! Buscando salida..."
                ],
                'victory': [
                    "¡Lo logré! El sistema es seguro nuevamente.",
                    "Victoria para los usuarios comunes. ¡Éxito!",
                    "Protección activada. Mis datos están a salvo.",
                    "¡Operación completada! Sistema estabilizado.",
                    "¡Crisis evitada! Todo bajo control."
                ],
                'action': [
                    "Ejecutando protocolo de seguridad...",
                    "Activando medidas defensivas.",
                    "Analizando posibles amenazas...",
                    "Implementando contramedidas.",
                    "Reforzando protecciones del sistema."
                ]
            },
            'hacker': {
                'neutral': [
                    "Analizando vectores de ataque... Firewalls detectados.",
                    "Escaneando vulnerabilidades del sistema.",
                    "Monitoreando tráfico de red sospechoso.",
                    "Preparando herramientas de análisis.",
                    "Evaluando puntos de entrada potenciales."
                ],
                'stressed': [
                    "¡Contramedidas activadas! El sistema se defiende...",
                    "Alerta: Múltiples amenazas detectadas.",
                    "¡Casi me detectan! Activando evasión...",
                    "La resistencia del sistema es mayor de lo esperado.",
                    "¡Firewalls reforzados! Necesito otra estrategia."
                ],
                'victory': [
                    "¡Sistemas expuestos! Justicia digital servida.",
                    "La verdad sale a la luz. Misión cumplida.",
                    "Vulnerabilidades parchadas. Sistema seguro.",
                    "¡Éxito! Los datos están protegidos.",
                    "Amenaza neutralizada. Trabajo completado."
                ],
                'action': [
                    "Desplegando exploits...",
                    "Infiltrando sistemas de seguridad.",
                    "Ejecutando scripts de penetración.",
                    "Analizando código fuente en busca de fallos.",
                    "Probando vectores de ataque alternativos."
                ]
            },
            'cyberdelincuente': {
                'neutral': [
                    "Operando en las sombras... Rastreo evadido.",
                    "Movimientos sigilosos activados.",
                    "Navegando por los canales oscuros.",
                    "Preparando el próximo movimiento.",
                    "Evaluando riesgos y recompensas."
                ],
                'stressed': [
                    "¡Casi me detectan! Activando protocolos de escape...",
                    "Las defensas son más fuertes de lo esperado.",
                    "¡Alerta! Rastreadores activados en el sector.",
                    "Necesito cubrir mis huellas rápidamente.",
                    "¡Situación crítica! Plan B activado."
                ],
                'victory': [
                    "¡El botín es mío! Operación completada con éxito.",
                    "Objetivo alcanzado. Recursos obtenidos.",
                    "¡Éxito total! Sin dejar rastros.",
                    "Misión cumplida. Retirándose del área.",
                    "¡Tesoro adquirido! Operación impecable."
                ],
                'action': [
                    "Ejecutando procedimientos de infiltración...",
                    "Instalando backdoors silenciosos.",
                    "Exfiltrando datos sensibles...",
                    "Activando medidas de evasión avanzadas.",
                    "Manipulando sistemas de registro."
                ]
            }
        }
        
        # Mapeo inteligente de emociones basado en situación
        if any(word in situation.lower() for word in ['éxito', 'exito', 'victoria', 'completado', 'logrado']):
            emotion_key = 'victory'
        elif any(word in situation.lower() for word in ['peligro', 'amenaza', 'estrés', 'estres', 'problema', 'error']):
            emotion_key = 'stressed'
        elif any(word in situation.lower() for word in ['acción', 'accion', 'decisión', 'decisión', 'opción']):
            emotion_key = 'action'
        else:
            emotion_key = emotion
        
        # Obtener diálogos disponibles o usar default
        character_dialogs = dialogs.get(character_type, dialogs['usuario'])
        available_dialogs = character_dialogs.get(emotion_key, character_dialogs['neutral'])
        
        return random.choice(available_dialogs)