#!/usr/bin/env python3
"""
Script to create a Titanic-themed PDF for testing the PDF chat application.
"""

try:
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
    from reportlab.lib.units import inch
    import os
    
    def create_titanic_pdf():
        """Create a Titanic-themed PDF document."""
        
        # Create the PDF file
        filename = "titanic_history.pdf"
        doc = SimpleDocTemplate(filename, pagesize=letter)
        styles = getSampleStyleSheet()
        
        # Content about the Titanic
        content = [
            Paragraph("The RMS Titanic: A Historical Overview", styles['Title']),
            Spacer(1, 12),
            
            Paragraph("Introduction", styles['Heading1']),
            Paragraph("""
            The RMS Titanic was a British passenger liner that sank in the North Atlantic Ocean 
            in the early morning hours of 15 April 1912, after striking an iceberg during her 
            maiden voyage from Southampton to New York City. Of the estimated 2,224 passengers 
            and crew aboard, more than 1,500 died, making it one of the deadliest commercial 
            peacetime maritime disasters in modern history.
            """, styles['Normal']),
            
            Spacer(1, 12),
            Paragraph("Construction and Design", styles['Heading1']),
            Paragraph("""
            The Titanic was built by the Harland and Wolff shipyard in Belfast, Ireland. 
            She was designed to be the largest and most luxurious passenger ship of her time. 
            The ship was 882 feet 9 inches long and 92 feet 6 inches wide, with a gross 
            tonnage of 46,328 tons. She had three propellers and could reach a top speed 
            of 23 knots.
            """, styles['Normal']),
            
            Spacer(1, 12),
            Paragraph("Passenger Classes", styles['Heading1']),
            Paragraph("""
            The Titanic had three passenger classes: First Class, Second Class, and Third Class. 
            First Class passengers enjoyed luxurious accommodations with private promenades, 
            a swimming pool, Turkish baths, and fine dining. Second Class passengers had 
            comfortable but more modest accommodations. Third Class passengers, mostly 
            immigrants, traveled in basic but clean conditions.
            """, styles['Normal']),
            
            Spacer(1, 12),
            Paragraph("The Maiden Voyage", styles['Heading1']),
            Paragraph("""
            The Titanic departed Southampton on April 10, 1912, with stops in Cherbourg, 
            France, and Queenstown (now Cobh), Ireland, before heading across the Atlantic 
            to New York. The ship carried some of the wealthiest people in the world, 
            as well as hundreds of emigrants seeking a new life in America.
            """, styles['Normal']),
            
            Spacer(1, 12),
            Paragraph("The Collision", styles['Heading1']),
            Paragraph("""
            On the night of April 14, 1912, at 11:40 PM ship's time, the Titanic struck 
            an iceberg. The collision caused the ship's hull plates to buckle inwards along 
            her starboard side and opened five of her sixteen watertight compartments to 
            the sea. The ship was designed to stay afloat with up to four compartments 
            flooded, but not five.
            """, styles['Normal']),
            
            Spacer(1, 12),
            Paragraph("The Sinking", styles['Heading1']),
            Paragraph("""
            As the ship began to sink, passengers and crew were evacuated in lifeboats. 
            However, there were only enough lifeboats for about half of the people on board. 
            The ship broke in two and sank at 2:20 AM on April 15, 1912. The Carpathia 
            arrived at the scene about an hour and a half later and rescued the survivors.
            """, styles['Normal']),
            
            Spacer(1, 12),
            Paragraph("Aftermath and Legacy", styles['Heading1']),
            Paragraph("""
            The sinking of the Titanic led to major changes in maritime safety regulations. 
            The International Convention for the Safety of Life at Sea (SOLAS) was established 
            in 1914, requiring ships to carry enough lifeboats for all passengers and crew. 
            The disaster also led to the establishment of the International Ice Patrol 
            to monitor icebergs in the North Atlantic.
            """, styles['Normal']),
            
            Spacer(1, 12),
            Paragraph("Discovery of the Wreck", styles['Heading1']),
            Paragraph("""
            The wreck of the Titanic was discovered in 1985 by a team led by Robert Ballard. 
            The ship lies in two main pieces about 370 miles southeast of Newfoundland, 
            at a depth of about 12,500 feet. The wreck has been extensively explored and 
            documented, though it is deteriorating due to deep-sea conditions.
            """, styles['Normal']),
            
            Spacer(1, 12),
            Paragraph("Cultural Impact", styles['Heading1']),
            Paragraph("""
            The Titanic disaster has had a lasting cultural impact, inspiring numerous books, 
            films, and documentaries. The most famous is James Cameron's 1997 film "Titanic," 
            which won 11 Academy Awards. The story continues to fascinate people around 
            the world as a symbol of human hubris and the power of nature.
            """, styles['Normal']),
        ]
        
        # Build the PDF
        doc.build(content)
        print(f"✅ Created Titanic PDF: {filename}")
        return filename
    
    if __name__ == "__main__":
        create_titanic_pdf()
        
except ImportError:
    print("❌ reportlab library not found. Installing...")
    import subprocess
    import sys
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "reportlab"])
        print("✅ reportlab installed successfully!")
        print("Please run this script again to create the Titanic PDF.")
    except subprocess.CalledProcessError:
        print("❌ Failed to install reportlab. Please install it manually:")
        print("pip install reportlab")
