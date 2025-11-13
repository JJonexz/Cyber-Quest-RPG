# ============================================================================
# ARCHIVO: models/story.py
# DESCRIPCIÓN: Sistema de generación de historias dinámicas con IA.
#              Historias realistas de ciberseguridad con tags en eventos y
#              opciones. Selección de opciones estrictamente contextual por tag.
# ============================================================================

import random
from typing import Dict, List, Any, Optional, Tuple


class StoryGenerator:

    # (Eliminada la versión dañada y duplicada de _generate_options)

    def __init__(self, seed: Optional[int] = None):
        if seed is not None:
            random.seed(seed)
        self.story_templates = self._load_story_templates()

    def _load_story_templates(self) -> Dict[str, Any]:
        """Carga plantillas base para generar historias diferenciadas por dificultad/personaje."""
        return {
            'scenarios': [
                # Usuario: oficinista, historias de defensa personal y errores comunes
                {
                    'id': 'usuario_oficina',
                    'name': 'Riesgos Digitales en la Oficina',
                    'context': 'Como oficinista, enfrentas intentos de engaño digital, dispositivos sospechosos y errores cotidianos que pueden poner en riesgo tus datos y los de la empresa.',
                    'locations': [
                        {'name': 'Bandeja de Entrada', 'connections': ['PC Personal', 'Red WiFi Pública']},
                        {'name': 'PC Personal', 'connections': ['Bandeja de Entrada', 'Dispositivo Móvil']},
                        {'name': 'Dispositivo Móvil', 'connections': ['PC Personal', 'Café con WiFi']},
                        {'name': 'Café con WiFi', 'connections': ['Dispositivo Móvil', 'Bandeja de Entrada']},
                        {'name': 'Red WiFi Pública', 'connections': ['Café con WiFi']}
                    ],
                    'objectives': {
                        'usuario': 'Mantener tu identidad y datos seguros frente a intentos de engaño.',
                        'hacker': 'N/A',
                        'cyberdelincuente': 'N/A'
                    }
                },
                # Hacker ético: actividades de protección, respuesta y prevención
                {
                    'id': 'hacker_empresa',
                    'name': 'Defensa y Respuesta en la Empresa',
                    'context': 'Como profesional de ciberseguridad, tu misión es proteger la infraestructura, corregir errores de compañeros y anticipar ataques, implementando controles y educando a usuarios.',
                    'locations': [
                        {'name': 'SOC', 'connections': ['Oficina TI', 'Sala de Servidores']},
                        {'name': 'Oficina TI', 'connections': ['SOC', 'Puestos de Trabajo']},
                        {'name': 'Puestos de Trabajo', 'connections': ['Oficina TI', 'Recepción']},
                        {'name': 'Recepción', 'connections': ['Puestos de Trabajo', 'Sala de Servidores']},
                        {'name': 'Sala de Servidores', 'connections': ['SOC', 'Recepción']}
                    ],
                    'objectives': {
                        'usuario': 'N/A',
                        'hacker': 'Detectar, mitigar y prevenir incidentes de seguridad en la empresa, corrigiendo errores y educando a los empleados.',
                        'cyberdelincuente': 'N/A'
                    }
                },
                # Ciberdelincuente: actividades ofensivas, simulando ataques
                {
                    'id': 'ciberdelincuente_ataque',
                    'name': 'Campaña de Ataque a la Empresa',
                    'context': 'Como hacker externo, tu objetivo es comprometer la empresa usando phishing, USBs maliciosos, ingeniería social y técnicas avanzadas para evadir defensas.',
                    'locations': [
                        {'name': 'Cafetería', 'connections': ['Estacionamiento', 'Oficina Externa']},
                        {'name': 'Estacionamiento', 'connections': ['Cafetería', 'Recepción']},
                        {'name': 'Recepción', 'connections': ['Estacionamiento', 'Oficina Externa']},
                        {'name': 'Oficina Externa', 'connections': ['Cafetería', 'Recepción']}
                    ],
                    'objectives': {
                        'usuario': 'N/A',
                        'hacker': 'N/A',
                        'cyberdelincuente': 'Comprometer la empresa mediante técnicas de ataque y obtener acceso a información sensible.'
                    }
                }
            ],
            # Eventos diferenciados por dificultad/personaje
            'events': [
                # Usuario: eventos de defensa y errores comunes
                {'text': 'Recibes un correo sospechoso pidiendo tus credenciales.', 'effect': {'alert_level': +1}, 'tags': ['phishing', 'correo', 'usuario']},
                {'text': 'Encuentras un USB en la sala de descanso.', 'effect': {'pistas': +1}, 'tags': ['usb', 'physical', 'usuario']},
                {'text': 'Tu compañero te pide tu contraseña para "arreglar" tu PC.', 'effect': {'alert_level': +1}, 'tags': ['social', 'credentials', 'usuario']},
                {'text': 'Intentas conectarte a la WiFi pública y ves un portal falso.', 'effect': {'alert_level': +2}, 'tags': ['phishing', 'wifi', 'usuario']},
                # Hacker ético: eventos de protección y respuesta
                {'text': 'Detectas tráfico inusual en el firewall.', 'effect': {'pistas': +1, 'alert_level': +1}, 'tags': ['logs', 'firewall', 'hacker']},
                {'text': 'Un empleado conecta un USB no autorizado.', 'effect': {'alert_level': +2}, 'tags': ['usb', 'physical', 'hacker']},
                {'text': 'Se reporta un intento de phishing masivo a empleados.', 'effect': {'alert_level': +2}, 'tags': ['phishing', 'correo', 'hacker']},
                {'text': 'Encuentras credenciales escritas en un post-it.', 'effect': {'pistas': +1}, 'tags': ['credentials', 'hacker']},
                {'text': 'Un servidor muestra actividad de ransomware.', 'effect': {'alert_level': +3}, 'tags': ['ransomware', 'hacker']},
                # Ciberdelincuente: eventos ofensivos
                {'text': 'Preparas un correo de phishing suplantando a un directivo.', 'effect': {'pistas': +1}, 'tags': ['phishing', 'correo', 'cyberdelincuente']},
                {'text': 'Dejas un USB malicioso en el estacionamiento.', 'effect': {'pistas': +1}, 'tags': ['usb', 'physical', 'cyberdelincuente']},
                {'text': 'Obtienes acceso a una cuenta débil tras un ataque de diccionario.', 'effect': {'alert_level': +1}, 'tags': ['credentials', 'bruteforce', 'cyberdelincuente']},
                {'text': 'Logras evadir el firewall y exfiltrar datos.', 'effect': {'pistas': +2, 'alert_level': +2}, 'tags': ['exfiltration', 'firewall', 'cyberdelincuente']},
                {'text': 'Simulas una llamada de soporte para obtener acceso remoto.', 'effect': {'alert_level': +1}, 'tags': ['vishing', 'cyberdelincuente']}
            ],
            'consequences': [
                'Se generaron logs que indican acceso no autorizado.',
                'Se activó una alerta y el equipo de respuesta se moviliza.',
                'Se pudo contener una exfiltración parcial.',
                'El atacante consiguió persistencia en un host.',
                'La campaña de phishing obtuvo algunas credenciales débiles.',
                'Se restauraron archivos desde backups.'
            ]
        }
    def _generate_options(self,
                          character_type: str,
                          stage: int,
                          total_stages: int,
                          scenario: Dict[str, Any],
                          location: str,
                          event: Dict[str, Any],
                          state: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Devuelve exactamente 3 opciones contextuales relacionadas con el event.tags, sin repetir texto."""
        # Determinar fase (early/mid/late)
        fraction = stage / max(1, total_stages - 1) if total_stages > 1 else 0
        if fraction < 0.33:
            phase = 'early'
        elif fraction < 0.66:
            phase = 'mid'
        else:
            phase = 'late'

        catalog = self._base_options_catalog()
        phase_candidates = list(catalog.get(character_type, {}).get(phase, []))

        # obtener tags del evento (si los hay)
        event_tags = event.get('tags', []) if isinstance(event, dict) else []

        # 1) Filtrar candidatos que explícitamente tengan al menos un tag en común y tengan texto
        def tag_match(cand: Dict[str, Any]) -> bool:
            ctags = cand.get('tags', [])
            return any(t in ctags for t in event_tags) if ctags and event_tags else False

        filtered = [cand for cand in phase_candidates if tag_match(cand) and 'text' in cand]

        # Si no hay suficientes, buscar en otras fases
        if len(filtered) < 3:
            other_phases = ['early', 'mid', 'late']
            for p in other_phases:
                if p == phase:
                    continue
                extras = list(catalog.get(character_type, {}).get(p, []))
                for e in extras:
                    if tag_match(e) and e not in filtered and 'text' in e:
                        filtered.append(e)
                    if len(filtered) >= 3:
                        break
                if len(filtered) >= 3:
                    break

        # Si siguen faltando, crear opciones genéricas estrictamente relacionadas con el evento, asegurando textos únicos
        generic_count = 1
        while len(filtered) < 3:
            primary_tag = event_tags[0] if event_tags else None
            if primary_tag in ('usb', 'physical'):
                base_text = f'No manipular dispositivos externos y reportar a IT desde {location}.'
                generic = {
                    'text': base_text,
                    'tags': ['usb', 'physical'],
                    'risk': 'bajo', 'time': 1, 'success': 95,
                    'effect_on_state': {'success': {}, 'failure': {'alert_level': +1}},
                    'outcome_text': {'success': 'IT recibió el USB y lo analizó.', 'failure': 'IT no respondió a tiempo.'}
                }
            elif primary_tag in ('phishing', 'links', 'correo'):
                base_text = f'No abrir enlaces del remitente y reportar desde {location}.'
                generic = {
                    'text': base_text,
                    'tags': ['phishing'],
                    'risk': 'bajo', 'time': 1, 'success': 90,
                    'effect_on_state': {'success': {'pistas': +1}, 'failure': {'alert_level': +1}},
                    'outcome_text': {'success': 'Reportaste y se bloqueó al remitente.', 'failure': 'El enlace causó problemas a otros usuarios.'}
                }
            elif primary_tag in ('exfiltration', 'database', 'tráfico'):
                base_text = f'Correlacionar logs y alertar al SOC desde {location}.'
                generic = {
                    'text': base_text,
                    'tags': ['logs', 'exfiltration'],
                    'risk': 'medio', 'time': 2, 'success': 85,
                    'effect_on_state': {'success': {'pistas': +1}, 'failure': {'alert_level': +1}},
                    'outcome_text': {'success': 'Se obtuvieron pistas útiles.', 'failure': 'Faltaron logs para confirmar.'}
                }
            else:
                base_text = f'Reportar la anomalía desde {location} a IT.'
                generic = {
                    'text': base_text,
                    'tags': ['report'],
                    'risk': 'bajo', 'time': 1, 'success': 85,
                    'effect_on_state': {'success': {}, 'failure': {'alert_level': +1}},
                    'outcome_text': {'success': 'IT recibió el reporte.', 'failure': 'IT no respondió a tiempo.'}
                }
            # Si el texto ya existe, hacer único
            texts_in_filtered = [o['text'] for o in filtered]
            text = generic['text']
            while text in texts_in_filtered:
                generic_count += 1
                text = f"{base_text} (alternativa {generic_count})"
            generic['text'] = text
            filtered.append(generic)

        # Eliminar duplicados por texto (mantener el primero)
        unique_options = []
        seen_texts = set()
        for opt in filtered:
            t = opt.get('text', None)
            if t and t not in seen_texts:
                unique_options.append(opt)
                seen_texts.add(t)
            if len(unique_options) >= 3:
                break

        # Final tweak: asegurar keys
        for opt in unique_options:
            opt.setdefault('risk', 'medio')
            opt.setdefault('time', 1)
            opt.setdefault('success', 50)
            opt.setdefault('effect_on_state', {})
            opt.setdefault('outcome_text', {'success': 'Operación completada.', 'failure': 'Operación fallida.'})

        # Siempre devolver exactamente 3 opciones
        while len(unique_options) < 3:
            # Agregar opción genérica de respaldo si por alguna razón faltan
            fallback = {
                'text': f'Reportar la situación desde {location} a IT.',
                'tags': ['report'],
                'risk': 'bajo', 'time': 1, 'success': 85,
                'effect_on_state': {'success': {}, 'failure': {'alert_level': +1}},
                'outcome_text': {'success': 'IT recibió el reporte.', 'failure': 'IT no respondió a tiempo.'}
            }
            if fallback['text'] not in seen_texts:
                unique_options.append(fallback)
                seen_texts.add(fallback['text'])
            else:
                # Si ya existe, modificar el texto para hacerlo único
                unique_options.append({**fallback, 'text': fallback['text'] + f' (alternativa {len(unique_options)+1})'})
            if len(unique_options) >= 3:
                break

        return unique_options

    # (Eliminado el bloque de datos corrupto)

    # -------------------------
    # Generación de nueva historia
    # -------------------------
    def generate_new_story(self, character_type: str, seed: Optional[int] = None) -> Dict[str, Any]:
        """Genera una historia completa y coherente para el personaje dado."""
        if seed is not None:
            random.seed(seed)
        if character_type not in ('usuario', 'hacker', 'cyberdelincuente'):
            raise ValueError("character_type debe ser 'usuario', 'hacker' o 'cyberdelincuente'")

        # Seleccionar solo escenarios válidos para el personaje
        valid_scenarios = [s for s in self.story_templates['scenarios'] if s['objectives'].get(character_type, 'N/A') != 'N/A']
        if not valid_scenarios:
            raise ValueError(f"No hay escenarios válidos para el personaje {character_type}")
        scenario = random.choice(valid_scenarios)
        goal, antagonist, key_item = self._create_thread(scenario, character_type)

        # Estado persistente que influirá en eventos y descripciones
        state = {
            'alert_level': 0,           # 0=bajo, 1=medio, 2=alto, 3=crítico
            'pistas': 0,                # número de pistas recogidas
            'tiene_objeto_clave': False,
            'current_location': scenario['locations'][0]['name'],
            'aliados': [],
            'compromised_hosts': 0,     # número de hosts comprometidos detectados
            'credentials_leaked': 0     # credenciales potencialmente filtradas
        }

        # Número de etapas entre 4 y 6 para mantener historias compactas y coherentes
        num_stages = random.randint(4, 6)
        story_stages: List[Dict[str, Any]] = []

        used_events = set()

        for i in range(num_stages):
            # elegir locación conectada a la actual (mover ubicación primero para progresión real)
            location = self._choose_location(state['current_location'], scenario)
            state['current_location'] = location

            # elegir evento coherente con el estado y la fase actual (ahora devuelve evento con tags)
            # Evitar repetir eventos en la misma historia
            event = None
            attempts = 0
            while attempts < 10:
                candidate = self._choose_event_by_state(state, stage_num=i)
                event_id = candidate['text']
                if event_id not in used_events:
                    event = candidate
                    used_events.add(event_id)
                    break
                attempts += 1
            if event is None:
                # Si no se pudo evitar, usar cualquiera
                event = self._choose_event_by_state(state, stage_num=i)

            # generar descripción que refiera al estado, objetivo y antagonista
            description = self._generate_description(scenario, location, event, i, state, goal, antagonist, key_item, show_objective=(i==0))

            # generar opciones según personaje, fase y contexto (location + event + state)
            options = self._generate_options(character_type, i, num_stages, scenario, location, event, state)

            # Aplicar los efectos del evento al estado (antes de que el jugador elija)
            state = self._apply_event_effects(state, event)

            # Insertar snapshot del estado (útil para debugging o UI)
            stage_entry = {
                'stage': i + 1,
                'location': location,
                'event': event,
                'description': description,
                'options': options,
                'state_snapshot': state.copy()
            }

            story_stages.append(stage_entry)

        # Guardar historia y preparar control de etapas
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
        return self.current_story

    # -------------------------
    # Hilo conductor (goal, antagonist, key item)
    # -------------------------
    def _create_thread(self, scenario: Dict[str, Any], character_type: str) -> Tuple[str, str, str]:
        """Crea objetivo concreto, antagonista y objeto clave ligados al escenario y al personaje."""
        base_goal = scenario['objectives'].get(character_type, 'N/A')
        # Usuario: defensa personal
        if character_type == 'usuario':
            goal = base_goal
            key_item = 'copia de seguridad local (backup)'
            antagonist = 'Campaña de Ingeniería Social'
        # Hacker ético: defensa y respuesta
        elif character_type == 'hacker':
            goal = base_goal
            if scenario['id'] == 'hacker_empresa':
                key_item = 'Playbook de Respuesta y Kit de Concientización'
            else:
                key_item = 'Herramientas de monitoreo y scripts de automatización'
            antagonist = 'Atacante persistente (APT) y errores humanos'
        # Ciberdelincuente: ofensiva
        else:  # cyberdelincuente
            goal = base_goal
            if scenario['id'] == 'ciberdelincuente_ataque':
                key_item = 'USB con payload, plantillas de phishing y exploits'
            else:
                key_item = 'Infraestructura de C2 y credenciales robadas'
            antagonist = 'Equipo de Seguridad y sistemas de defensa'
        return goal, antagonist, key_item

    # -------------------------
    # Selección de eventos y locaciones coherentes
    # -------------------------
    def _choose_event_by_state(self, state: Dict[str, Any], stage_num: int = 0) -> Dict[str, Any]:
        """Selecciona un evento relevante según el personaje y la dificultad."""
        events = self.story_templates['events']
        character = self.current_story['character'] if hasattr(self, 'current_story') and self.current_story else 'usuario'
        # Filtrar eventos por tag de personaje
        relevant_events = [e for e in events if character in e.get('tags', [])]
        if not relevant_events:
            relevant_events = events  # fallback

        weighted = []
        alert = state.get('alert_level', 0)
        pistas = state.get('pistas', 0)

        # Preferencias por fase narrativa
        if stage_num < 2:  # early
            for e in relevant_events:
                weight = 3 if 'usb' in e['tags'] or 'phishing' in e['tags'] or 'correo' in e['tags'] else 1
                weighted.extend([e] * weight)
        elif stage_num < 4:  # mid
            for e in relevant_events:
                weight = 2
                if any(k in e['tags'] for k in ('logs', 'firewall', 'ransomware', 'exfiltration')):
                    weight = 4
                weighted.extend([e] * weight)
        else:  # late
            for e in relevant_events:
                weight = 3 if any(k in e['tags'] for k in ('ransomware', 'alert', 'exfiltration')) else 1
                weighted.extend([e] * weight)

        # Si alerta alta/critica, reforzar eventos detectores
        if alert >= 2:
            for e in relevant_events:
                if any(w in e['tags'] for w in ('alert', 'detect', 'ransomware', 'compromet')):
                    weighted.extend([e] * 3)

        # Si no hay pistas, favorecer eventos que las provean
        if pistas == 0:
            for e in relevant_events:
                if any(w in e['tags'] for w in ('pistas', 'logs', 'reporta', 'exfiltration')):
                    weighted.extend([e] * 2)

        return random.choice(weighted) if weighted else random.choice(relevant_events)

    def _choose_location(self, current_location: str, scenario: Dict[str, Any]) -> str:
        """Elige la siguiente ubicación basándose en las conexiones del scenario."""
        names = [loc['name'] for loc in scenario['locations']]
        loc_map = {loc['name']: loc for loc in scenario['locations']}
        if current_location not in loc_map:
            return names[0]

        connections = loc_map[current_location]['connections']
        if not connections:
            return random.choice(names)

        if random.random() < 0.85:
            return random.choice(connections)
        else:
            return random.choice(names)

    # -------------------------
    # Aplicación de efectos de eventos y opciones al state
    # -------------------------
    def _apply_event_effects(self, state: Dict[str, Any], event: Dict[str, Any]) -> Dict[str, Any]:
        """Aplica efectos contenidos en un evento al state."""
        new_state = state.copy()
        effect = event.get('effect', {}) or {}
        for key, delta in effect.items():
            if key in new_state and isinstance(new_state[key], int):
                new_state[key] = max(0, new_state[key] + int(delta))
            else:
                new_state[key] = delta
        return new_state

    def _apply_option_effects(self, state: Dict[str, Any], option: Dict[str, Any], success: bool) -> Dict[str, Any]:
        """Aplica efectos de una opción elegida por el jugador."""
        new_state = state.copy()
        effects = option.get('effect_on_state', {}) or {}
        if isinstance(effects, dict) and ('success' in effects or 'failure' in effects):
            chosen_effect = effects['success'] if success else effects['failure']
        else:
            chosen_effect = effects

        for key, delta in chosen_effect.items():
            if key in new_state and isinstance(new_state[key], int):
                new_state[key] = max(0, new_state[key] + int(delta))
            else:
                new_state[key] = chosen_effect[key]
        return new_state

    # -------------------------
    # Descripciones realistas y conectadas al estado
    # -------------------------
    def _generate_description(self,
                              scenario: Dict[str, Any],
                              location: str,
                              event: Dict[str, Any],
                              stage_num: int,
                              state: Dict[str, Any],
                              goal: str,
                              antagonist: str,
                              key_item: str,
                              show_objective: bool = False) -> str:
        parts: List[str] = []
        parts.append(f"Ubicación: {location}.")
        parts.append(event['text'])

        if state.get('alert_level', 0) >= 3:
            parts.append("Alerta crítica: se ha detectado un incidente grave — actúa con prioridad.")
        elif state.get('alert_level', 0) == 2:
            parts.append("Alerta alta: actividad sospechosa persistente.")
        elif state.get('alert_level', 0) == 1:
            parts.append("Vigilancia aumentada: revisa tus acciones y reporta anomalías.")

        pistas = state.get('pistas', 0)
        if pistas > 0:
            parts.append(f"Tienes {pistas} pista(s) relevantes que ayudan a {goal.split('.')[0].lower()}.")

        # if show_objective:
        #     parts.append(f"Objetivo: {goal}")

        parts.append("¿Qué haces ahora?")
        return " ".join(parts)

    # -------------------------
    # Opciones por personaje (con tags) - usadas por la selección contextual
    # -------------------------
    def _base_options_catalog(self) -> Dict[str, Dict[str, List[Dict[str, Any]]]]:
        """Catálogo centralizado de opciones con tags que describen cuando son relevantes.
        Cada opción tiene 'tags' lista (ej: ['phishing','credentials'])
        """
        return {
            'usuario': {
                'early': [
                    {
                        'text': 'Verificar remitente y no abrir el enlace; reportarlo a soporte.',
                        'tags': ['phishing', 'correo', 'links'],
                        'risk': 'bajo',
                        'time': 1,
                        'success': 90,
                        'effect_on_state': {'success': {'pistas': +1}, 'failure': {'alert_level': +1}},
                        'outcome_text': {'success': 'Reportaste el intento y el equipo bloqueó el remitente.', 'failure': 'El reporte tardó y algunos empleados cayeron en el engaño.'}
                    },
                    {
                        'text': 'Hacer clic en el enlace para ver de qué se trata.',
                        'tags': ['phishing', 'links'],
                        'risk': 'alto',
                        'time': 1,
                        'success': 20,
                        'effect_on_state': {'success': {'credentials_leaked': +1}, 'failure': {'alert_level': +2}},
                        'outcome_text': {'success': 'Sincronizaste sin darte cuenta credenciales (mal).', 'failure': 'El enlace no funcionó, pero generó logs.'}
                    },
                    {
                        'text': 'Activar autenticación en dos pasos en la cuenta afectada.',
                        'tags': ['phishing', 'credentials', 'mfa'],
                        'risk': 'bajo',
                        'time': 2,
                        'success': 85,
                        'effect_on_state': {'success': {'alert_level': -1}, 'failure': {}},
                        'outcome_text': {'success': 'MFA activada; reduce la probabilidad de compromiso.', 'failure': 'No pudiste completar la activación ahora.'}
                    }
                ],
                'mid': [
                    {
                        'text': 'No conectar el USB y llevarlo a IT para análisis.',
                        'tags': ['usb', 'physical'],
                        'risk': 'bajo',
                        'time': 1,
                        'success': 95,
                        'effect_on_state': {'success': {}, 'failure': {'alert_level': +1}},
                        'outcome_text': {'success': 'IT analiza el USB y confirma que es malicioso.', 'failure': 'IT no está disponible y alguien más lo conectó.'}
                    },
                    {
                        'text': 'Conectar el USB en tu equipo y abrir archivos.',
                        'tags': ['usb', 'physical', 'malware'],
                        'risk': 'alto',
                        'time': 1,
                        'success': 10,
                        'effect_on_state': {'success': {'compromised_hosts': +1}, 'failure': {'alert_level': +2}},
                        'outcome_text': {'success': 'El USB ejecutó un payload y comprometió tu equipo.', 'failure': 'El USB parecía inofensivo pero generó logs sospechosos.'}
                    },
                    {
                        'text': 'Actualizar tu sistema y hacer backup local de archivos sensibles.',
                        'tags': ['patch', 'backup'],
                        'risk': 'bajo',
                        'time': 2,
                        'success': 90,
                        'effect_on_state': {'success': {'pistas': +1}, 'failure': {}},
                        'outcome_text': {'success': 'Actualizaste y creaste respaldo; estarás mejor protegido.', 'failure': 'La actualización falló por falta de permisos.'}
                    }
                ],
                'late': [
                    {
                        'text': 'Cambiar contraseñas y revisar sesiones activas.',
                        'tags': ['credentials', 'mfa'],
                        'risk': 'bajo',
                        'time': 1,
                        'success': 85,
                        'effect_on_state': {'success': {'credentials_leaked': -1}, 'failure': {}},
                        'outcome_text': {'success': 'Contraseñas actualizadas y sesiones sospechosas cerradas.', 'failure': 'Algunos servicios no permitieron cambio inmediato.'}
                    },
                    {
                        'text': 'Seguir trabajando como si nada (ignorar el riesgo).',
                        'tags': ['ignore', 'risky'],
                        'risk': 'alto',
                        'time': 1,
                        'success': 10,
                        'effect_on_state': {'success': {}, 'failure': {'compromised_hosts': +1}},
                        'outcome_text': {'success': 'Suerte estuvo de tu lado por ahora.', 'failure': 'Tu equipo fue comprometido por no actuar.'}
                    }
                ]
            },
            'hacker': {
                'early': [
                    {
                        'text': 'Recolectar y correlacionar logs para identificar IOCs.',
                        'tags': ['logs', 'exfiltration', 'detection'],
                        'risk': 'bajo',
                        'time': 2,
                        'success': 85,
                        'effect_on_state': {'success': {'pistas': +2}, 'failure': {'alert_level': +1}},
                        'outcome_text': {'success': 'Encontraste indicadores de compromiso claros.', 'failure': 'Los logs estaban incompletos; necesitas más datos.'}
                    },
                    {
                        'text': 'Aislar el host sospechoso de la red para análisis forense.',
                        'tags': ['isolate', 'forensics'],
                        'risk': 'medio',
                        'time': 1,
                        'success': 80,
                        'effect_on_state': {'success': {'compromised_hosts': -1}, 'failure': {'alert_level': +1}},
                        'outcome_text': {'success': 'El aislamiento evita más exfiltración.', 'failure': 'El aislamiento no fue completo y el atacante persistió.'}
                    }
                ],
                'mid': [
                    {
                        'text': 'Aplicar mitigación: revocar credenciales comprometidas y rotar claves.',
                        'tags': ['credentials', 'rotate'],
                        'risk': 'medio',
                        'time': 2,
                        'success': 80,
                        'effect_on_state': {'success': {'credentials_leaked': -1}, 'failure': {'alert_level': +1}},
                        'outcome_text': {'success': 'Credenciales rotadas y acceso del atacante restringido.', 'failure': 'Algunas credenciales no se pudieron rotar a tiempo.'}
                    },
                    {
                        'text': 'Restaurar desde backups verificados y validar integridad.',
                        'tags': ['backup', 'restore'],
                        'risk': 'bajo',
                        'time': 3,
                        'success': 85,
                        'effect_on_state': {'success': {'compromised_hosts': -1}, 'failure': {'alert_level': +2}},
                        'outcome_text': {'success': 'Restauración exitosa y sistemas volverán a la normalidad.', 'failure': 'Backups dañados o incompletos.'}
                    }
                ],
                'late': [
                    {
                        'text': 'Implementar reglas IDS/IPS y bloqueos a nivel de firewall.',
                        'tags': ['ids', 'firewall'],
                        'risk': 'bajo',
                        'time': 2,
                        'success': 90,
                        'effect_on_state': {'success': {'alert_level': -1}, 'failure': {'alert_level': +1}},
                        'outcome_text': {'success': 'Se redujo el ruido y se contuvo la campaña.', 'failure': 'El atacante cambió tácticas y el bloqueo fue insuficiente.'}
                    },
                    {
                        'text': 'Generar reporte técnico y coordinar comunicación con stakeholders.',
                        'tags': ['report', 'comms'],
                        'risk': 'bajo',
                        'time': 1,
                        'success': 75,
                        'effect_on_state': {'success': {}, 'failure': {}},
                        'outcome_text': {'success': 'La comunicación reduce impacto reputacional.', 'failure': 'La comunicación fue lenta y generó incertidumbre.'}
                    }
                ]
            },
            'cyberdelincuente': {
                'early': [
                    {
                        'text': 'Enviar phishing dirigido (spear-phishing) a empleados clave.',
                        'tags': ['phishing', 'spear'],
                        'risk': 'medio',
                        'time': 2,
                        'success': 60,
                        'effect_on_state': {'success': {'credentials_leaked': +1}, 'failure': {'alert_level': +1}},
                        'outcome_text': {'success': 'Algunos empleados cayeron y entregaron credenciales.', 'failure': 'La campaña fue detectada por filtros anti-spam.'}
                    },
                    {
                        'text': 'Dejar USB malicioso en un lugar visible esperando que alguien lo conecte.',
                        'tags': ['usb', 'physical'],
                        'risk': 'alto',
                        'time': 3,
                        'success': 45,
                        'effect_on_state': {'success': {'compromised_hosts': +1}, 'failure': {'alert_level': +1}},
                        'outcome_text': {'success': 'Un empleado conectó el USB y se logró acceso inicial.', 'failure': 'Nadie lo conectó y fue recogido por seguridad.'}
                    }
                ],
                'mid': [
                    {
                        'text': 'Escalada lateral usando credenciales robadas para acceder a la base de datos.',
                        'tags': ['lateral', 'exfiltration', 'database'],
                        'risk': 'alto',
                        'time': 3,
                        'success': 65,
                        'effect_on_state': {'success': {'pistas': +2, 'compromised_hosts': +1}, 'failure': {'alert_level': +2}},
                        'outcome_text': {'success': 'Accediste a la base de datos y comenzaste la exfiltración.', 'failure': 'El control de accesos impidió la escalada.'}
                    },
                    {
                        'text': 'Instalar backdoor persistente para acceso futuro.',
                        'tags': ['backdoor', 'persistence'],
                        'risk': 'alto',
                        'time': 3,
                        'success': 55,
                        'effect_on_state': {'success': {'tiene_objeto_clave': True}, 'failure': {'alert_level': +2}},
                        'outcome_text': {'success': 'Backdoor instalado; mantienes acceso.', 'failure': 'El backdoor fue detectado y limpiado.'}
                    }
                ],
                'late': [
                    {
                        'text': 'Exfiltrar datos y cifrar backups para pedir rescate.',
                        'tags': ['exfiltration', 'ransomware', 'rescate'],
                        'risk': 'alto',
                        'time': 3,
                        'success': 70,
                        'effect_on_state': {'success': {'credentials_leaked': +2, 'compromised_hosts': +1}, 'failure': {'alert_level': +3}},
                        'outcome_text': {'success': 'Datos exfiltrados y cifrados; la empresa sufre interrupciones.', 'failure': 'El intento fue detectado y frenado por IDS.'}
                    },
                    {
                        'text': 'Borrar rastros y preparar rutas de salida seguras.',
                        'tags': ['cleanup', 'logs'],
                        'risk': 'medio',
                        'time': 2,
                        'success': 60,
                        'effect_on_state': {'success': {}, 'failure': {'alert_level': +1}},
                        'outcome_text': {'success': 'Limpiaste logs y redujiste evidencia.', 'failure': 'Dejaste huellas que más tarde permiten tu identificación.'}
                    }
                ]
            }
        }

    # -------------------------
    # Selección estricta de 3 opciones contextuales
    # -------------------------
    def _generate_options(self,
                          character_type: str,
                          stage: int,
                          total_stages: int,
                          scenario: Dict[str, Any],
                          location: str,
                          event: Dict[str, Any],
                          state: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Devuelve exactamente 3 opciones contextuales relacionadas con el event.tags."""
        # Determinar fase (early/mid/late)
        fraction = stage / max(1, total_stages - 1) if total_stages > 1 else 0
        if fraction < 0.33:
            phase = 'early'
        elif fraction < 0.66:
            phase = 'mid'
        else:
            phase = 'late'

        catalog = self._base_options_catalog()
        phase_candidates = list(catalog.get(character_type, {}).get(phase, []))

        # obtener tags del evento (si los hay)
        event_tags = event.get('tags', []) if isinstance(event, dict) else []

        # 1) Filtrar candidatos que explícitamente tengan al menos un tag en común
        def tag_match(cand: Dict[str, Any]) -> bool:
            ctags = cand.get('tags', [])
            return any(t in ctags for t in event_tags) if ctags and event_tags else False

        # Solo opciones con tags en común
        filtered = [cand for cand in phase_candidates if tag_match(cand)]

        # Si no hay suficientes, buscar en otras fases
        if len(filtered) < 3:
            other_phases = ['early', 'mid', 'late']
            for p in other_phases:
                if p == phase:
                    continue
                extras = list(catalog.get(character_type, {}).get(p, []))
                for e in extras:
                    if tag_match(e) and e not in filtered:
                        filtered.append(e)
                    if len(filtered) >= 3:
                        break
                if len(filtered) >= 3:
                    break

        # Si siguen faltando, crear opciones genéricas estrictamente relacionadas con el evento, usando variantes y evitando repeticiones
        generic_variants = []
        if event_tags:
            if any(tag in event_tags for tag in ('usb', 'physical')):
                generic_variants = [
                    f'No manipular dispositivos externos y reportar a IT desde {location}.',
                    f'Colocar el USB en una bolsa antiestática y avisar a seguridad en {location}.',
                    f'Ignorar el dispositivo y advertir a los compañeros en {location}.',
                ]
            elif any(tag in event_tags for tag in ('phishing', 'links', 'correo')):
                generic_variants = [
                    f'No abrir enlaces del remitente y reportar desde {location}.',
                    f'Bloquear al remitente y reenviar el correo a IT desde {location}.',
                    f'Eliminar el correo y advertir a los compañeros en {location}.',
                ]
            elif any(tag in event_tags for tag in ('exfiltration', 'database', 'tráfico')):
                generic_variants = [
                    f'Correlacionar logs y alertar al SOC desde {location}.',
                    f'Contactar al área de seguridad para revisión de logs en {location}.',
                    f'Generar un informe de actividad sospechosa desde {location}.',
                ]
        if not generic_variants:
            generic_variants = [
                f'Reportar la anomalía desde {location} a IT.',
                f'Contactar a soporte para revisión presencial en {location}.',
                f'Ignorar la anomalía y continuar trabajando en {location}.',
            ]
        # Agregar variantes que no estén ya en filtered
        texts_in_filtered = [o['text'] for o in filtered]
        for variant in generic_variants:
            if len(filtered) >= 3:
                break
            if variant not in texts_in_filtered:
                generic = {
                    'text': variant,
                    'tags': event_tags if event_tags else ['report'],
                    'risk': 'medio', 'time': 1, 'success': 80,
                    'effect_on_state': {'success': {}, 'failure': {'alert_level': +1}},
                    'outcome_text': {'success': 'Acción realizada y reportada.', 'failure': 'No hubo respuesta a tiempo.'}
                }
                filtered.append(generic)

        # Final tweak: asegurar keys
        for opt in filtered[:3]:
            opt.setdefault('risk', 'medio')
            opt.setdefault('time', 1)
            opt.setdefault('success', 50)
            opt.setdefault('effect_on_state', {})
            opt.setdefault('outcome_text', {'success': 'Operación completada.', 'failure': 'Operación fallida.'})

        return filtered[:3]

    # -------------------------
    # Métodos de control de etapas y resolución
    # -------------------------
    def get_current_stage(self) -> Optional[Dict[str, Any]]:
        if not self.current_story:
            return None
        stages = self.current_story.get('stages', [])
        if 0 <= self.stage_index < len(stages):
            return stages[self.stage_index]
        return None

    def is_story_complete(self) -> bool:
        if not self.current_story:
            return True
        return self.stage_index >= len(self.current_story.get('stages', []))

    def resolve_option(self, current_state: Dict[str, Any], option: Dict[str, Any]) -> Dict[str, Any]:
        """Resuelve una opción: aplica efectos y avanza etapa (por defecto)."""
        chance = option.get('success', 50)
        roll = random.randint(1, 100)
        success = roll <= chance

        # Aplica efectos
        state = self.current_story.get('final_state', {}).copy() if self.current_story else current_state.copy()
        new_state = self._apply_option_effects(state, option, success)
        if self.current_story:
            self.current_story['final_state'] = new_state

        # Actualizar snapshot de la etapa actual
        if self.current_story and 0 <= self.stage_index < len(self.current_story['stages']):
            stage = self.current_story['stages'][self.stage_index]
            stage['state_snapshot'] = new_state.copy()
            outcome_text = option.get('outcome_text', {})
            stage_result_text = outcome_text.get('success' if success else 'failure', '') if isinstance(outcome_text, dict) else str(outcome_text)
            stage.setdefault('results', []).append({'choice_text': option.get('text', ''), 'success': success, 'text': stage_result_text})

        # Avanzar (por defecto avance siempre)
        self.stage_index += 1
        story_complete = self.is_story_complete()
        next_stage = self.get_current_stage() if not story_complete else None

        outcome_text = option.get('outcome_text', {})
        text = outcome_text.get('success' if success else 'failure', '') if isinstance(outcome_text, dict) else str(outcome_text)

        return {'success': success, 'new_state': new_state, 'result_text': text, 'roll': roll, 'chance': chance, 'story_complete': story_complete, 'next_stage': next_stage}
