#!/usr/bin/env python3
"""
Create a HueGenius logo representing color psychology and culture
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_huegenius_logo():
    """Create a logo for HueGenius app"""
    
    # Create a square canvas
    size = 400
    img = Image.new('RGBA', (size, size), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    
    # Define colors representing different cultures and psychology
    colors = [
        (255, 0, 0),      # Red - passion, energy
        (0, 0, 255),      # Blue - trust, calm
        (255, 255, 0),    # Yellow - optimism, creativity
        (0, 128, 0),      # Green - nature, balance
        (128, 0, 128),    # Purple - luxury, mystery
        (255, 165, 0),    # Orange - enthusiasm, warmth
        (255, 192, 203),  # Pink - love, compassion
        (0, 255, 255),    # Cyan - clarity, freshness
    ]
    
    # Create a circular color wheel pattern
    center = size // 2
    radius = 150
    
    # Draw concentric circles with different colors
    for i, color in enumerate(colors):
        # Create a gradient effect by varying the radius
        inner_radius = radius - (i * 15)
        outer_radius = radius - (i * 15) + 20
        
        if inner_radius > 0:
            # Draw a segment of the circle
            start_angle = i * 45  # 45 degrees per color
            end_angle = (i + 1) * 45
            
            # Create a pie slice
            draw.pieslice([center - outer_radius, center - outer_radius, 
                          center + outer_radius, center + outer_radius],
                         start_angle, end_angle, fill=color)
    
    # Add a brain/psychology symbol in the center
    brain_center = center
    brain_radius = 60
    
    # Draw a stylized brain shape
    draw.ellipse([brain_center - brain_radius, brain_center - brain_radius,
                  brain_center + brain_radius, brain_center + brain_radius],
                 fill=(255, 255, 255, 200), outline=(0, 0, 0, 255), width=3)
    
    # Add brain-like curves
    for i in range(3):
        y_offset = -20 + i * 20
        draw.arc([brain_center - brain_radius + 10, brain_center - brain_radius + y_offset,
                  brain_center + brain_radius - 10, brain_center + brain_radius + y_offset],
                 0, 180, fill=(0, 0, 0, 255), width=2)
    
    # Add cultural symbols around the circle
    cultural_symbols = ['★', '●', '◆', '▲', '■', '♦', '♠', '♥']
    symbol_radius = radius + 40
    
    for i, symbol in enumerate(cultural_symbols):
        angle = i * 45
        import math
        x = center + symbol_radius * math.cos(math.radians(angle))
        y = center + symbol_radius * math.sin(math.radians(angle))
        
        # Draw cultural symbol
        draw.text((x - 10, y - 10), symbol, fill=(0, 0, 0, 255))
    
    # Add the text "HueGenius"
    try:
        # Try to use a nice font
        font_size = 24
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        # Fallback to default font
        font = ImageFont.load_default()
    
    # Draw the main title
    title_text = "HueGenius"
    title_bbox = draw.textbbox((0, 0), title_text, font=font)
    title_width = title_bbox[2] - title_bbox[0]
    title_x = (size - title_width) // 2
    title_y = size - 80
    
    draw.text((title_x, title_y), title_text, fill=(0, 0, 0, 255), font=font)
    
    # Draw the subtitle
    subtitle_text = "Color Psychology & Culture"
    subtitle_font_size = 16
    try:
        subtitle_font = ImageFont.truetype("arial.ttf", subtitle_font_size)
    except:
        subtitle_font = ImageFont.load_default()
    
    subtitle_bbox = draw.textbbox((0, 0), subtitle_text, font=subtitle_font)
    subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
    subtitle_x = (size - subtitle_width) // 2
    subtitle_y = size - 50
    
    draw.text((subtitle_x, subtitle_y), subtitle_text, fill=(100, 100, 100, 255), font=subtitle_font)
    
    # Save the logo
    logo_filename = "huegenius_logo.png"
    img.save(logo_filename, "PNG")
    
    print(f"✅ Created HueGenius logo: {logo_filename}")
    return logo_filename

def create_simple_logo():
    """Create a simpler logo using basic shapes"""
    
    # Create a square canvas
    size = 300
    img = Image.new('RGBA', (size, size), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    
    # Create a color wheel background
    center = size // 2
    radius = 120
    
    # Define colors
    colors = [
        (255, 0, 0),      # Red
        (255, 165, 0),    # Orange
        (255, 255, 0),    # Yellow
        (0, 255, 0),      # Green
        (0, 0, 255),      # Blue
        (128, 0, 128),    # Purple
    ]
    
    # Draw color segments
    for i, color in enumerate(colors):
        start_angle = i * 60
        end_angle = (i + 1) * 60
        
        # Draw pie slice
        draw.pieslice([center - radius, center - radius, 
                      center + radius, center + radius],
                     start_angle, end_angle, fill=color)
    
    # Add a white circle in the center
    inner_radius = 60
    draw.ellipse([center - inner_radius, center - inner_radius,
                  center + inner_radius, center + inner_radius],
                 fill=(255, 255, 255, 255), outline=(0, 0, 0, 255), width=3)
    
    # Add "HG" text in the center
    try:
        font = ImageFont.truetype("arial.ttf", 36)
    except:
        font = ImageFont.load_default()
    
    draw.text((center - 25, center - 15), "HG", fill=(0, 0, 0, 255), font=font)
    
    # Save the simple logo
    logo_filename = "huegenius_simple_logo.png"
    img.save(logo_filename, "PNG")
    
    print(f"✅ Created simple HueGenius logo: {logo_filename}")
    return logo_filename

if __name__ == "__main__":
    # Try to create the main logo
    try:
        create_huegenius_logo()
    except Exception as e:
        print(f"Error creating main logo: {e}")
        print("Creating simple logo instead...")
        create_simple_logo()
