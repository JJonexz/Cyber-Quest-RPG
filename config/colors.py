# config/colors.py - VERSION 2.0
# Paleta de colores profesional basada en especificaciones CSS

COLORS = {
    # Colores base
    'bg': '#062747',
    'modal': '#051e38',
    'text': '#f1f1f1',
    'text_secondary': '#ffffff',
    'text_tertiary': '#000000',
    
    # Colores de acento
    'accent': '#00b894',
    'primary': '#4a0086',
    'secondary': '#e67e22',
    
    # Backgrounds
    'header_bg': '#051925',
    'footer_bg': '#072131',
    'footer_bg2': '#061c2a',
    'container_bg': 'rgba(0, 0, 0, 0.6)',
    'container_bg2': '#00435e',
    'subheader_bg': 'rgba(255, 255, 255, 0.05)',
    
    # Dropdown y shadows
    'dropdown_bg': '#051e38',
    'dropdown_shadow': 'rgba(0, 162, 255, 0.247)',
    
    # Borders y hover
    'border': 'rgba(255, 255, 255, 0.1)',
    'hover': 'rgba(255, 255, 255, 0.05)',
    
    # Efectos y sombras
    'shadow_glow': 'rgba(0, 255, 255, 0.3)',
    'glow_accent': 'rgba(0, 184, 148, 0.4)',
    'glow_primary': 'rgba(74, 0, 134, 0.5)',
    
    # Sombras (strings para usar en efectos visuales)
    'shadow_sm': '0 2px 8px rgba(0, 0, 0, 0.15)',
    'shadow_md': '0 4px 16px rgba(0, 0, 0, 0.2)',
    'shadow_lg': '0 8px 32px rgba(0, 0, 0, 0.3)',
    'shadow_xl': '0 12px 48px rgba(0, 0, 0, 0.4)',
    
    # Estados
    'success': '#00b894',
    'warning': '#f39c12',
    'danger': '#e74c3c',
    'info': '#3498db',
    
    # Modo claro (opcional, para futura implementación)
    'light_mode': {
        'bg': '#e3f2fd',
        'modal': '#ffffff',
        'header_bg': '#0d47a1',
        'text': '#0d1b2a',
        'accent': '#01579b',
        'container_bg': '#ffffff',
        'container_bg2': '#f1f8ff',
        'border': 'rgba(13, 71, 161, 0.15)'
    }
}

# Configuración de estilo
STYLE = {
    'border_radius': 12,
    'transition': 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
    'padding_standard': 20,
    'padding_large': 40,
    'spacing_small': 5,
    'spacing_medium': 10,
    'spacing_large': 20
}