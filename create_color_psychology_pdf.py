#!/usr/bin/env python3
"""
Color Psychology and Cultural Meanings PDF Generator
Creates a comprehensive PDF for testing the specialized RAG application
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import Color, HexColor
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
import os

def create_color_psychology_pdf():
    """Create a comprehensive PDF about color psychology and cultural meanings"""
    
    # Create the PDF document
    filename = "color_psychology_cultural_meanings.pdf"
    doc = SimpleDocTemplate(filename, pagesize=A4, topMargin=1*inch, bottomMargin=1*inch)
    
    # Get styles
    styles = getSampleStyleSheet()
    
    # Create custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        alignment=TA_CENTER,
        textColor=HexColor('#2c3e50')
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        spaceAfter=12,
        spaceBefore=20,
        textColor=HexColor('#34495e')
    )
    
    subheading_style = ParagraphStyle(
        'CustomSubHeading',
        parent=styles['Heading3'],
        fontSize=14,
        spaceAfter=8,
        spaceBefore=12,
        textColor=HexColor('#7f8c8d')
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=6,
        alignment=TA_JUSTIFY,
        leftIndent=0,
        rightIndent=0
    )
    
    # Content for the PDF
    content = []
    
    # Title
    content.append(Paragraph("The Complete Guide to Color Psychology and Cultural Meanings", title_style))
    content.append(Spacer(1, 20))
    
    # Introduction
    content.append(Paragraph("Introduction", heading_style))
    content.append(Paragraph("""
    Color is one of the most powerful tools in human communication, influencing our emotions, 
    decisions, and cultural understanding. This comprehensive guide explores the psychological 
    effects of colors and their diverse cultural meanings across different societies. Understanding 
    these concepts is crucial for designers, marketers, psychologists, and anyone interested in 
    the profound impact of color on human behavior and culture.
    """, body_style))
    
    # Primary Colors Psychology
    content.append(Paragraph("Primary Colors and Their Psychological Effects", heading_style))
    
    content.append(Paragraph("Red: The Color of Passion and Energy", subheading_style))
    content.append(Paragraph("""
    Red is the most emotionally intense color in the spectrum. Psychologically, red increases 
    heart rate, blood pressure, and respiration. It's associated with passion, love, anger, and 
    danger. In marketing, red creates urgency and is often used for clearance sales. Studies show 
    that red can enhance physical performance and increase appetite, which is why many restaurants 
    use red in their branding.
    """, body_style))
    
    content.append(Paragraph("Blue: The Color of Trust and Stability", subheading_style))
    content.append(Paragraph("""
    Blue is universally associated with trust, reliability, and calmness. It has a calming effect 
    on the mind and body, reducing blood pressure and heart rate. Blue is often used in corporate 
    branding to convey professionalism and dependability. However, blue can also be associated 
    with sadness and depression in certain contexts. It's the most popular color globally, 
    representing sky and water in nature.
    """, body_style))
    
    content.append(Paragraph("Yellow: The Color of Optimism and Creativity", subheading_style))
    content.append(Paragraph("""
    Yellow is the most visible color and stimulates mental activity. It's associated with happiness, 
    optimism, and creativity. Yellow can increase energy levels and stimulate the nervous system. 
    However, too much yellow can cause anxiety and agitation. In design, yellow is often used 
    to grab attention and convey warmth and friendliness.
    """, body_style))
    
    # Cultural Meanings
    content.append(PageBreak())
    content.append(Paragraph("Cultural Meanings of Colors Across Different Societies", heading_style))
    
    content.append(Paragraph("Red in Different Cultures", subheading_style))
    content.append(Paragraph("""
    <b>Western Cultures:</b> Red represents love, passion, danger, and stop signals. It's associated 
    with Valentine's Day and Christmas.<br/><br/>
    <b>Eastern Cultures:</b> In China, red symbolizes good luck, prosperity, and celebration. It's 
    the traditional color for weddings and New Year celebrations. In India, red represents purity 
    and is worn by brides.<br/><br/>
    <b>African Cultures:</b> Red often represents blood, life force, and spiritual power. It's 
    used in many traditional ceremonies and rituals.
    """, body_style))
    
    content.append(Paragraph("White in Different Cultures", subheading_style))
    content.append(Paragraph("""
    <b>Western Cultures:</b> White symbolizes purity, innocence, and peace. It's the traditional 
    color for weddings and represents cleanliness.<br/><br/>
    <b>Eastern Cultures:</b> In many Asian cultures, white is associated with death, mourning, 
    and funerals. It represents the end of life and spiritual transition.<br/><br/>
    <b>Middle Eastern Cultures:</b> White represents peace, purity, and divine light. It's 
    often worn during religious ceremonies and represents spiritual cleanliness.
    """, body_style))
    
    content.append(Paragraph("Black in Different Cultures", subheading_style))
    content.append(Paragraph("""
    <b>Western Cultures:</b> Black represents elegance, sophistication, and formality. It's also 
    associated with mourning, death, and evil.<br/><br/>
    <b>Eastern Cultures:</b> In China, black represents water, winter, and the unknown. It's 
    associated with mystery and the supernatural.<br/><br/>
    <b>African Cultures:</b> Black often represents the earth, fertility, and spiritual power. 
    It's considered a powerful and protective color.
    """, body_style))
    
    # Color in Marketing and Branding
    content.append(PageBreak())
    content.append(Paragraph("Color Psychology in Marketing and Branding", heading_style))
    
    content.append(Paragraph("Brand Color Strategies", subheading_style))
    content.append(Paragraph("""
    Successful brands carefully choose their colors based on psychological principles and 
    cultural considerations. McDonald's uses red and yellow to stimulate appetite and create 
    urgency. Facebook uses blue to convey trust and reliability. Starbucks uses green to 
    represent growth, nature, and relaxation. Understanding these principles helps businesses 
    create more effective marketing campaigns and brand identities.
    """, body_style))
    
    content.append(Paragraph("Color and Consumer Behavior", subheading_style))
    content.append(Paragraph("""
    Research shows that color can influence purchasing decisions by up to 85%. Warm colors 
    (red, orange, yellow) create urgency and impulse buying, while cool colors (blue, green, 
    purple) encourage careful consideration. The right color choice can increase brand recognition 
    by 80% and improve readability by 40%.
    """, body_style))
    
    # Color Therapy and Healing
    content.append(Paragraph("Color Therapy and Healing Applications", heading_style))
    
    content.append(Paragraph("Chromotherapy Principles", subheading_style))
    content.append(Paragraph("""
    Color therapy, or chromotherapy, uses specific colors to promote healing and well-being. 
    Red light therapy is used to increase circulation and energy. Blue light therapy helps 
    with sleep disorders and relaxation. Green is used for balance and harmony. Yellow 
    stimulates the nervous system and improves mood. Understanding these therapeutic 
    applications can help in designing healing environments and wellness programs.
    """, body_style))
    
    # Color in Interior Design
    content.append(PageBreak())
    content.append(Paragraph("Color Psychology in Interior Design", heading_style))
    
    content.append(Paragraph("Room-Specific Color Guidelines", subheading_style))
    content.append(Paragraph("""
    <b>Bedrooms:</b> Cool colors like blue and green promote relaxation and better sleep. 
    Avoid bright reds and oranges which can be stimulating.<br/><br/>
    <b>Kitchens:</b> Warm colors like yellow and orange stimulate appetite and create 
    a welcoming atmosphere.<br/><br/>
    <b>Living Rooms:</b> Neutral colors with warm accents create comfort and social 
    interaction.<br/><br/>
    <b>Bathrooms:</b> Light blues and greens create a spa-like, calming environment.
    """, body_style))
    
    # Color Combinations and Harmony
    content.append(Paragraph("Color Combinations and Psychological Effects", heading_style))
    
    content.append(Paragraph("Complementary Colors", subheading_style))
    content.append(Paragraph("""
    Complementary colors (opposite on the color wheel) create high contrast and visual 
    excitement. Red and green combinations create energy and tension. Blue and orange 
    combinations are calming yet vibrant. These combinations are effective for creating 
    focal points and drawing attention.
    """, body_style))
    
    content.append(Paragraph("Analogous Colors", subheading_style))
    content.append(Paragraph("""
    Analogous colors (next to each other on the color wheel) create harmony and unity. 
    Blue, blue-green, and green combinations are calming and natural. Red, red-orange, 
    and orange combinations are warm and energetic. These combinations work well for 
    creating cohesive, peaceful environments.
    """, body_style))
    
    # Gender and Color Preferences
    content.append(PageBreak())
    content.append(Paragraph("Gender Differences in Color Preferences", heading_style))
    
    content.append(Paragraph("Research Findings", subheading_style))
    content.append(Paragraph("""
    Studies show that men and women have different color preferences. Men tend to prefer 
    blue, green, and black, while women often prefer purple, pink, and lighter colors. 
    These preferences may be influenced by cultural conditioning, biological factors, 
    and personal experiences. Understanding these differences is important for 
    gender-targeted marketing and design.
    """, body_style))
    
    # Age and Color Psychology
    content.append(Paragraph("Age-Related Color Preferences", heading_style))
    
    content.append(Paragraph("Developmental Color Psychology", subheading_style))
    content.append(Paragraph("""
    Color preferences change throughout life. Children are drawn to bright, saturated colors 
    like red, yellow, and blue. Teenagers often prefer bold, contrasting colors. Adults 
    tend to prefer more muted, sophisticated colors. Elderly individuals often prefer 
    warmer, more comforting colors. These preferences influence product design, marketing, 
    and environmental design for different age groups.
    """, body_style))
    
    # Color in Digital Design
    content.append(Paragraph("Color Psychology in Digital Design", heading_style))
    
    content.append(Paragraph("Web and App Design Considerations", subheading_style))
    content.append(Paragraph("""
    Digital design requires careful consideration of color psychology. Blue is commonly 
    used for trust and security in financial apps. Green is used for success messages 
    and environmental themes. Red is used for errors and urgent actions. Yellow is 
    used for warnings and attention-grabbing elements. Understanding these conventions 
    helps create intuitive user experiences.
    """, body_style))
    
    # Conclusion
    content.append(PageBreak())
    content.append(Paragraph("Conclusion", heading_style))
    content.append(Paragraph("""
    Color psychology and cultural meanings are complex, multifaceted subjects that influence 
    every aspect of human life. From marketing and branding to interior design and therapy, 
    understanding the psychological and cultural impact of colors is essential for creating 
    effective communication and meaningful experiences. As our world becomes more interconnected, 
    cultural sensitivity in color choices becomes increasingly important for global brands 
    and designers.
    
    The key to successful color application lies in understanding your audience, considering 
    cultural contexts, and applying psychological principles thoughtfully. Whether you're 
    designing a website, decorating a room, or creating a marketing campaign, the colors 
    you choose will significantly impact how your message is received and understood.
    """, body_style))
    
    # Build the PDF
    doc.build(content)
    print(f"✅ Created comprehensive Color Psychology PDF: {filename}")
    return filename

if __name__ == "__main__":
    create_color_psychology_pdf()

