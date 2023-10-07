from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
import re

def text_to_pdf(text, pdf_filename="questions.pdf"):
    # Split the text into individual questions
    questions = re.split(r'\d+\.', text)[1:]  # Split by numbers followed by a dot
    
    # Create a new PDF document
    doc = SimpleDocTemplate(pdf_filename, pagesize=letter)
    
    # Define styles for the PDF
    styles = getSampleStyleSheet()
    
    # Create an empty list to hold the PDF content
    content = []
    
    for question in questions:
        lines = question.strip().split('\n')
        for line in lines:
            content.append(Paragraph(line.strip(), styles['Normal']))
            content.append(Spacer(1, 12))  # Add a space after each line for clarity
        content.append(PageBreak())
    
    # Build the PDF document with the content
    doc.build(content)

# Provided text
text = """
... [your provided text here] ...
"""

# Convert the text to a PDF
text_to_pdf(text)

# Read in text from "output/questions.txt"
with open("output/questions.txt", "r", encoding="utf-8") as f:
    text = f.read()

# Convert the text to a PDF
text_to_pdf(text)
