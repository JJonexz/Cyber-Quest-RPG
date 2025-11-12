# utils/dialog_engine.py - VERSIÓN MEJORADA CON MÁS CONTENIDO
import random
from typing import Dict, List
import os

class DialogEngine:
    """Motor de diálogos mejorado con más contenido y mejor integración"""
    
    def __init__(self):
        self.gemini_enabled = False
        self.model = None
        self._initialize_gemini()
    
    def _initialize_gemini(self):
        """Intenta inicializar Gemini AI (opcional)"""
        try:
            import google.generativeai as genai
            
            api_key = os.getenv('GEMINI_API_KEY')
            if not api_key:
                # Intentar con clave hardcoded como fallback
                api_key = 'AIzaSyA0KzSkYvmfzYxMqLBp9CHnkFjtgzHjvyY'
            
            if api_key:
                genai.configure(api_key=api_key)
                
                generation_config = {
                    "temperature": 0.9,
                    "top_p": 0.95,
                    "top_k": 40,
                    "max_output_tokens": 100,
                }
                
                safety_settings = [
                    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
                ]
                
                self.model = genai.GenerativeModel(
                    model_name='gemini-pro',
                    generation_config=generation_config,
                    safety_settings=safety_settings
                )
                
                self.gemini_enabled = True
                print("✅ Gemini AI habilitado para diálogos")
            else:
                print("ℹ️ GEMINI_API_KEY no encontrada - usando diálogos locales")
        except ImportError:
            print("ℹ️ google-generativeai no instalado - usando diálogos locales")
            print("   Instalar con: pip install google-generativeai")
        except Exception as e:
            print(f"⚠️ Error inicializando Gemini: {e} - usando diálogos locales")
    
    def generate_character_dialog(self, character_type: str, situation: str, emotion: str = "neutral") -> str:
        """Genera diálogo contextual para personajes - MEJORADO"""
        
        # Intentar usar Gemini AI si está disponible
        if self.gemini_enabled:
            try:
                gemini_dialog = self._generate_with_gemini(character_type, situation, emotion)
                if gemini_dialog:
                    return gemini_dialog
            except Exception as e:
                print(f"⚠️ Error en Gemini, usando fallback: {e}")
        
        # Fallback a diálogos locales mejorados
        return self._get_enhanced_dialog(character_type, situation, emotion)
    
    def _generate_with_gemini(self, character_type: str, situation: str, emotion: str) -> str:
        """Genera diálogo usando Gemini AI - MEJORADO"""
        
        personalities = {
            'usuario': {
                'role': 'un ciudadano común preocupado por su privacidad digital',
                'traits': 'cauteloso, nervioso pero determinado, usa lenguaje cotidiano',
                'style': 'expresiones de preocupación y alivio, tono personal'
            },
            'hacker': {
                'role': 'un hacker ético experto en seguridad informática',
                'traits': 'confiado, técnico, usa jerga de ciberseguridad',
                'style': 'referencias técnicas, tono profesional pero accesible'
            },
            'cyberdelincuente': {
                'role': 'un operativo sigiloso que trabaja en las sombras',
                'traits': 'misterioso, calculador, habla con precisión',
                'style': 'metáforas oscuras, tono enigmático y directo'
            }
        }
        
        personality = personalities.get(character_type, personalities['usuario'])
        
        prompt = f"""Eres {personality['role']} en un juego cyberpunk.

Personalidad: {personality['traits']}
Estilo: {personality['style']}

Situación actual: {situation}
Estado emocional: {emotion}

Genera UN diálogo CORTO (máximo 20 palabras) que el personaje diría en esta situación.
El diálogo debe ser INMERSIVO, en ESPAÑOL, y reflejar la personalidad del personaje.
NO uses comillas. Solo el diálogo directo.

Tu diálogo:"""
        
        try:
            response = self.model.generate_content(prompt)
            
            if response and response.text:
                dialog = response.text.strip()
                dialog = dialog.replace('"', '').replace("'", "").strip()
                words = dialog.split()
                if len(words) > 25:
                    dialog = ' '.join(words[:25]) + '...'
                return dialog
        except Exception as e:
            print(f"⚠️ Error específico en Gemini: {e}")
        
        return None
    
    def _get_enhanced_dialog(self, character_type: str, situation: str, emotion: str) -> str:
        """Diálogos mejorados locales como fallback - CONTENIDO EXPANDIDO"""
        dialogs = {
            'usuario': {
                'neutral': [
                    "El sistema parece estable... por ahora.", 
                    "Verificando protocolos de seguridad.",
                    "Todo en orden, procediendo con cautela.",
                    "Monitoreando actividad del sistema.",
                    "Revisando integridad de los datos.",
                    "Espero que esto funcione...",
                    "Debo mantener la calma y pensar con claridad.",
                    "Mi información personal está en riesgo.",
                    "Cada paso debe ser calculado.",
                    "No puedo permitir errores ahora.",
                    "La interfaz responde adecuadamente.",
                    "Sigo los procedimientos establecidos.",
                    "Confirmando que todo esté en orden.",
                    "La seguridad es mi prioridad absoluta.",
                    "Avanzando con precaución necesaria."
                ],
                'stressed': [
                    "¡La presión aumenta! Necesito mantener la calma...",
                    "El sistema se está volviendo impredecible.",
                    "¡Algo no anda bien! Debo actuar con cuidado.",
                    "Las defensas se están activando, ¡cuidado!",
                    "¡La situación se complica! Buscando salida...",
                    "¡Detectaron actividad sospechosa!",
                    "No puedo permitir que accedan a mis datos.",
                    "Esto es más peligroso de lo que pensaba...",
                    "El tiempo se agota rápidamente.",
                    "¡Necesito una solución ya!",
                    "¡Las alertas no cesan! Esto es serio.",
                    "Mi corazón late al ritmo de las alarmas.",
                    "¿Dónde está la salida? Necesito escapar.",
                    "Los sistemas fallan uno tras otro.",
                    "¡No puedo fallar ahora, demasiado en juego!"
                ],
                'victory': [
                    "¡Lo logré! El sistema es seguro nuevamente.",
                    "Victoria para los usuarios comunes. ¡Éxito!",
                    "Protección activada. Mis datos están a salvo.",
                    "¡Operación completada! Sistema estabilizado.",
                    "¡Crisis evitada! Todo bajo control.",
                    "Finalmente puedo respirar tranquilo.",
                    "Sabía que podía hacerlo si me concentraba.",
                    "Mi información está protegida al fin.",
                    "¡Superé todos los obstáculos!",
                    "La perseverancia rindió frutos.",
                    "¡Increíble! Todo salió mejor de lo esperado.",
                    "La seguridad ha sido restaurada por completo.",
                    "Mis datos están a salvo, misión cumplida.",
                    "¡Éxito total! Aprendí mucho en el proceso.",
                    "El sistema respira aliviado, y yo también."
                ],
                'action': [
                    "Ejecutando protocolo de seguridad...",
                    "Activando medidas defensivas.",
                    "Analizando posibles amenazas...",
                    "Implementando contramedidas.",
                    "Reforzando protecciones del sistema.",
                    "Tomando acción para protegerme.",
                    "Debo ser estratégico en este momento.",
                    "Cada segundo cuenta ahora.",
                    "Aplicando solución rápida.",
                    "Iniciando secuencia de defensa.",
                    "Configurando parámetros de emergencia.",
                    "Ejecutando procedimiento crítico.",
                    "Activando todos los protocolos.",
                    "No hay tiempo que perder, acción inmediata.",
                    "Implementando plan de contingencia."
                ]
            },
            'hacker': {
                'neutral': [
                    "Analizando vectores de ataque... Firewalls detectados.",
                    "Escaneando vulnerabilidades del sistema.",
                    "Monitoreando tráfico de red sospechoso.",
                    "Preparando herramientas de análisis.",
                    "Evaluando puntos de entrada potenciales.",
                    "El código revela sus secretos...",
                    "Arquitectura del sistema mapeada.",
                    "Buscando exploits conocidos en la base de datos.",
                    "Analizando patrones de seguridad.",
                    "Recopilando información crítica.",
                    "Descompilando módulos sospechosos.",
                    "Trazando rutas de acceso alternativas.",
                    "Verificando integridad del kernel.",
                    "Monitorizando procesos en segundo plano.",
                    "Evaluando superficie de ataque disponible."
                ],
                'stressed': [
                    "¡Contramedidas activadas! El sistema se defiende...",
                    "Alerta: Múltiples amenazas detectadas.",
                    "¡Casi me detectan! Activando evasión...",
                    "La resistencia del sistema es mayor de lo esperado.",
                    "¡Firewalls reforzados! Necesito otra estrategia.",
                    "IDS activo, cambiando de táctica.",
                    "El honeypot casi me atrapa.",
                    "Sistema de defensa más robusto de lo anticipado.",
                    "¡Rastreadores en mi cola!",
                    "Necesito replantear mi enfoque.",
                    "¡El sistema contraataca! Defensas automáticas activas.",
                    "Múltiples capas de seguridad, esto se complica.",
                    "¡Alerta! He sido marcado como amenaza.",
                    "Los protocolos de defensa son agresivos.",
                    "¡Código de evasión fallando! Plan B necesario."
                ],
                'victory': [
                    "¡Sistemas expuestos! Justicia digital servida.",
                    "La verdad sale a la luz. Misión cumplida.",
                    "Vulnerabilidades parchadas. Sistema seguro.",
                    "¡Éxito! Los datos están protegidos.",
                    "Amenaza neutralizada. Trabajo completado.",
                    "Exploit ejecutado perfectamente.",
                    "El sistema está ahora fortificado.",
                    "Objetivo alcanzado sin dejar rastros.",
                    "La seguridad ha sido restaurada.",
                    "Protocolo de protección implementado.",
                    "¡Brecha sellada! El sistema respira aliviado.",
                    "Código malicioso eliminado por completo.",
                    "Infraestructura asegurada, trabajo impecable.",
                    "¡Victoria técnica! Todos los sistemas verdes.",
                    "El enemigo digital ha sido derrotado."
                ],
                'action': [
                    "Desplegando exploits...",
                    "Infiltrando sistemas de seguridad.",
                    "Ejecutando scripts de penetración.",
                    "Analizando código fuente en busca de fallos.",
                    "Probando vectores de ataque alternativos.",
                    "Bypasseando autenticación...",
                    "Inyectando payload personalizado.",
                    "Escalando privilegios en el sistema.",
                    "Ejecutando exploit de día cero.",
                    "Aplicando técnicas de ingeniería inversa.",
                    "Compilando código de acceso forzado.",
                    "Ejecutando ataque de diccionario optimizado.",
                    "Inyectando SQL en puntos vulnerables.",
                    "Desactivando sistemas de monitoreo.",
                    "Activando puertas traseras estratégicas."
                ]
            },
            'cyberdelincuente': {
                'neutral': [
                    "Operando en las sombras... Rastreo evadido.",
                    "Movimientos sigilosos activados.",
                    "Navegando por los canales oscuros.",
                    "Preparando el próximo movimiento.",
                    "Evaluando riesgos y recompensas.",
                    "Las sombras digitales me protegen.",
                    "Invisibilidad garantizada por ahora.",
                    "El anonimato es mi mejor arma.",
                    "Sin rastros, sin pruebas.",
                    "El fantasma digital continúa su obra.",
                    "Deslizándome entre los bits sin dejar huella.",
                    "El silencio digital es mi aliado.",
                    "Observando desde la oscuridad.",
                    "Preparando el siguiente asalto silencioso.",
                    "La red es mi territorio de caza."
                ],
                'stressed': [
                    "¡Casi me detectan! Activando protocolos de escape...",
                    "Las defensas son más fuertes de lo esperado.",
                    "¡Alerta! Rastreadores activados en el sector.",
                    "Necesito cubrir mis huellas rápidamente.",
                    "¡Situación crítica! Plan B activado.",
                    "El cerco se cierra, debo ser más astuto.",
                    "Sistemas de rastreo a full capacidad.",
                    "Momento de desaparecer del radar.",
                    "La cacería ha comenzado.",
                    "Necesito una ruta de escape inmediata.",
                    "¡Marcado! Todos los sistemas me buscan.",
                    "La red se cierra a mi alrededor.",
                    "¡Trampas digitales por todas partes!",
                    "El sistema huele mi presencia.",
                    "¡Alerta máxima! Modo evasión total."
                ],
                'victory': [
                    "¡El botín es mío! Operación completada con éxito.",
                    "Objetivo alcanzado. Recursos obtenidos.",
                    "¡Éxito total! Sin dejar rastros.",
                    "Misión cumplida. Retirándose del área.",
                    "¡Tesoro adquirido! Operación impecable.",
                    "Payload entregado, extracción exitosa.",
                    "El fantasma digital golpea de nuevo.",
                    "Perfecto. Como si nunca hubiera estado aquí.",
                    "Otro trabajo limpio para mi registro.",
                    "Las sombras celebran mi victoria.",
                    "¡Recompensa obtenida! Desapareciendo en la noche.",
                    "Objetivo cumplido, identidad intacta.",
                    "La red olvidará mi paso pronto.",
                    "¡Éxito silencioso! Nadie supo que estuve aquí.",
                    "Tesoro digital seguro, misión terminada."
                ],
                'action': [
                    "Ejecutando procedimientos de infiltración...",
                    "Instalando backdoors silenciosos.",
                    "Exfiltrando datos sensibles...",
                    "Activando medidas de evasión avanzadas.",
                    "Manipulando sistemas de registro.",
                    "Borrando huellas digitales...",
                    "Estableciendo punto de acceso persistente.",
                    "Operación fantasma en progreso.",
                    "Despliegue de malware personalizado.",
                    "Ejecutando protocolo de extracción.",
                    "Silenciando alarmas del sistema.",
                    "Creando identidades digitales falsas.",
                    "Envenenando caché del sistema.",
                    "Redirigiendo tráfico de vigilancia.",
                    "Activando cortinas de humo digitales."
                ]
            }
        }
        
        # Mapeo inteligente de emociones mejorado
        situation_lower = situation.lower()
        if any(word in situation_lower for word in ['éxito', 'exito', 'victoria', 'completado', 'logrado', 'ganado', 'triunfo']):
            emotion_key = 'victory'
        elif any(word in situation_lower for word in ['peligro', 'amenaza', 'estrés', 'estres', 'problema', 'error', 'fallo', 'detectado', 'pérdida', 'pérdida']):
            emotion_key = 'stressed'
        elif any(word in situation_lower for word in ['acción', 'accion', 'decisión', 'opción', 'ejecutar', 'proceder', 'actuar']):
            emotion_key = 'action'
        else:
            emotion_key = emotion if emotion in ['neutral', 'stressed', 'victory', 'action'] else 'neutral'
        
        # Obtener diálogos disponibles
        character_dialogs = dialogs.get(character_type, dialogs['usuario'])
        available_dialogs = character_dialogs.get(emotion_key, character_dialogs['neutral'])
        
        return random.choice(available_dialogs)
    
    def generate_event_description(self, event_type: str) -> str:
        """Genera descripciones narrativas para eventos globales - MEJORADO"""
        if self.gemini_enabled:
            try:
                prompt = f"""Genera una descripción CORTA (máximo 15 palabras) para un evento en un juego cyberpunk:

Tipo de evento: {event_type}

La descripción debe ser DRAMÁTICA y INMERSIVA.
NO uses comillas. Solo la descripción directa.

Tu descripción:"""
                
                response = self.model.generate_content(prompt)
                if response and response.text:
                    return response.text.strip().replace('"', '').replace("'", "")
            except:
                pass
        
        # Fallback local mejorado
        descriptions = {
            'security_alert': '🚨 ALERTA CRÍTICA: Sistemas de defensa activados en toda la red',
            'system_vulnerability': '🔓 VULNERABILIDAD CRÍTICA: Brecha de seguridad masiva detectada',
            'data_corruption': '💾 COLAPSO DE DATOS: Corrupción sistémica afectando núcleos',
            'network_boost': '📡 OPTIMIZACIÓN GLOBAL: Ancho de banda aumentado significativamente',
            'virus_outbreak': '🦠 BROTE VIRAL: Malware de propagación rápida detectado',
            'firewall_breach': '🛡️ BRECHA DEFENSIVA: Sistemas de protección comprometidos',
            'encryption_failure': '🔒 FALLO ENCRIPTACIÓN: Protocolos de seguridad colapsados'
        }
        return descriptions.get(event_type, 'Evento desconocido en el sistema')
    
    def generate_ending_dialog(self, character_type: str, won: bool, stats: dict) -> str:
        """Genera diálogo final del personaje - MEJORADO"""
        if self.gemini_enabled:
            try:
                result = "victoria" if won else "derrota"
                prompt = f"""Eres un {character_type} en un juego cyberpunk que acaba de experimentar una {result}.

Estadísticas:
- Progreso: {stats.get('progress', 0)}%
- Errores: {stats.get('errors', 0)}
- Tiempo: {stats.get('time', 0)} segundos

Genera UN diálogo de cierre CORTO (máximo 25 palabras) que refleje la experiencia del personaje.
El tono debe ser {'triunfante' if won else 'reflexivo'}.
NO uses comillas. Solo el diálogo directo en ESPAÑOL.

Tu diálogo:"""
                
                response = self.model.generate_content(prompt)
                if response and response.text:
                    return response.text.strip().replace('"', '').replace("'", "")
            except:
                pass
        
        # Fallback local mejorado
        if won:
            endings = {
                'usuario': "Lo logré... mi información está segura. Nunca más subestimaré la importancia de la privacidad digital.",
                'hacker': "Misión cumplida. El sistema está más seguro ahora. La justicia digital prevalece una vez más.",
                'cyberdelincuente': "Objetivo completado sin rastros. Otro trabajo perfecto en las sombras digitales. Hasta la próxima."
            }
        else:
            endings = {
                'usuario': "No pude proteger mis datos... pero aprendí una lección valiosa sobre seguridad en la red.",
                'hacker': "El sistema era más robusto de lo esperado. Regresaré con mejores herramientas y más conocimiento.",
                'cyberdelincuente': "Me detectaron esta vez... pero un fantasma siempre encuentra otra sombra donde esconderse."
            }
        
        return endings.get(character_type, "La batalla en el ciberespacio continúa...")