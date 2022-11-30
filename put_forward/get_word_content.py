from os import listdir
from os.path import isfile, join
import zipfile
import xml.etree.ElementTree as ET

import pandas as pd


class GetWordContent():

    def __init__(self):
        doc_1 = 'raw_data/CN_Awards_2022_carbon_reduction.docx'
        doc_2 = 'raw_data/zen_of_python.docx'
        doc_3 = 'raw_data/Example_doc2.docx'
        doc_4 = 'raw_data/DBDA_CW_Suite.docx' # this on reads ok
        doc_5 = 'raw_data/Client2_PQQ_180322.docx' # this on reads ok
        doc_6 = 'raw_data/Question 15 - Construction Quality Assurance v3_IW.docx'
        self.doc = doc_5


    def get_title_text_df(self, heading_type, doc):
        if doc != "": self.doc = doc
        if doc[-4:] == '.doc':
            print(".doc found! currently excluding these in > GetWordContent.get_title_text_df \n")
            return None
        # nice reference: https://towardsdatascience.com/how-to-extract-data-from-ms-word-documents-using-python-ed3fbb48c122

        # take out path from filename:
        self.short_doc_name = doc[9:]

        try:
            self.doc = zipfile.ZipFile(self.doc).read('word/document.xml')
            self.root = ET.fromstring(self.doc)

            # to see the formats extracted... pretty complex and unreadable:
            # print(ET.tostring(root))
            # print(doc)


            # Microsoft's XML makes heavy use of XML namespaces; thus, we'll need to reference that in our code
            self.ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
            self.body = self.root.find('w:body',self. ns)  # find the XML "body" tag
            self.p_sections = self.body.findall('w:p', self.ns)  # under the body tag, find all the paragraph sections



            section_labels = [self.get_section_text(s, self.ns)
                            if self.is_heading2_section(s, self.ns) else ''
                            for s in self.p_sections]
            # print(section_labels)

            section_text = [{'doc_title': f'{self.short_doc_name}',
                             'title': t, 'paragraph_text':
                            self.get_section_text(self.p_sections[i+1], self.ns)}
                            for i, t in enumerate(section_labels) if len(t) > 0]
            # print(section_text)

            df = pd.DataFrame(section_text)

        except BaseException as e:
            print("Error: " + str(e))
            return None
        # print(df)
        return df

    def is_heading2_section(self, p, ns):
        """Returns True if the given paragraph section has been styled as a Heading2"""
        return_val = False
        heading_style_elem = p.find(".//w:pStyle[@w:val='Heading2']", ns)
        if heading_style_elem is not None:
            return_val = True
        return return_val

    def get_section_text(self, p, ns):
        """Returns the joined text of the text elements under the given paragraph tag"""
        return_val = ''
        text_elems = p.findall('.//w:t', ns)
        if text_elems is not None:
            return_val = ''.join([t.text for t in text_elems])
        return return_val

    def get_list_files_n_paths(self, mypath):
        onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
        print(onlyfiles)
        return onlyfiles

if __name__ == "__main__":
    # docs = {
    #     1: 'raw_data/CN_Awards_2022_carbon_reduction.docx',
    #     2: 'raw_data/zen_of_python.docx',
    #     3: 'raw_data/Example_doc2.doc', # gives an error
    #     4: 'raw_data/DBDA_CW_Suite.docx',
    #     5: 'raw_data/Client2_PQQ_180322.docx',
    #     6: 'raw_data/Question 15 - Construction Quality Assurance v3_IW.docx',
    # }
    path_for_files = "raw_data/"

    c = GetWordContent()
    # get list of files to process:
    list_of_files = c.get_list_files_n_paths(path_for_files)


    docs_n_content = []
    overall_df = pd.DataFrame()
    df_temp = pd.DataFrame()
    for d in list_of_files:
        df = c.get_title_text_df("Heading2", "raw_data/"+d)
        print(d)
        # print(df)
        print(' ***************** **************** ')
        df_temp = pd.concat([df_temp, df], axis=0)
        # overall_df.append(df)
    print(df_temp)
    overall_df = df_temp
    overall_df.to_csv('output_split_docs.csv', index=False)

    # syed's categorisation:
    df=pd.read_csv('output_split_docs.csv')
    documenttags=[("") for i in range (len(df['title']))]
    keytopics= ['Business Continuity','Commissioning','Communication','Commercial','Design','Digital Construction','Enviromental','Framework Management', 'Health & Safety', 'Procurement', 'Planning', 'Project Management', 'Quality','Risk Management','Soft Landings', 'Staff', 'Stakeholder Management', 'Supply Chain', 'Sustainability']
    for i in range (len(keytopics)):
        for j in range (len(df['title'])):
            if keytopics[i] in df['title'][j]:
                documenttags[j] = keytopics[i]
    # print(documenttags)
    df['Tags'] = documenttags
    df.to_csv('categorised_testfile.csv', index=False)
