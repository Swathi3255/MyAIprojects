#!/usr/bin/env python3
"""
Convert Color Psychology text content to PDF
"""

from fpdf import FPDF
import os

def convert_text_to_pdf():
    """Convert the text file to PDF"""
    
    # Read the text file
    with open('color_psychology_cultural_meanings.txt', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Create PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Split content into lines and add to PDF
    lines = content.split('\n')
    
    for line in lines:
        if line.strip() == '':
            pdf.ln(5)  # Add space for empty lines
        elif line.isupper() and len(line) > 10:  # Headers
            pdf.set_font("Arial", style="B", size=14)
            pdf.cell(0, 10, line, ln=True)
            pdf.set_font("Arial", size=12)
        elif line.startswith('    ') or line.startswith('\t'):  # Indented content
            pdf.set_font("Arial", style="I", size=11)
            pdf.cell(0, 8, line.strip(), ln=True)
            pdf.set_font("Arial", size=12)
        else:
            # Regular content
            if len(line) > 80:
                # Split long lines
                words = line.split()
                current_line = ""
                for word in words:
                    if len(current_line + word) > 80:
                        pdf.cell(0, 8, current_line.strip(), ln=True)
                        current_line = word + " "
                    else:
                        current_line += word + " "
                if current_line.strip():
                    pdf.cell(0, 8, current_line.strip(), ln=True)
            else:
                pdf.cell(0, 8, line, ln=True)
    
    # Save PDF
    pdf_filename = "color_psychology_cultural_meanings.pdf"
    pdf.output(pdf_filename)
    
    print(f"✅ Created PDF: {pdf_filename}")
    return pdf_filename

if __name__ == "__main__":
    convert_text_to_pdf()

