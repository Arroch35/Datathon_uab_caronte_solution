import pdfplumber
import os

# here likely that we use a OOP class to manage the student's data
def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text


def extract_text_from_multiple_pdfs(pdf_paths):
    all_text = ""
    for pdf_path in pdf_paths:
        all_text += extract_text_from_pdf(pdf_path) 
    return all_text
    

#pdf_paths = ["../data/L10-numpy.pdf", "../data/L12a-Recursion.pdf"]
#extracted_text = extract_text_from_multiple_pdfs(pdf_paths)
#print(extracted_text)