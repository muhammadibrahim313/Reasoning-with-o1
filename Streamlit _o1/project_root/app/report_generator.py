import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def generate_report(filename, summary, analysis):
    report = f"""
# Liability Analysis Report

## File: {filename}

### Summary
{summary}

### Analysis
{analysis}
    """
    return report

def save_report_as_pdf(report):
    pdf_file = "liability_analysis_report.pdf"
    
    doc = SimpleDocTemplate(pdf_file, pagesize=letter)
    styles = getSampleStyleSheet()
    
    # Split the report into lines
    lines = report.split('\n')
    
    # Create a list of flowables (paragraphs and spacers)
    flowables = []
    for line in lines:
        if line.startswith('# '):
            flowables.append(Paragraph(line[2:], styles['Title']))
        elif line.startswith('## '):
            flowables.append(Paragraph(line[3:], styles['Heading1']))
        elif line.startswith('### '):
            flowables.append(Paragraph(line[4:], styles['Heading2']))
        elif line.strip():
            flowables.append(Paragraph(line, styles['BodyText']))
        else:
            flowables.append(Spacer(1, 12))
    
    # Build the PDF
    doc.build(flowables)
    
    return pdf_file