#!/usr/bin/env python3
"""
Color Psychology and Cultural Meanings PDF Generator
Creates a comprehensive PDF for testing the specialized RAG application
"""

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import inch
import os

def create_color_psychology_pdf():
    """Create a comprehensive PDF about color psychology and cultural meanings"""
    
    filename = "color_psychology_cultural_meanings.pdf"
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4
    
    # Title
    c.setFont("Helvetica-Bold", 24)
    c.drawCentredText(width/2, height - 2*inch, "The Complete Guide to Color Psychology and Cultural Meanings")
    
    # Introduction
    c.setFont("Helvetica-Bold", 16)
    c.drawString(1*inch, height - 3*inch, "Introduction")
    
    c.setFont("Helvetica", 12)
    intro_text = """
Color is one of the most powerful tools in human communication, influencing our emotions, 
decisions, and cultural understanding. This comprehensive guide explores the psychological 
effects of colors and their diverse cultural meanings across different societies. Understanding 
these concepts is crucial for designers, marketers, psychologists, and anyone interested in 
the profound impact of color on human behavior and culture.
    """
    
    y_position = height - 3.5*inch
    for line in intro_text.strip().split('\n'):
        c.drawString(1*inch, y_position, line.strip())
        y_position -= 0.25*inch
    
    # Primary Colors Psychology
    c.setFont("Helvetica-Bold", 16)
    c.drawString(1*inch, y_position - 0.5*inch, "Primary Colors and Their Psychological Effects")
    
    # Red
    c.setFont("Helvetica-Bold", 14)
    c.drawString(1*inch, y_position - 1*inch, "Red: The Color of Passion and Energy")
    
    c.setFont("Helvetica", 12)
    red_text = """
Red is the most emotionally intense color in the spectrum. Psychologically, red increases 
heart rate, blood pressure, and respiration. It's associated with passion, love, anger, and 
danger. In marketing, red creates urgency and is often used for clearance sales. Studies show 
that red can enhance physical performance and increase appetite, which is why many restaurants 
use red in their branding.
    """
    
    y_position -= 1.5*inch
    for line in red_text.strip().split('\n'):
        c.drawString(1*inch, y_position, line.strip())
        y_position -= 0.25*inch
    
    # Blue
    c.setFont("Helvetica-Bold", 14)
    c.drawString(1*inch, y_position - 0.5*inch, "Blue: The Color of Trust and Stability")
    
    c.setFont("Helvetica", 12)
    blue_text = """
Blue is universally associated with trust, reliability, and calmness. It has a calming effect 
on the mind and body, reducing blood pressure and heart rate. Blue is often used in corporate 
branding to convey professionalism and dependability. However, blue can also be associated 
with sadness and depression in certain contexts. It's the most popular color globally, 
representing sky and water in nature.
    """
    
    y_position -= 1.5*inch
    for line in blue_text.strip().split('\n'):
        c.drawString(1*inch, y_position, line.strip())
        y_position -= 0.25*inch
    
    # Yellow
    c.setFont("Helvetica-Bold", 14)
    c.drawString(1*inch, y_position - 0.5*inch, "Yellow: The Color of Optimism and Creativity")
    
    c.setFont("Helvetica", 12)
    yellow_text = """
Yellow is the most visible color and stimulates mental activity. It's associated with happiness, 
optimism, and creativity. Yellow can increase energy levels and stimulate the nervous system. 
However, too much yellow can cause anxiety and agitation. In design, yellow is often used 
to grab attention and convey warmth and friendliness.
    """
    
    y_position -= 1.5*inch
    for line in yellow_text.strip().split('\n'):
        c.drawString(1*inch, y_position, line.strip())
        y_position -= 0.25*inch
    
    # New page for cultural meanings
    c.showPage()
    
    # Cultural Meanings
    c.setFont("Helvetica-Bold", 16)
    c.drawString(1*inch, height - 2*inch, "Cultural Meanings of Colors Across Different Societies")
    
    # Red in different cultures
    c.setFont("Helvetica-Bold", 14)
    c.drawString(1*inch, height - 2.5*inch, "Red in Different Cultures")
    
    c.setFont("Helvetica", 12)
    red_cultural_text = """
Western Cultures: Red represents love, passion, danger, and stop signals. It's associated 
with Valentine's Day and Christmas.

Eastern Cultures: In China, red symbolizes good luck, prosperity, and celebration. It's 
the traditional color for weddings and New Year celebrations. In India, red represents purity 
and is worn by brides.

African Cultures: Red often represents blood, life force, and spiritual power. It's 
used in many traditional ceremonies and rituals.
    """
    
    y_position = height - 3*inch
    for line in red_cultural_text.strip().split('\n'):
        c.drawString(1*inch, y_position, line.strip())
        y_position -= 0.25*inch
    
    # White in different cultures
    c.setFont("Helvetica-Bold", 14)
    c.drawString(1*inch, y_position - 0.5*inch, "White in Different Cultures")
    
    c.setFont("Helvetica", 12)
    white_cultural_text = """
Western Cultures: White symbolizes purity, innocence, and peace. It's the traditional 
color for weddings and represents cleanliness.

Eastern Cultures: In many Asian cultures, white is associated with death, mourning, 
and funerals. It represents the end of life and spiritual transition.

Middle Eastern Cultures: White represents peace, purity, and divine light. It's 
often worn during religious ceremonies and represents spiritual cleanliness.
    """
    
    y_position -= 1*inch
    for line in white_cultural_text.strip().split('\n'):
        c.drawString(1*inch, y_position, line.strip())
        y_position -= 0.25*inch
    
    # Black in different cultures
    c.setFont("Helvetica-Bold", 14)
    c.drawString(1*inch, y_position - 0.5*inch, "Black in Different Cultures")
    
    c.setFont("Helvetica", 12)
    black_cultural_text = """
Western Cultures: Black represents elegance, sophistication, and formality. It's also 
associated with mourning, death, and evil.

Eastern Cultures: In China, black represents water, winter, and the unknown. It's 
associated with mystery and the supernatural.

African Cultures: Black often represents the earth, fertility, and spiritual power. 
It's considered a powerful and protective color.
    """
    
    y_position -= 1*inch
    for line in black_cultural_text.strip().split('\n'):
        c.drawString(1*inch, y_position, line.strip())
        y_position -= 0.25*inch
    
    # New page for marketing and branding
    c.showPage()
    
    # Color in Marketing and Branding
    c.setFont("Helvetica-Bold", 16)
    c.drawString(1*inch, height - 2*inch, "Color Psychology in Marketing and Branding")
    
    c.setFont("Helvetica-Bold", 14)
    c.drawString(1*inch, height - 2.5*inch, "Brand Color Strategies")
    
    c.setFont("Helvetica", 12)
    branding_text = """
Successful brands carefully choose their colors based on psychological principles and 
cultural considerations. McDonald's uses red and yellow to stimulate appetite and create 
urgency. Facebook uses blue to convey trust and reliability. Starbucks uses green to 
represent growth, nature, and relaxation. Understanding these principles helps businesses 
create more effective marketing campaigns and brand identities.
    """
    
    y_position = height - 3*inch
    for line in branding_text.strip().split('\n'):
        c.drawString(1*inch, y_position, line.strip())
        y_position -= 0.25*inch
    
    c.setFont("Helvetica-Bold", 14)
    c.drawString(1*inch, y_position - 0.5*inch, "Color and Consumer Behavior")
    
    c.setFont("Helvetica", 12)
    consumer_text = """
Research shows that color can influence purchasing decisions by up to 85%. Warm colors 
(red, orange, yellow) create urgency and impulse buying, while cool colors (blue, green, 
purple) encourage careful consideration. The right color choice can increase brand recognition 
by 80% and improve readability by 40%.
    """
    
    y_position -= 1*inch
    for line in consumer_text.strip().split('\n'):
        c.drawString(1*inch, y_position, line.strip())
        y_position -= 0.25*inch
    
    # Color Therapy
    c.setFont("Helvetica-Bold", 16)
    c.drawString(1*inch, y_position - 0.5*inch, "Color Therapy and Healing Applications")
    
    c.setFont("Helvetica-Bold", 14)
    c.drawString(1*inch, y_position - 1*inch, "Chromotherapy Principles")
    
    c.setFont("Helvetica", 12)
    therapy_text = """
Color therapy, or chromotherapy, uses specific colors to promote healing and well-being. 
Red light therapy is used to increase circulation and energy. Blue light therapy helps 
with sleep disorders and relaxation. Green is used for balance and harmony. Yellow 
stimulates the nervous system and improves mood. Understanding these therapeutic 
applications can help in designing healing environments and wellness programs.
    """
    
    y_position -= 1.5*inch
    for line in therapy_text.strip().split('\n'):
        c.drawString(1*inch, y_position, line.strip())
        y_position -= 0.25*inch
    
    # Interior Design
    c.setFont("Helvetica-Bold", 16)
    c.drawString(1*inch, y_position - 0.5*inch, "Color Psychology in Interior Design")
    
    c.setFont("Helvetica-Bold", 14)
    c.drawString(1*inch, y_position - 1*inch, "Room-Specific Color Guidelines")
    
    c.setFont("Helvetica", 12)
    interior_text = """
Bedrooms: Cool colors like blue and green promote relaxation and better sleep. 
Avoid bright reds and oranges which can be stimulating.

Kitchens: Warm colors like yellow and orange stimulate appetite and create 
a welcoming atmosphere.

Living Rooms: Neutral colors with warm accents create comfort and social 
interaction.

Bathrooms: Light blues and greens create a spa-like, calming environment.
    """
    
    y_position -= 2*inch
    for line in interior_text.strip().split('\n'):
        c.drawString(1*inch, y_position, line.strip())
        y_position -= 0.25*inch
    
    # Color Combinations
    c.setFont("Helvetica-Bold", 16)
    c.drawString(1*inch, y_position - 0.5*inch, "Color Combinations and Psychological Effects")
    
    c.setFont("Helvetica-Bold", 14)
    c.drawString(1*inch, y_position - 1*inch, "Complementary Colors")
    
    c.setFont("Helvetica", 12)
    complementary_text = """
Complementary colors (opposite on the color wheel) create high contrast and visual 
excitement. Red and green combinations create energy and tension. Blue and orange 
combinations are calming yet vibrant. These combinations are effective for creating 
focal points and drawing attention.
    """
    
    y_position -= 1.5*inch
    for line in complementary_text.strip().split('\n'):
        c.drawString(1*inch, y_position, line.strip())
        y_position -= 0.25*inch
    
    c.setFont("Helvetica-Bold", 14)
    c.drawString(1*inch, y_position - 0.5*inch, "Analogous Colors")
    
    c.setFont("Helvetica", 12)
    analogous_text = """
Analogous colors (next to each other on the color wheel) create harmony and unity. 
Blue, blue-green, and green combinations are calming and natural. Red, red-orange, 
and orange combinations are warm and energetic. These combinations work well for 
creating cohesive, peaceful environments.
    """
    
    y_position -= 1.5*inch
    for line in analogous_text.strip().split('\n'):
        c.drawString(1*inch, y_position, line.strip())
        y_position -= 0.25*inch
    
    # New page for gender and age differences
    c.showPage()
    
    # Gender Differences
    c.setFont("Helvetica-Bold", 16)
    c.drawString(1*inch, height - 2*inch, "Gender Differences in Color Preferences")
    
    c.setFont("Helvetica-Bold", 14)
    c.drawString(1*inch, height - 2.5*inch, "Research Findings")
    
    c.setFont("Helvetica", 12)
    gender_text = """
Studies show that men and women have different color preferences. Men tend to prefer 
blue, green, and black, while women often prefer purple, pink, and lighter colors. 
These preferences may be influenced by cultural conditioning, biological factors, 
and personal experiences. Understanding these differences is important for 
gender-targeted marketing and design.
    """
    
    y_position = height - 3*inch
    for line in gender_text.strip().split('\n'):
        c.drawString(1*inch, y_position, line.strip())
        y_position -= 0.25*inch
    
    # Age Differences
    c.setFont("Helvetica-Bold", 16)
    c.drawString(1*inch, y_position - 0.5*inch, "Age-Related Color Preferences")
    
    c.setFont("Helvetica-Bold", 14)
    c.drawString(1*inch, y_position - 1*inch, "Developmental Color Psychology")
    
    c.setFont("Helvetica", 12)
    age_text = """
Color preferences change throughout life. Children are drawn to bright, saturated colors 
like red, yellow, and blue. Teenagers often prefer bold, contrasting colors. Adults 
tend to prefer more muted, sophisticated colors. Elderly individuals often prefer 
warmer, more comforting colors. These preferences influence product design, marketing, 
and environmental design for different age groups.
    """
    
    y_position -= 1.5*inch
    for line in age_text.strip().split('\n'):
        c.drawString(1*inch, y_position, line.strip())
        y_position -= 0.25*inch
    
    # Digital Design
    c.setFont("Helvetica-Bold", 16)
    c.drawString(1*inch, y_position - 0.5*inch, "Color Psychology in Digital Design")
    
    c.setFont("Helvetica-Bold", 14)
    c.drawString(1*inch, y_position - 1*inch, "Web and App Design Considerations")
    
    c.setFont("Helvetica", 12)
    digital_text = """
Digital design requires careful consideration of color psychology. Blue is commonly 
used for trust and security in financial apps. Green is used for success messages 
and environmental themes. Red is used for errors and urgent actions. Yellow is 
used for warnings and attention-grabbing elements. Understanding these conventions 
helps create intuitive user experiences.
    """
    
    y_position -= 1.5*inch
    for line in digital_text.strip().split('\n'):
        c.drawString(1*inch, y_position, line.strip())
        y_position -= 0.25*inch
    
    # Conclusion
    c.setFont("Helvetica-Bold", 16)
    c.drawString(1*inch, y_position - 0.5*inch, "Conclusion")
    
    c.setFont("Helvetica", 12)
    conclusion_text = """
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
    """
    
    y_position -= 1*inch
    for line in conclusion_text.strip().split('\n'):
        c.drawString(1*inch, y_position, line.strip())
        y_position -= 0.25*inch
    
    # Save the PDF
    c.save()
    print(f"✅ Created comprehensive Color Psychology PDF: {filename}")
    return filename

if __name__ == "__main__":
    create_color_psychology_pdf()
