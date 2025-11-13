# ============================================================================
# ARCHIVO: models/story.py
# DESCRIPCIÓN: Sistema de generación de historias dinámicas con IA mejorado.
# Historias realistas de ciberseguridad con contexto persistente y
# correlación optimizada entre eventos y opciones.
# ============================================================================

import random
from typing import Dict, List, Any, Optional, Tuple


class StoryGenerator:
    """Generador de historias de ciberseguridad con narrativa coherente y contextual."""
    
    def __init__(self, seed: Optional[int] = None):
        if seed is not None:
            random.seed(seed)
        self.story_templates = self._load_story_templates()
        self.current_story = None
        self.stage_index = 0
        self.narrative_memory = []  # Memoria de eventos pasados para contexto

    def _load_story_templates(self) -> Dict[str, Any]:
        """Carga plantillas base optimizadas por rol y dificultad."""
        return {
            'scenarios': [
                # USUARIO: Empleado defendiéndose de amenazas
                {
                    'id': 'usuario_oficina',
                    'name': 'Supervivencia Digital en la Oficina',
                    'context': 'Eres un empleado que debe identificar y responder correctamente a intentos de phishing, dispositivos sospechosos, y técnicas de ingeniería social dirigidas a ti y tus compañeros.',
                    'locations': [
                        {'name': 'Escritorio', 'connections': ['Sala de Reuniones', 'Cafetería']},
                        {'name': 'Sala de Reuniones', 'connections': ['Escritorio', 'Recepción']},
                        {'name': 'Cafetería', 'connections': ['Escritorio', 'Estacionamiento']},
                        {'name': 'Recepción', 'connections': ['Sala de Reuniones', 'Estacionamiento']},
                        {'name': 'Estacionamiento', 'connections': ['Cafetería', 'Recepción']}
                    ],
                    'objectives': {
                        'usuario': 'Proteger tus credenciales y datos personales, reportando amenazas sin caer en trampas.',
                        'hacker': 'N/A',
                        'cyberdelincuente': 'N/A'
                    }
                },
                # HACKER ÉTICO: Defensor de la empresa
                {
                    'id': 'hacker_empresa',
                    'name': 'Defensa Activa Corporativa',
                    'context': 'Como analista de seguridad, debes detectar amenazas en tiempo real, corregir vulnerabilidades, educar a empleados y responder a incidentes antes de que escalen.',
                    'locations': [
                        {'name': 'SOC (Centro de Operaciones)', 'connections': ['Sala de Servidores', 'Oficina TI']},
                        {'name': 'Sala de Servidores', 'connections': ['SOC (Centro de Operaciones)', 'Área de Empleados']},
                        {'name': 'Oficina TI', 'connections': ['SOC (Centro de Operaciones)', 'Área de Empleados']},
                        {'name': 'Área de Empleados', 'connections': ['Oficina TI', 'Sala de Servidores']},
                        {'name': 'Perímetro de Red', 'connections': ['SOC (Centro de Operaciones)', 'Sala de Servidores']}
                    ],
                    'objectives': {
                        'usuario': 'N/A',
                        'hacker': 'Prevenir brechas de seguridad, detectar actividad maliciosa y responder efectivamente a incidentes.',
                        'cyberdelincuente': 'N/A'
                    }
                },
                # CIBERDELINCUENTE: Atacante externo
                {
                    'id': 'ciberdelincuente_ataque',
                    'name': 'Operación de Intrusión Corporativa',
                    'context': 'Como atacante externo, tu objetivo es comprometer la empresa mediante phishing dirigido, exploits, ingeniería social y evasión de controles de seguridad.',
                    'locations': [
                        {'name': 'Infraestructura Externa', 'connections': ['Perímetro WiFi', 'Zona de Reconocimiento']},
                        {'name': 'Perímetro WiFi', 'connections': ['Infraestructura Externa', 'Punto de Acceso Físico']},
                        {'name': 'Zona de Reconocimiento', 'connections': ['Infraestructura Externa', 'Punto de Acceso Físico']},
                        {'name': 'Punto de Acceso Físico', 'connections': ['Perímetro WiFi', 'Zona de Reconocimiento']},
                        {'name': 'Red Comprometida', 'connections': ['Punto de Acceso Físico', 'Infraestructura Externa']}
                    ],
                    'objectives': {
                        'usuario': 'N/A',
                        'hacker': 'N/A',
                        'cyberdelincuente': 'Obtener acceso inicial, escalar privilegios y exfiltrar información valiosa sin ser detectado.'
                    }
                }
            ],
            
            # EVENTOS MEJORADOS: Más realistas y específicos
            'events': [
                # === EVENTOS DE USUARIO ===
                {'text': 'Recibes un correo urgente del "CEO" pidiendo transferir fondos inmediatamente', 
                 'effect': {'alert_level': +2}, 'tags': ['phishing', 'correo', 'urgencia', 'usuario'], 'severity': 'high'},
                
                {'text': 'Encuentras una memoria USB con etiqueta "Nóminas 2024" en el baño', 
                 'effect': {'pistas': +1}, 'tags': ['usb', 'physical', 'usuario'], 'severity': 'medium'},
                
                {'text': 'Un "técnico de soporte" llama pidiendo tu contraseña para "mantenimiento del sistema"', 
                 'effect': {'alert_level': +2}, 'tags': ['vishing', 'social', 'credentials', 'usuario'], 'severity': 'high'},
                
                {'text': 'Tu navegador muestra una alerta de seguridad de "Microsoft" pidiendo instalar una actualización urgente', 
                 'effect': {'alert_level': +1}, 'tags': ['phishing', 'malware', 'usuario'], 'severity': 'medium'},
                
                {'text': 'Recibes un mensaje de LinkedIn de un reclutador con un "test de habilidades" adjunto', 
                 'effect': {'pistas': +1}, 'tags': ['phishing', 'social', 'adjunto', 'usuario'], 'severity': 'medium'},
                
                {'text': 'Tu jefe te pide por WhatsApp compartir el acceso VPN "solo por hoy"', 
                 'effect': {'alert_level': +1}, 'tags': ['social', 'credentials', 'usuario'], 'severity': 'high'},
                
                # === EVENTOS DE HACKER ÉTICO ===
                {'text': 'El IDS detecta 50+ intentos de login fallidos desde una IP en Rusia en los últimos 5 minutos', 
                 'effect': {'alert_level': +2, 'pistas': +1}, 'tags': ['bruteforce', 'logs', 'detection', 'hacker'], 'severity': 'high'},
                
                {'text': 'Un empleado de finanzas reporta que no puede acceder a sus archivos; todos tienen extensión .locked', 
                 'effect': {'alert_level': +3}, 'tags': ['ransomware', 'incident', 'hacker'], 'severity': 'critical'},
                
                {'text': 'Notas tráfico saliente masivo (2GB) desde una estación de trabajo a las 3 AM', 
                 'effect': {'alert_level': +2, 'pistas': +2}, 'tags': ['exfiltration', 'logs', 'anomaly', 'hacker'], 'severity': 'critical'},
                
                {'text': 'El escáner de vulnerabilidades reporta un servidor con SMBv1 activo y puertos administrativos expuestos', 
                 'effect': {'pistas': +1}, 'tags': ['vulnerability', 'scan', 'hacker'], 'severity': 'medium'},
                
                {'text': 'Recibes 20 tickets de empleados que cayeron en el mismo correo de phishing', 
                 'effect': {'alert_level': +2}, 'tags': ['phishing', 'incident', 'response', 'hacker'], 'severity': 'high'},
                
                {'text': 'Encuentras un script PowerShell sospechoso programado en el Inicio de un servidor crítico', 
                 'effect': {'alert_level': +2, 'pistas': +1}, 'tags': ['malware', 'persistence', 'forensics', 'hacker'], 'severity': 'high'},
                
                {'text': 'Un empleado conectó su laptop personal a la red corporativa sin autorización', 
                 'effect': {'alert_level': +1}, 'tags': ['policy', 'physical', 'hacker'], 'severity': 'low'},
                
                # === EVENTOS DE CIBERDELINCUENTE ===
                {'text': 'Consigues un listado de 200 emails corporativos mediante scraping de LinkedIn', 
                 'effect': {'pistas': +1}, 'tags': ['recon', 'osint', 'cyberdelincuente'], 'severity': 'low'},
                
                {'text': 'Detectas un servidor web desactualizado con vulnerabilidad de RCE sin parchear', 
                 'effect': {'pistas': +2}, 'tags': ['vulnerability', 'exploit', 'cyberdelincuente'], 'severity': 'high'},
                
                {'text': 'Clonas el portal de Office365 de la empresa para capturar credenciales', 
                 'effect': {'pistas': +1}, 'tags': ['phishing', 'clone', 'credentials', 'cyberdelincuente'], 'severity': 'medium'},
                
                {'text': 'Logras acceso inicial mediante una cuenta de practicante con contraseña débil (usuario:123456)', 
                 'effect': {'alert_level': +1, 'compromised_hosts': +1}, 'tags': ['bruteforce', 'credentials', 'cyberdelincuente'], 'severity': 'high'},
                
                {'text': 'Despliegas un USB con payload Rubber Ducky en el estacionamiento de la empresa', 
                 'effect': {'pistas': +1}, 'tags': ['usb', 'physical', 'payload', 'cyberdelincuente'], 'severity': 'medium'},
                
                {'text': 'Identificas backups sin cifrar accesibles desde la red interna', 
                 'effect': {'pistas': +2}, 'tags': ['recon', 'data', 'cyberdelincuente'], 'severity': 'high'},
                
                {'text': 'Consigues moverte lateralmente a un controlador de dominio mediante Pass-the-Hash', 
                 'effect': {'alert_level': +2, 'compromised_hosts': +1}, 'tags': ['lateral', 'privilege', 'cyberdelincuente'], 'severity': 'critical'},
            ],
            
            'consequences': [
                'Se generaron alertas en el SIEM que indican acceso no autorizado.',
                'El equipo de respuesta a incidentes inició protocolo de contención.',
                'Se logró detener una exfiltración de datos a tiempo.',
                'El atacante estableció persistencia mediante un backdoor.',
                'Varios empleados comprometieron credenciales corporativas.',
                'Se activó el plan de recuperación de desastres.',
                'Forense digital confirmó compromiso de múltiples sistemas.',
                'Se notificó al equipo legal sobre posible brecha de datos.'
            ]
        }

    def _create_thread(self, scenario: Dict[str, Any], character_type: str) -> Tuple[str, str, str]:
        """Crea narrativa base coherente por personaje."""
        base_goal = scenario['objectives'].get(character_type, 'N/A')
        
        if character_type == 'usuario':
            goal = base_goal
            key_item = 'Token de autenticación MFA y conocimiento de políticas de seguridad'
            antagonist = 'Campaña de phishing dirigido y ataques de ingeniería social'
            
        elif character_type == 'hacker':
            goal = base_goal
            key_item = 'Acceso a logs, herramientas de análisis forense y autoridad para aislar sistemas'
            antagonist = 'Atacante APT persistente explotando errores humanos y configuraciones débiles'
            
        else:  # cyberdelincuente
            goal = base_goal
            key_item = 'Infraestructura de comando y control (C2) y arsenal de exploits'
            antagonist = 'Equipo de respuesta a incidentes y controles de seguridad multicapa'
            
        return goal, antagonist, key_item

    def _choose_event_by_state(self, state: Dict[str, Any], stage_num: int = 0) -> Dict[str, Any]:
        """Selecciona eventos coherentes con el estado actual y fase narrativa."""
        events = self.story_templates['events']
        character = self.current_story.get('character', 'usuario') if self.current_story else 'usuario'
        
        # Mapeo de caracteres para asegurar consistencia
        char_tag_map = {
            'usuario': 'usuario',
            'hacker': 'hacker',
            'cyberdelincuente': 'cyberdelincuente'
        }
        char_tag = char_tag_map.get(character, 'usuario')
        
        # Filtrar por personaje
        relevant_events = [e for e in events if char_tag in e.get('tags', [])]
        if not relevant_events:
            # Si no hay eventos específicos, usar todos como fallback
            relevant_events = events
            print(f"⚠️ Warning: No se encontraron eventos para '{character}', usando todos los eventos.")
        
        # Sistema de pesos basado en contexto
        weighted = []
        alert = state.get('alert_level', 0)
        pistas = state.get('pistas', 0)
        compromised = state.get('compromised_hosts', 0)
        
        # Determinar fase narrativa
        if not self.current_story or not self.current_story.get('stages'):
            total_stages = 6  # default
        else:
            total_stages = len(self.current_story.get('stages', []))
        
        fraction = stage_num / max(1, total_stages - 1) if total_stages > 1 else 0
        
        for event in relevant_events:
            weight = 1
            severity = event.get('severity', 'medium')
            tags = event.get('tags', [])
            
            # FASE EARLY (0-33%): Introducción y reconocimiento
            if fraction < 0.33:
                if 'recon' in tags or 'osint' in tags:
                    weight = 4
                elif 'phishing' in tags or 'social' in tags:
                    weight = 3
                elif severity == 'low' or severity == 'medium':
                    weight = 2
                    
            # FASE MID (33-66%): Escalada y acción
            elif fraction < 0.66:
                if 'exploit' in tags or 'lateral' in tags or 'incident' in tags:
                    weight = 4
                elif 'malware' in tags or 'vulnerability' in tags:
                    weight = 3
                elif severity == 'medium' or severity == 'high':
                    weight = 2
                    
            # FASE LATE (66-100%): Clímax y resolución
            else:
                if 'ransomware' in tags or 'exfiltration' in tags or 'critical' in tags:
                    weight = 4
                elif 'privilege' in tags or 'persistence' in tags:
                    weight = 3
                elif severity == 'high' or severity == 'critical':
                    weight = 2
            
            # Ajustes por estado actual
            if alert >= 3 and severity == 'critical':
                weight *= 2
            if alert == 0 and severity == 'low':
                weight *= 2
            if pistas == 0 and 'pistas' in str(event.get('effect', {})):
                weight *= 1.5
            if compromised > 0 and ('forensics' in tags or 'response' in tags):
                weight *= 1.5
                
            weighted.extend([event] * int(weight))
        
        # Asegurar que weighted no esté vacío
        if not weighted:
            print(f"⚠️ Warning: No hay eventos ponderados para '{character}', usando evento aleatorio.")
            return random.choice(relevant_events) if relevant_events else random.choice(events)
        
        return random.choice(weighted)

    def _choose_location(self, current_location: str, scenario: Dict[str, Any]) -> str:
        """Elige siguiente ubicación con preferencia por conexiones lógicas."""
        loc_map = {loc['name']: loc for loc in scenario['locations']}
        
        if current_location not in loc_map:
            return scenario['locations'][0]['name']
        
        connections = loc_map[current_location]['connections']
        if not connections:
            return random.choice([loc['name'] for loc in scenario['locations']])
        
        # 90% de probabilidad de moverse a ubicación conectada
        return random.choice(connections) if random.random() < 0.9 else random.choice([loc['name'] for loc in scenario['locations']])

    def _apply_event_effects(self, state: Dict[str, Any], event: Dict[str, Any]) -> Dict[str, Any]:
        """Aplica efectos de eventos al estado."""
        new_state = state.copy()
        effect = event.get('effect', {}) or {}
        
        for key, delta in effect.items():
            if key in new_state and isinstance(new_state[key], int):
                new_state[key] = max(0, new_state[key] + int(delta))
            else:
                new_state[key] = delta
                
        return new_state

    def _apply_option_effects(self, state: Dict[str, Any], option: Dict[str, Any], success: bool) -> Dict[str, Any]:
        """Aplica efectos de decisión del jugador."""
        new_state = state.copy()
        effects = option.get('effect_on_state', {}) or {}
        
        if isinstance(effects, dict) and ('success' in effects or 'failure' in effects):
            chosen_effect = effects.get('success' if success else 'failure', {})
        else:
            chosen_effect = effects
        
        for key, delta in chosen_effect.items():
            if key in new_state and isinstance(new_state[key], int):
                new_state[key] = max(0, new_state[key] + int(delta))
            else:
                new_state[key] = chosen_effect[key]
                
        return new_state

    def _generate_description(self, scenario: Dict[str, Any], location: str, event: Dict[str, Any], 
                            stage_num: int, state: Dict[str, Any], goal: str, antagonist: str, 
                            key_item: str, show_objective: bool = False) -> str:
        """Genera descripción narrativa contextual con memoria de eventos previos."""
        parts = []
        
        # Ubicación actual
        parts.append(f"📍 **{location}**")
        
        # Evento principal con contexto
        parts.append(f"\n{event['text']}")
        
        # Información de estado crítico
        alert = state.get('alert_level', 0)
        if alert >= 3:
            parts.append("\n⚠️ **ALERTA CRÍTICA**: La situación requiere acción inmediata para evitar daños mayores.")
        elif alert == 2:
            parts.append("\n⚠️ **Alerta Alta**: Actividad sospechosa confirmada. Procede con cautela.")
        elif alert == 1:
            parts.append("\n⚡ Vigilancia aumentada: Se detectaron anomalías menores.")
        
        # Pistas acumuladas
        pistas = state.get('pistas', 0)
        if pistas >= 3:
            parts.append(f"\n🔍 Tienes evidencia sólida ({pistas} indicadores) para tomar decisiones informadas.")
        elif pistas > 0:
            parts.append(f"\n🔍 Has reunido {pistas} pista(s) que pueden ser útiles.")
        
        # Objetivo (solo al inicio)
        if show_objective:
            parts.append(f"\n🎯 **Objetivo**: {goal}")
        
        # Memoria narrativa (referencia a eventos pasados para coherencia)
        if len(self.narrative_memory) > 0 and stage_num > 0:
            last_event = self.narrative_memory[-1]
            if 'phishing' in last_event and 'phishing' in event.get('tags', []):
                parts.append("\n💭 Este incidente parece relacionado con la campaña anterior...")
        
        parts.append("\n\n**¿Cuál es tu siguiente movimiento?**")
        
        return "".join(parts)

    def _base_options_catalog(self) -> Dict[str, Dict[str, List[Dict[str, Any]]]]:
        """Catálogo optimizado de opciones con mayor realismo y variedad."""
        return {
            'usuario': {
                'early': [
                    {
                        'text': 'Verificar remitente (header completo), no abrir enlaces y reportar a seguridad',
                        'tags': ['phishing', 'correo', 'urgencia'],
                        'risk': 'bajo', 'time': 1, 'success': 90,
                        'effect_on_state': {'success': {'pistas': +1, 'alert_level': -1}, 'failure': {'alert_level': +1}},
                        'outcome_text': {
                            'success': 'Reportaste el correo. El equipo de seguridad confirmó que era phishing y bloqueó al remitente.',
                            'failure': 'Tu reporte llegó tarde y otros empleados ya abrieron el enlace malicioso.'
                        }
                    },
                    {
                        'text': 'Llamar directamente al supuesto remitente para confirmar autenticidad',
                        'tags': ['phishing', 'correo', 'social', 'urgencia'],
                        'risk': 'bajo', 'time': 2, 'success': 85,
                        'effect_on_state': {'success': {'pistas': +1}, 'failure': {}},
                        'outcome_text': {
                            'success': 'El remitente confirmó que nunca envió ese correo. Evitaste caer en la trampa.',
                            'failure': 'No lograste contactarlo a tiempo, pero al menos no abriste el enlace.'
                        }
                    },
                    {
                        'text': 'Hacer clic en el enlace para verificar si es legítimo',
                        'tags': ['phishing', 'correo', 'urgencia'],
                        'risk': 'alto', 'time': 1, 'success': 15,
                        'effect_on_state': {'success': {}, 'failure': {'alert_level': +3, 'credentials_leaked': +1}},
                        'outcome_text': {
                            'success': 'Por suerte era un test de concientización de seguridad (simulacro).',
                            'failure': 'El enlace instaló malware y envió tus credenciales al atacante. Incidente crítico iniciado.'
                        }
                    },
                ],
                'mid': [
                    {
                        'text': 'Colocar el USB en bolsa antiestática y llevarlo inmediatamente a IT sin conectarlo',
                        'tags': ['usb', 'physical'],
                        'risk': 'bajo', 'time': 1, 'success': 95,
                        'effect_on_state': {'success': {'pistas': +1}, 'failure': {}},
                        'outcome_text': {
                            'success': 'IT analizó el USB en sandbox: contenía un payload de ransomware. Evitaste un desastre.',
                            'failure': 'IT estaba ocupado, pero al menos no lo conectaste.'
                        }
                    },
                    {
                        'text': 'Conectar el USB en tu equipo "solo para ver qué contiene"',
                        'tags': ['usb', 'physical'],
                        'risk': 'crítico', 'time': 1, 'success': 5,
                        'effect_on_state': {'success': {}, 'failure': {'alert_level': +3, 'compromised_hosts': +1}},
                        'outcome_text': {
                            'success': 'Increíblemente, el USB solo tenía documentos vacíos.',
                            'failure': 'El USB ejecutó un script que cifró tus archivos y se propagó por la red. Ransomware detectado.'
                        }
                    },
                    {
                        'text': 'Cambiar todas tus contraseñas y activar autenticación multifactor (MFA)',
                        'tags': ['credentials', 'mfa', 'phishing'],
                        'risk': 'bajo', 'time': 2, 'success': 90,
                        'effect_on_state': {'success': {'credentials_leaked': -1, 'alert_level': -1}, 'failure': {}},
                        'outcome_text': {
                            'success': 'Actualizaste tus credenciales y configuraste MFA. Ahora estás mucho más protegido.',
                            'failure': 'Algunos servicios no permitieron el cambio inmediato por políticas corporativas.'
                        }
                    },
                ],
                'late': [
                    {
                        'text': 'Rechazar la solicitud educadamente y verificar por canal oficial (email corporativo)',
                        'tags': ['social', 'credentials', 'vishing'],
                        'risk': 'bajo', 'time': 1, 'success': 90,
                        'effect_on_state': {'success': {'pistas': +1}, 'failure': {}},
                        'outcome_text': {
                            'success': 'Tu jefe confirmó que nunca solicitó eso. Era un intento de suplantación.',
                            'failure': 'Tu jefe no respondió de inmediato, pero al menos no compartiste credenciales.'
                        }
                    },
                    {
                        'text': 'Desconectar tu equipo de la red y llamar a IT inmediatamente',
                        'tags': ['incident', 'malware', 'response'],
                        'risk': 'bajo', 'time': 1, 'success': 85,
                        'effect_on_state': {'success': {'compromised_hosts': -1, 'alert_level': +1}, 'failure': {}},
                        'outcome_text': {
                            'success': 'Aislaste el problema a tiempo. IT inició análisis forense de tu equipo.',
                            'failure': 'IT llegó tarde pero al menos conteniste el daño desconectando la red.'
                        }
                    },
                ]
            },
            
            'hacker': {
                'early': [
                    {
                        'text': 'Correlacionar logs del firewall, proxy y AD para identificar origen del ataque',
                        'tags': ['logs', 'detection', 'bruteforce', 'anomaly'],
                        'risk': 'bajo', 'time': 2, 'success': 85,
                        'effect_on_state': {'success': {'pistas': +2}, 'failure': {'alert_level': +1}},
                        'outcome_text': {
                            'success': 'Identificaste la IP atacante y patrones de ataque. Procedes a bloquear y alertar.',
                            'failure': 'Los logs estaban fragmentados. Necesitas más tiempo o herramientas adicionales.'
                        }
                    },
                    {
                        'text': 'Implementar bloqueo IP inmediato en firewall y activar rate limiting',
                        'tags': ['firewall', 'bruteforce', 'mitigation'],
                        'risk': 'bajo', 'time': 1, 'success': 90,
                        'effect_on_state': {'success': {'alert_level': -1}, 'failure': {}},
                        'outcome_text': {
                            'success': 'Bloqueaste la IP y los intentos cesaron. Éxito táctico.',
                            'failure': 'El atacante cambió de IP. Necesitas estrategia más robusta.'
                        }
                    },
                    {
                        'text': 'Escanear la red completa en busca de otros indicadores de compromiso (IOCs)',
                        'tags': ['scan', 'detection', 'forensics'],
                        'risk': 'medio', 'time': 3, 'success': 75,
                        'effect_on_state': {'success': {'pistas': +2, 'compromised_hosts': +1}, 'failure': {}},
                        'outcome_text': {
                            'success': 'Detectaste 2 hosts adicionales ya comprometidos. Ahora sabes la magnitud del problema.',
                            'failure': 'El escaneo no encontró más evidencia, pero consumió recursos valiosos.'
                        }
                    },
                ],
                'mid': [
                    {
                        'text': 'Aislar red de finanzas y ejecutar análisis forense en el sistema afectado',
                        'tags': ['ransomware', 'incident', 'forensics', 'response'],
                        'risk': 'medio', 'time': 2, 'success': 80,
                        'effect_on_state': {'success': {'compromised_hosts': -1, 'pistas': +1}, 'failure': {'alert_level': +2}},
                        'outcome_text': {
                            'success': 'Contuviste el ransomware a tiempo. Forense reveló el vector de entrada.',
                            'failure': 'El aislamiento fue lento y el ransomware se propagó a 3 sistemas más.'
                        }
                    },
                    {
                        'text': 'Restaurar desde backup más reciente y validar integridad de archivos',
                        'tags': ['ransomware', 'backup', 'recovery'],
                        'risk': 'bajo', 'time': 3, 'success': 85,
                        'effect_on_state': {'success': {'compromised_hosts': -1}, 'failure': {'alert_level': +1}},
                        'outcome_text': {
                            'success': 'Restauración exitosa. Sistema operativo en 2 horas. Crisis evitada.',
                            'failure': 'El backup estaba corrupto parcialmente. Se perdieron datos de 48hrs.'
                        }
                    },
                    {
                        'text': 'Bloquear exfiltración mediante reglas DLP y alertar al equipo legal',
                        'tags': ['exfiltration', 'logs', 'anomaly'],
                        'risk': 'medio', 'time': 2, 'success': 75,
                        'effect_on_state': {'success': {'pistas': +1, 'alert_level': -1}, 'failure': {'alert_level': +1}},
                        'outcome_text': {
                            'success': 'Bloqueaste la transferencia de datos. Se exfiltraron solo 200MB de 2GB planeados.',
                            'failure': 'La exfiltración se completó antes de que actuaras. Forense determinará el daño.'
                        }
                    },
                ],
                'late': [
                    {
                        'text': 'Revocar credenciales comprometidas masivamente y forzar reset de contraseñas',
                        'tags': ['credentials', 'incident', 'response', 'phishing'],
                        'risk': 'bajo', 'time': 2, 'success': 85,
                        'effect_on_state': {'success': {'credentials_leaked': -2, 'alert_level': -1}, 'failure': {}},
                        'outcome_text': {
                            'success': 'Revocaste 47 credenciales comprometidas. El atacante perdió acceso.',
                            'failure': 'La revocación fue parcial. Algunas cuentas de servicio quedaron expuestas.'
                        }
                    },
                    {
                        'text': 'Implementar detección EDR en todos los endpoints y configurar alertas ML',
                        'tags': ['malware', 'persistence', 'detection'],
                        'risk': 'bajo', 'time': 3, 'success': 80,
                        'effect_on_state': {'success': {'pistas': +1, 'alert_level': -1}, 'failure': {}},
                        'outcome_text': {
                            'success': 'EDR detectó 3 backdoors activos que pasaron desapercibidos. Ahora puedes neutralizarlos.',
                            'failure': 'El despliegue de EDR causó falsos positivos que saturaron al equipo.'
                        }
                    },
                    {
                        'text': 'Generar informe ejecutivo del incidente y coordinar comunicación con stakeholders',
                        'tags': ['incident', 'response', 'communication'],
                        'risk': 'bajo', 'time': 2, 'success': 75,
                        'effect_on_state': {'success': {}, 'failure': {}},
                        'outcome_text': {
                            'success': 'El informe tranquilizó a la dirección y se aprobó presupuesto para mejoras.',
                            'failure': 'La comunicación fue confusa y generó pánico innecesario en la organización.'
                        }
                    },
                ]
            },
            
            'cyberdelincuente': {
                'early': [
                    {
                        'text': 'Crear campaña de spear-phishing dirigida a ejecutivos con pretexto convincente',
                        'tags': ['phishing', 'spear', 'recon', 'social'],
                        'risk': 'medio', 'time': 2, 'success': 65,
                        'effect_on_state': {'success': {'credentials_leaked': +1, 'pistas': +1}, 'failure': {'alert_level': +1}},
                        'outcome_text': {
                            'success': '3 ejecutivos abrieron tu email y 1 entregó credenciales. Acceso inicial conseguido.',
                            'failure': 'El filtro anti-spam bloqueó tu campaña. Debes cambiar de estrategia.'
                        }
                    },
                    {
                        'text': 'Realizar reconocimiento pasivo mediante OSINT y scraping de redes sociales',
                        'tags': ['recon', 'osint'],
                        'risk': 'bajo', 'time': 1, 'success': 90,
                        'effect_on_state': {'success': {'pistas': +2}, 'failure': {}},
                        'outcome_text': {
                            'success': 'Recopilaste organigramas, emails, tecnologías usadas y nombres de empleados clave.',
                            'failure': 'La información pública era limitada. Necesitas técnicas más agresivas.'
                        }
                    },
                    {
                        'text': 'Escanear perímetro en busca de servicios expuestos y vulnerabilidades conocidas',
                        'tags': ['recon', 'scan', 'vulnerability'],
                        'risk': 'medio', 'time': 2, 'success': 70,
                        'effect_on_state': {'success': {'pistas': +2}, 'failure': {'alert_level': +1}},
                        'outcome_text': {
                            'success': 'Encontraste un servidor Tomcat desactualizado con CVE-2021-42013 explotable.',
                            'failure': 'Tu escaneo fue detectado por el IDS. Ahora están alerta.'
                        }
                    },
                ],
                'mid': [
                    {
                        'text': 'Explotar vulnerabilidad detectada para obtener shell reverso en servidor web',
                        'tags': ['exploit', 'vulnerability', 'rce'],
                        'risk': 'alto', 'time': 2, 'success': 70,
                        'effect_on_state': {'success': {'compromised_hosts': +1, 'alert_level': +1}, 'failure': {'alert_level': +2}},
                        'outcome_text': {
                            'success': 'Conseguiste shell con privilegios de www-data. Ahora puedes escalar.',
                            'failure': 'El exploit falló y generó logs. El equipo de seguridad está investigando.'
                        }
                    },
                    {
                        'text': 'Realizar movimiento lateral usando Pass-the-Hash con credenciales robadas',
                        'tags': ['lateral', 'credentials', 'privilege'],
                        'risk': 'alto', 'time': 2, 'success': 60,
                        'effect_on_state': {'success': {'compromised_hosts': +1, 'pistas': +1}, 'failure': {'alert_level': +2}},
                        'outcome_text': {
                            'success': 'Accediste a 3 sistemas adicionales incluyendo un servidor de archivos.',
                            'failure': 'La autenticación falló. Parece que rotaron las credenciales.'
                        }
                    },
                    {
                        'text': 'Instalar beacon de Cobalt Strike para persistencia y comando y control',
                        'tags': ['persistence', 'backdoor', 'c2'],
                        'risk': 'alto', 'time': 2, 'success': 65,
                        'effect_on_state': {'success': {'tiene_objeto_clave': True}, 'failure': {'alert_level': +2}},
                        'outcome_text': {
                            'success': 'Beacon instalado y comunicándose cada 5 minutos. Tienes acceso persistente.',
                            'failure': 'El antivirus detectó y eliminó el beacon. Perdiste el acceso.'
                        }
                    },
                    {
                        'text': 'Desplegar USB con Rubber Ducky en áreas comunes de la empresa',
                        'tags': ['usb', 'physical', 'payload'],
                        'risk': 'medio', 'time': 3, 'success': 50,
                        'effect_on_state': {'success': {'compromised_hosts': +1}, 'failure': {'alert_level': +1}},
                        'outcome_text': {
                            'success': 'Un empleado conectó el USB. Tienes shell en su equipo.',
                            'failure': 'Seguridad física recogió el USB antes de que alguien lo conectara.'
                        }
                    },
                ],
                'late': [
                    {
                        'text': 'Escalar privilegios a Domain Admin mediante vulnerabilidad Zerologon',
                        'tags': ['privilege', 'exploit', 'lateral'],
                        'risk': 'crítico', 'time': 2, 'success': 55,
                        'effect_on_state': {'success': {'compromised_hosts': +2, 'pistas': +2}, 'failure': {'alert_level': +3}},
                        'outcome_text': {
                            'success': 'Conseguiste privilegios de Domain Admin. Control total de la red.',
                            'failure': 'El exploit falló y generó alertas críticas. Respuesta a incidentes activada.'
                        }
                    },
                    {
                        'text': 'Exfiltrar base de datos de clientes y cifrar servidores para pedir rescate',
                        'tags': ['exfiltration', 'ransomware', 'data'],
                        'risk': 'crítico', 'time': 3, 'success': 60,
                        'effect_on_state': {'success': {'credentials_leaked': +3, 'compromised_hosts': +2}, 'failure': {'alert_level': +3}},
                        'outcome_text': {
                            'success': 'Exfiltraste 50GB de datos sensibles y cifraste 30 servidores. Doble extorsión exitosa.',
                            'failure': 'DLP bloqueó la exfiltración y EDR detuvo el ransomware. Operación fallida.'
                        }
                    },
                    {
                        'text': 'Borrar logs de eventos y desactivar soluciones de seguridad antes de salir',
                        'tags': ['cleanup', 'logs', 'evasion'],
                        'risk': 'medio', 'time': 2, 'success': 55,
                        'effect_on_state': {'success': {'alert_level': -1}, 'failure': {'alert_level': +1}},
                        'outcome_text': {
                            'success': 'Limpiaste la mayoría de evidencias. Forense será difícil y costoso.',
                            'failure': 'Dejaste suficientes rastros para que te identifiquen. El FBI está involucrado.'
                        }
                    },
                    {
                        'text': 'Vender acceso a la red comprometida en foros de la dark web',
                        'tags': ['exfiltration', 'credentials', 'monetization'],
                        'risk': 'medio', 'time': 1, 'success': 70,
                        'effect_on_state': {'success': {'pistas': +1}, 'failure': {}},
                        'outcome_text': {
                            'success': 'Vendiste el acceso por $15,000. Otros actores ahora explotan la red.',
                            'failure': 'Los compradores eran honeypot de las autoridades. Estás bajo vigilancia.'
                        }
                    },
                ]
            }
        }

    def _generate_options(self, character_type: str, stage: int, total_stages: int, 
                         scenario: Dict[str, Any], location: str, event: Dict[str, Any], 
                         state: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Genera exactamente 3 opciones contextuales correlacionadas con el evento."""
        
        # Determinar fase narrativa
        fraction = stage / max(1, total_stages - 1) if total_stages > 1 else 0
        if fraction < 0.33:
            phase = 'early'
        elif fraction < 0.66:
            phase = 'mid'
        else:
            phase = 'late'
        
        catalog = self._base_options_catalog()
        character_catalog = catalog.get(character_type, {})
        
        if not character_catalog:
            print(f"      ⚠️ No hay catálogo para '{character_type}'")
            # Crear 3 opciones genéricas de emergencia
            return [
                self._create_contextual_generic(['general'], location, character_type)
                for _ in range(3)
            ]
        
        phase_candidates = list(character_catalog.get(phase, []))
        
        if not phase_candidates:
            print(f"      ⚠️ No hay candidatos para fase '{phase}', buscando en otras fases")
            # Buscar en todas las fases disponibles
            for p in ['early', 'mid', 'late']:
                phase_candidates.extend(character_catalog.get(p, []))
            
            if not phase_candidates:
                print(f"      ⚠️ No hay opciones en el catálogo para '{character_type}', generando genéricas")
                return [
                    self._create_contextual_generic(['general'], location, character_type)
                    for _ in range(3)
                ]
        
        event_tags = event.get('tags', []) if isinstance(event, dict) else []
        
        print(f"      Tags del evento: {event_tags}")
        print(f"      Fase: {phase}, Candidatos disponibles: {len(phase_candidates)}")
        
        # Función de matching por tags
        def tag_match_score(candidate: Dict[str, Any]) -> int:
            """Calcula score de relevancia entre opción y evento."""
            ctags = candidate.get('tags', [])
            if not ctags or not event_tags:
                return 0
            
            # Contar tags en común
            common_tags = len(set(ctags) & set(event_tags))
            
            # Bonus por tags críticos
            critical_match = any(t in ctags for t in event_tags if t in [
                'phishing', 'ransomware', 'exfiltration', 'credentials', 'malware'
            ])
            
            return common_tags * 10 + (20 if critical_match else 0)
        
        print(f"      Calculando scores de matching...")
        # Ordenar candidatos por relevancia
        scored_candidates = [(opt, tag_match_score(opt)) for opt in phase_candidates]
        scored_candidates.sort(key=lambda x: x[1], reverse=True)
        
        print(f"      Scores calculados: {[(i, s) for i, (o, s) in enumerate(scored_candidates[:5])]}")
        
        # Filtrar opciones con score > 0
        filtered = [opt for opt, score in scored_candidates if score > 0]
        print(f"      Opciones filtradas con score > 0: {len(filtered)}")
        
        # Si no hay suficientes, buscar en otras fases
        if len(filtered) < 3:
            for other_phase in ['early', 'mid', 'late']:
                if other_phase == phase:
                    continue
                    
                other_candidates = list(catalog.get(character_type, {}).get(other_phase, []))
                other_scored = [(opt, tag_match_score(opt)) for opt in other_candidates]
                other_scored.sort(key=lambda x: x[1], reverse=True)
                
                for opt, score in other_scored:
                    if score > 0 and opt not in filtered:
                        filtered.append(opt)
                        if len(filtered) >= 3:
                            break
                            
                if len(filtered) >= 3:
                    break
        
        # Si aún faltan, crear opciones genéricas contextuales
        safety_counter = 0
        max_generic_attempts = 10
        
        print(f"      Completando con opciones genéricas si es necesario...")
        while len(filtered) < 3 and safety_counter < max_generic_attempts:
            safety_counter += 1
            print(f"        Intento genérico {safety_counter}/{max_generic_attempts}")
            
            generic = self._create_contextual_generic(event_tags, location, character_type)
            
            # Verificar que no exista ya (por texto)
            if not any(opt['text'] == generic['text'] for opt in filtered):
                filtered.append(generic)
                print(f"        ✓ Opción genérica agregada ({len(filtered)}/3)")
            else:
                # Si ya existe, modificar el texto para hacerlo único
                generic['text'] = f"{generic['text']} (opción {len(filtered)+1})"
                filtered.append(generic)
                print(f"        ✓ Opción genérica modificada agregada ({len(filtered)}/3)")
        
        print(f"      Total después de genéricas: {len(filtered)}")
        
        # Último recurso: si aún no hay 3, completar con opciones muy básicas
        while len(filtered) < 3:
            print(f"        ⚠️ Usando fallback para completar ({len(filtered)}/3)")
            fallback_option = {
                'text': f'Evaluar situación cuidadosamente desde {location} (alternativa {len(filtered)+1})',
                'tags': ['general'],
                'risk': 'medio',
                'time': 1,
                'success': 60,
                'effect_on_state': {'success': {}, 'failure': {'alert_level': +1}},
                'outcome_text': {
                    'success': 'Tomaste un momento para analizar antes de actuar.',
                    'failure': 'Perdiste tiempo valioso evaluando la situación.'
                }
            }
            filtered.append(fallback_option)
        
        print(f"      ✓ Total final: {len(filtered)} opciones")
        
        # Asegurar campos completos
        for opt in filtered[:3]:
            opt.setdefault('risk', 'medio')
            opt.setdefault('time', 1)
            opt.setdefault('success', 50)
            opt.setdefault('effect_on_state', {'success': {}, 'failure': {'alert_level': +1}})
            opt.setdefault('outcome_text', {
                'success': 'Acción completada exitosamente.',
                'failure': 'La acción no tuvo el resultado esperado.'
            })
        
        return filtered[:3]

    def _create_contextual_generic(self, tags: List[str], location: str, 
                                   character_type: str) -> Dict[str, Any]:
        """Crea opción genérica pero contextualmente relevante."""
        
        # Diccionarios de respuestas genéricas por tipo de amenaza
        generic_responses = {
            'phishing': {
                'usuario': f'Reportar el correo sospechoso a IT desde {location} sin interactuar',
                'hacker': f'Analizar headers del correo y bloquear el dominio desde {location}',
                'cyberdelincuente': f'Registrar dominio similar y preparar infraestructura desde {location}'
            },
            'usb': {
                'usuario': f'Entregar el dispositivo a seguridad sin conectarlo en {location}',
                'hacker': f'Analizar el dispositivo en sandbox aislado en {location}',
                'cyberdelincuente': f'Preparar USB con payload y dejarlo en {location}'
            },
            'ransomware': {
                'usuario': f'Desconectar equipo de la red y alertar a IT desde {location}',
                'hacker': f'Aislar segmento afectado y activar protocolo de recuperación en {location}',
                'cyberdelincuente': f'Cifrar archivos críticos y dejar nota de rescate en {location}'
            },
            'credentials': {
                'usuario': f'Cambiar contraseñas y activar MFA desde {location}',
                'hacker': f'Revocar credenciales comprometidas y forzar reset en {location}',
                'cyberdelincuente': f'Usar credenciales para movimiento lateral desde {location}'
            },
            'exfiltration': {
                'usuario': f'Reportar actividad de red anómala desde {location}',
                'hacker': f'Bloquear tráfico saliente sospechoso mediante firewall en {location}',
                'cyberdelincuente': f'Exfiltrar datos cifrados por canal encubierto desde {location}'
            }
        }
        
        # Determinar categoría principal
        main_category = 'phishing'  # default
        for category in generic_responses.keys():
            if any(category in tag for tag in tags):
                main_category = category
                break
        
        text = generic_responses.get(main_category, {}).get(
            character_type, 
            f'Evaluar la situación y tomar acción apropiada desde {location}'
        )
        
        return {
            'text': text,
            'tags': tags if tags else ['general'],
            'risk': 'medio',
            'time': 1,
            'success': 70,
            'effect_on_state': {
                'success': {'pistas': +1},
                'failure': {'alert_level': +1}
            },
            'outcome_text': {
                'success': 'Tu acción mitigó la situación efectivamente.',
                'failure': 'La respuesta fue insuficiente o tardía.'
            }
        }

    def generate_new_story(self, character_type: str, seed: Optional[int] = None) -> Dict[str, Any]:
        """Genera historia completa y coherente para el personaje especificado."""
        
        if seed is not None:
            random.seed(seed)
        
        if character_type not in ('usuario', 'hacker', 'cyberdelincuente'):
            raise ValueError("character_type debe ser 'usuario', 'hacker' o 'cyberdelincuente'")
        
        # Mapeo de personaje a escenario específico
        scenario_map = {
            'usuario': 'usuario_oficina',
            'hacker': 'hacker_empresa',
            'cyberdelincuente': 'ciberdelincuente_ataque'
        }
        
        # Seleccionar escenario específico para el personaje
        target_scenario_id = scenario_map.get(character_type)
        scenario = next(
            (s for s in self.story_templates['scenarios'] if s['id'] == target_scenario_id),
            self.story_templates['scenarios'][0]  # fallback
        )
        
        goal, antagonist, key_item = self._create_thread(scenario, character_type)
        
        # Debug info
        print(f"🎮 Generando historia para: {character_type}")
        print(f"📋 Escenario: {scenario.get('name', 'Sin nombre')}")
        print(f"🎯 Objetivo: {goal}")
        
        # Estado inicial
        state = {
            'alert_level': 0,
            'pistas': 0,
            'tiene_objeto_clave': False,
            'current_location': scenario['locations'][0]['name'],
            'aliados': [],
            'compromised_hosts': 0,
            'credentials_leaked': 0
        }
        
        # Generar entre 5-7 etapas para narrativa completa
        num_stages = random.randint(5, 7)
        story_stages: List[Dict[str, Any]] = []
        used_events = set()
        self.narrative_memory = []
        
        for i in range(num_stages):
            print(f"  📍 Generando etapa {i+1}/{num_stages}...")
            
            # Mover a nueva ubicación
            location = self._choose_location(state['current_location'], scenario)
            state['current_location'] = location
            print(f"    Ubicación: {location}")
            
            # Seleccionar evento único
            event = None
            attempts = 0
            max_attempts = 20  # Aumentado para dar más oportunidades
            
            # Primero intentar encontrar evento específico del personaje que no se haya usado
            while attempts < max_attempts:
                candidate = self._choose_event_by_state(state, stage_num=i)
                event_id = candidate['text']
                candidate_tags = candidate.get('tags', [])
                
                # Verificar que el evento sea para el personaje correcto
                is_correct_character = character_type in candidate_tags
                is_not_used = event_id not in used_events
                
                if is_correct_character and is_not_used:
                    event = candidate
                    used_events.add(event_id)
                    print(f"    ✓ Evento válido para {character_type}")
                    break
                elif not is_correct_character:
                    print(f"    ✗ Evento rechazado: no es para {character_type} (tags: {candidate_tags})")
                    
                attempts += 1
            
            if event is None:
                print(f"    ⚠️ No se encontró evento único de {character_type} después de {max_attempts} intentos")
                # Último recurso: usar cualquier evento del personaje, incluso si está repetido
                candidate = self._choose_event_by_state(state, stage_num=i)
                if character_type in candidate.get('tags', []):
                    event = candidate
                    print(f"    ⚠️ Usando evento repetido pero correcto para {character_type}")
                else:
                    # Buscar manualmente un evento del personaje correcto
                    all_events = self.story_templates['events']
                    correct_events = [e for e in all_events if character_type in e.get('tags', [])]
                    if correct_events:
                        event = random.choice(correct_events)
                        print(f"    ⚠️ Forzando evento correcto para {character_type}")
                    else:
                        event = candidate
                        print(f"    ❌ ERROR: No hay eventos para {character_type}, usando cualquiera")
            
            print(f"    Evento seleccionado: {event['text'][:50]}...")
            
            # Guardar en memoria narrativa
            self.narrative_memory.append(event.get('tags', []))
            
            # Generar descripción contextual
            print(f"    Generando descripción...")
            description = self._generate_description(
                scenario, location, event, i, state, 
                goal, antagonist, key_item, 
                show_objective=(i == 0)
            )
            
            # Generar opciones correlacionadas
            print(f"    Generando opciones...")
            options = self._generate_options(
                character_type, i, num_stages, 
                scenario, location, event, state
            )
            print(f"    ✓ {len(options)} opciones generadas")
            
            # Aplicar efectos del evento
            state = self._apply_event_effects(state, event)
            
            # Crear entrada de etapa
            stage_entry = {
                'stage': i + 1,
                'location': location,
                'event': event,
                'description': description,
                'options': options,
                'state_snapshot': state.copy(),
                'results': []
            }
            
            story_stages.append(stage_entry)
        
        # Construir historia completa
        self.current_story = {
            'scenario': scenario,
            'stages': story_stages,
            'character': character_type,
            'objective': goal,
            'antagonist': antagonist,
            'key_item': key_item,
            'final_state': state.copy()
        }
        
        self.stage_index = 0
        
        print(f"✅ Historia generada exitosamente: {len(story_stages)} etapas")
        
        return self.current_story

    def get_current_stage(self) -> Optional[Dict[str, Any]]:
        """Obtiene la etapa actual de la historia."""
        if not self.current_story:
            return None
            
        stages = self.current_story.get('stages', [])
        if 0 <= self.stage_index < len(stages):
            return stages[self.stage_index]
            
        return None

    def is_story_complete(self) -> bool:
        """Verifica si la historia ha terminado."""
        if not self.current_story:
            return True
            
        return self.stage_index >= len(self.current_story.get('stages', []))

    def resolve_option(self, current_state: Dict[str, Any], 
                      option: Dict[str, Any]) -> Dict[str, Any]:
        """Resuelve la opción elegida por el jugador y avanza la historia."""
        
        # Determinar éxito basado en probabilidad
        chance = option.get('success', 50)
        roll = random.randint(1, 100)
        success = roll <= chance
        
        # Obtener estado actual
        state = self.current_story.get('final_state', {}).copy() if self.current_story else current_state.copy()
        
        # Aplicar efectos de la opción
        new_state = self._apply_option_effects(state, option, success)
        
        # Actualizar estado final
        if self.current_story:
            self.current_story['final_state'] = new_state
        
        # Registrar resultado en la etapa
        if self.current_story and 0 <= self.stage_index < len(self.current_story['stages']):
            stage = self.current_story['stages'][self.stage_index]
            stage['state_snapshot'] = new_state.copy()
            
            outcome_text = option.get('outcome_text', {})
            result_text = outcome_text.get('success' if success else 'failure', '')
            
            stage['results'].append({
                'choice_text': option.get('text', ''),
                'success': success,
                'text': result_text
            })
        
        # Avanzar a la siguiente etapa
        self.stage_index += 1
        
        # Determinar si la historia está completa
        story_complete = self.is_story_complete()
        next_stage = self.get_current_stage() if not story_complete else None
        
        # Construir respuesta
        outcome_text = option.get('outcome_text', {})
        text = outcome_text.get('success' if success else 'failure', '') if isinstance(outcome_text, dict) else str(outcome_text)
        
        return {
            'success': success,
            'new_state': new_state,
            'result_text': text,
            'roll': roll,
            'chance': chance,
            'story_complete': story_complete,
            'next_stage': next_stage
        }

    def get_story_summary(self) -> Dict[str, Any]:
        """Genera resumen de la historia completada."""
        if not self.current_story:
            return {}
        
        final_state = self.current_story.get('final_state', {})
        stages = self.current_story.get('stages', [])
        
        # Calcular estadísticas
        total_choices = sum(len(stage.get('results', [])) for stage in stages)
        successful_choices = sum(
            1 for stage in stages 
            for result in stage.get('results', []) 
            if result.get('success', False)
        )
        
        success_rate = (successful_choices / total_choices * 100) if total_choices > 0 else 0
        
        # Determinar desenlace
        alert = final_state.get('alert_level', 0)
        pistas = final_state.get('pistas', 0)
        compromised = final_state.get('compromised_hosts', 0)
        
        if alert >= 3:
            outcome = 'CRÍTICO: Incidente de seguridad mayor'
        elif alert >= 2:
            outcome = 'ALTO RIESGO: Situación controlada pero con daños'
        elif alert == 1:
            outcome = 'MODERADO: Amenazas detectadas y mitigadas'
        else:
            outcome = 'EXITOSO: Seguridad mantenida efectivamente'
        
        return {
            'character': self.current_story.get('character', ''),
            'objective': self.current_story.get('objective', ''),
            'stages_completed': len(stages),
            'total_choices': total_choices,
            'successful_choices': successful_choices,
            'success_rate': round(success_rate, 1),
            'final_alert_level': alert,
            'pistas_collected': pistas,
            'compromised_hosts': compromised,
            'outcome': outcome,
            'final_state': final_state
        }