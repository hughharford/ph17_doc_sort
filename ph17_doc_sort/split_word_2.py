import zipfile
import xml.etree.ElementTree as ET

import pandas as pd

doc_1 = 'raw_data/CN_Awards_2022_carbon_reduction.docx'
doc_2 = 'raw_data/zen_of_python.docx'
doc_3 = 'raw_data/Example_doc2.doc'
doc_4 = 'raw_data/DBDA_CW_Suite.docx' # this on reads ok
doc_5 = 'raw_data/Client2_PQQ_180322.docx' # this on reads ok
doc_6 = 'raw_data/Question 15 - Construction Quality Assurance v3_IW.docx'


# nice reference: https://towardsdatascience.com/how-to-extract-data-from-ms-word-documents-using-python-ed3fbb48c122

doc = zipfile.ZipFile(doc_5).read('word/document.xml')
root = ET.fromstring(doc)

# to see the formats extracted... pretty complex and unreadable:
# print(ET.tostring(root))
# print(doc)


# Microsoft's XML makes heavy use of XML namespaces; thus, we'll need to reference that in our code
ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
body = root.find('w:body', ns)  # find the XML "body" tag
p_sections = body.findall('w:p', ns)  # under the body tag, find all the paragraph sections

def is_heading2_section(p):
    """Returns True if the given paragraph section has been styled as a Heading2"""
    return_val = False
    heading_style_elem = p.find(".//w:pStyle[@w:val='Heading2']", ns)
    if heading_style_elem is not None:
        return_val = True
    return return_val

def get_section_text(p):
    """Returns the joined text of the text elements under the given paragraph tag"""
    return_val = ''
    text_elems = p.findall('.//w:t', ns)
    if text_elems is not None:
        return_val = ''.join([t.text for t in text_elems])
    return return_val


section_labels = [get_section_text(s) if is_heading2_section(s) else '' for s in p_sections]
# print(section_labels)

section_text = [{'title': t, 'text': get_section_text(p_sections[i+1])} for i, t in enumerate(section_labels) if len(t) > 0]
# print(section_text)

df = pd.DataFrame(section_text)
print(df)
