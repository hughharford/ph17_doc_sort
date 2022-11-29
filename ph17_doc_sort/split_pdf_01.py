pdf_to_try = 'raw_data/AQ1_Project_Management_Response.pdf'
second_pdf_to_try = 'raw_data/The Orb __ Ticket_1.pdf'

# pip install pdfminer.six
from pdfminer.high_level import extract_text

# text = extract_text(pdf_to_try)
# print(text)


# pip install PyPDF2
# PyPDF2

doc_input = 'raw_data/CN_Awards_2022_carbon_reduction _championMarketing.docx'

# pip install docx2txt
# import docx2txt
# my_text = docx2txt.process(doc_input)
# print(my_text)


import textract

text = textract.process(doc_input)
text = text.decode("utf-8")
print(text)
