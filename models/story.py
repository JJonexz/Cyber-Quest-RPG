# ============================================================================
# ARCHIVO: models/story.py
# DESCRIPCIÓN: Sistema de generación de historias dinámicas con IA.
#              Crea narrativas únicas para cada partida con eventos aleatorios.
# ============================================================================

import random
from typing import Dict, List

class StoryGenerator:
    """Generador de historias dinámicas para cada partida"""
    
    def __init__(self):
        self.story_templates = self._load_story_templates()
        self.current_story = None
        
    def _load_story_templates(self) -> Dict:
        """Carga plantillas base para generar historias"""
        return {
            'scenarios': [
                {
                    'name': 'La Amenaza Corporativa',
                    'context': 'Una megacorporación está implementando un sistema de vigilancia masiva',
                    'locations': ['Data Center', 'Oficinas Ejecutivas', 'Laboratorio de Seguridad', 'Red Corporativa'],
                    'objectives': {
                        'usuario': 'Proteger tus datos personales y escapar del sistema',
                        'hacker': 'Exponer las vulnerabilidades y alertar al público',
                        'cyberdelincuente': 'Robar información valiosa sin ser detectado'
                    }
                },
                {
                    'name': 'El Virus Desconocido',
                    'context': 'Un malware de origen desconocido está infectando sistemas críticos',
                    'locations': ['Hospital Central', 'Base de Datos Nacional', 'Servidor de Energía', 'Centro de Control'],
                    'objectives': {
                        'usuario': 'Recuperar tus archivos y proteger tu información',
                        'hacker': 'Neutralizar el virus y restaurar los sistemas',
                        'cyberdelincuente': 'Aprovechar el caos para infiltrarte en sistemas protegidos'
                    }
                },
                {
                    'name': 'La Red Oscura',
                    'context': 'Una organización criminal controla una vasta red de información robada',
                    'locations': ['Mercado Negro', 'Servidor Proxy', 'Nodo de Distribución', 'Base de Operaciones'],
                    'objectives': {
                        'usuario': 'Encontrar y eliminar tu información del mercado negro',
                        'hacker': 'Desmantelar la red y reportar a las autoridades',
                        'cyberdelincuente': 'Tomar control de la red para tu beneficio'
                    }
                },
                {
                    'name': 'Ataque a la Infraestructura',
                    'context': 'Sistemas críticos de la ciudad están siendo comprometidos',
                    'locations': ['Central Eléctrica', 'Sistema de Tráfico', 'Red de Comunicaciones', 'Bunker de Seguridad'],
                    'objectives': {
                        'usuario': 'Mantener tus servicios funcionando y pedir ayuda',
                        'hacker': 'Defender la infraestructura y detener el ataque',
                        'cyberdelincuente': 'Extorsionar a la ciudad con el control de los sistemas'
                    }
                }
            ],
            'events': [
                'Un firewall inesperado bloquea tu progreso',
                'Detectas una presencia enemiga en la red',
                'Encuentras una vulnerabilidad crítica',
                'El sistema activa protocolos de emergencia',
                'Recibes una comunicación anónima',
                'Descubres un archivo encriptado',
                'Se activa un rastreador de intrusos',
                'Encuentras un backdoor oculto'
            ],
            'consequences': [
                'Tu actividad ha sido registrada',
                'Has ganado tiempo valioso',
                'Alertaste al sistema de seguridad',
                'Obtuviste información crítica',
                'Perdiste el rastro del objetivo',
                'Creaste una distracción efectiva'
            ]
        }
    
    def generate_new_story(self, character_type: str) -> Dict:
        """Genera una historia única para cada partida"""
        scenario = random.choice(self.story_templates['scenarios'])
        
        # Generar secuencia de eventos
        num_stages = random.randint(4, 6)
        story_stages = []
        
        for i in range(num_stages):
            location = random.choice(scenario['locations'])
            event = random.choice(self.story_templates['events'])
            
            # Generar opciones basadas en el personaje
            options = self._generate_options(character_type, i, num_stages)
            
            story_stages.append({
                'stage': i + 1,
                'location': location,
                'event': event,
                'description': self._generate_description(scenario, location, event, i),
                'options': options
            })
        
        self.current_story = {
            'scenario': scenario,
            'stages': story_stages,
            'character': character_type,
            'objective': scenario['objectives'][character_type]
        }
        
        return self.current_story
    
    def _generate_description(self, scenario, location, event, stage_num):
        """Genera descripción narrativa para cada etapa"""
        descriptions = [
            f"Te encuentras en {location}. {event}. La tensión aumenta mientras {scenario['context'].lower()}.",
            f"Llegas a {location}. De repente, {event.lower()}. Debes actuar rápido.",
            f"En {location}, observas que {event.lower()}. Cada decisión cuenta ahora.",
            f"El sistema te lleva a {location}. {event}. El tiempo corre en tu contra.",
            f"Navegando hacia {location}, descubres que {event.lower()}. ¿Qué harás?"
        ]
        return random.choice(descriptions)
    
    def _generate_options(self, character_type: str, stage: int, total_stages: int) -> List[Dict]:
        """Genera opciones contextuales según el personaje y la etapa"""
        options_db = {
            'usuario': {
                'early': [
                    {'text': 'Buscar ayuda de seguridad', 'risk': 'bajo', 'time': 1, 'success': 75},
                    {'text': 'Intentar resolver solo', 'risk': 'medio', 'time': 2, 'success': 50},
                    {'text': 'Desconectarte temporalmente', 'risk': 'bajo', 'time': 1, 'success': 60}
                ],
                'mid': [
                    {'text': 'Seguir las instrucciones de seguridad', 'risk': 'bajo', 'time': 1, 'success': 70},
                    {'text': 'Explorar opciones alternativas', 'risk': 'medio', 'time': 2, 'success': 55},
                    {'text': 'Contactar con autoridades', 'risk': 'bajo', 'time': 2, 'success': 65}
                ],
                'late': [
                    {'text': 'Aplicar medidas de protección', 'risk': 'bajo', 'time': 1, 'success': 80},
                    {'text': 'Evacuar el sistema', 'risk': 'medio', 'time': 1, 'success': 70},
                    {'text': 'Confiar en los expertos', 'risk': 'bajo', 'time': 2, 'success': 75}
                ]
            },
            'hacker': {
                'early': [
                    {'text': 'Escanear vulnerabilidades', 'risk': 'medio', 'time': 2, 'success': 70},
                    {'text': 'Implementar contramedidas', 'risk': 'medio', 'time': 2, 'success': 65},
                    {'text': 'Analizar el código fuente', 'risk': 'alto', 'time': 3, 'success': 80}
                ],
                'mid': [
                    {'text': 'Desplegar herramientas de pentesting', 'risk': 'medio', 'time': 2, 'success': 70},
                    {'text': 'Explotar vulnerabilidad encontrada', 'risk': 'alto', 'time': 2, 'success': 75},
                    {'text': 'Crear un bypass de seguridad', 'risk': 'medio', 'time': 3, 'success': 65}
                ],
                'late': [
                    {'text': 'Ejecutar exploit definitivo', 'risk': 'alto', 'time': 2, 'success': 80},
                    {'text': 'Reportar hallazgos', 'risk': 'bajo', 'time': 1, 'success': 70},
                    {'text': 'Neutralizar la amenaza', 'risk': 'medio', 'time': 2, 'success': 75}
                ]
            },
            'cyberdelincuente': {
                'early': [
                    {'text': 'Infiltrarse sigilosamente', 'risk': 'alto', 'time': 3, 'success': 60},
                    {'text': 'Usar técnicas de evasión avanzadas', 'risk': 'alto', 'time': 3, 'success': 65},
                    {'text': 'Crear distracción en otro sector', 'risk': 'medio', 'time': 2, 'success': 55}
                ],
                'mid': [
                    {'text': 'Instalar backdoor persistente', 'risk': 'alto', 'time': 3, 'success': 60},
                    {'text': 'Exfiltrar datos valiosos', 'risk': 'alto', 'time': 3, 'success': 65},
                    {'text': 'Borrar rastros de tu presencia', 'risk': 'alto', 'time': 2, 'success': 50}
                ],
                'late': [
                    {'text': 'Ejecutar el golpe final', 'risk': 'alto', 'time': 3, 'success': 70},
                    {'text': 'Establecer ruta de escape', 'risk': 'alto', 'time': 2, 'success': 60},
                    {'text': 'Maximizar ganancias antes de salir', 'risk': 'alto', 'time': 3, 'success': 65}
                ]
            }
        }
        
        # Determinar fase del juego
        if stage < total_stages * 0.33:
            phase = 'early'
        elif stage < total_stages * 0.66:
            phase = 'mid'
        else:
            phase = 'late'
        
        return options_db[character_type][phase]

