#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para crear un favicon.ico para Proyecto Pilar
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_favicon():
    """Crear favicon de 32x32 con la letra 'P' de PILAR"""
    
    # Color azul EBPB2 (azul corporativo)
    bg_color = (41, 82, 156, 255)  # #29529C
    text_color = (255, 255, 255, 255)  # Blanco
    
    # Crear imagen de 32x32 píxeles
    img = Image.new('RGBA', (32, 32), bg_color)
    draw = ImageDraw.Draw(img)
    
    # Intentar usar una fuente del sistema
    try:
        font = ImageFont.truetype('arial.ttf', 24)
    except:
        try:
            font = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 24)
        except:
            try:
                font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 24)
            except:
                font = ImageFont.load_default()
    
    # Dibujar 'P' centrada
    draw.text((7, 2), 'P', fill=text_color, font=font)
    
    # Guardar como ICO en varios tamaños
    output_path = os.path.join('static', 'img', 'favicon.ico')
    
    # Crear también versiones en diferentes tamaños
    sizes = [(16, 16), (32, 32), (48, 48)]
    icons = []
    
    for size in sizes:
        icon = img.resize(size, Image.Resampling.LANCZOS)
        icons.append(icon)
    
    # Guardar como ICO con múltiples tamaños
    icons[0].save(output_path, format='ICO', sizes=[(16, 16), (32, 32), (48, 48)])
    
    print(f'✅ Favicon creado exitosamente en: {output_path}')
    print(f'   Tamaños incluidos: 16x16, 32x32, 48x48')

if __name__ == '__main__':
    try:
        create_favicon()
    except ImportError:
        print('❌ Error: Se requiere Pillow (PIL)')
        print('Instalar con: pip install Pillow')
    except Exception as e:
        print(f'❌ Error creando favicon: {e}')
