from get_word_content import GetWordContent


concept_list = [
    "Risk",
    "Environment",
    "Sustainability",
    "Procurement",
    "Experience"
]

class LinkToTitles:

    def __init__(self):
        self.c = GetWordContent()
        # c.get_title_text_df("Heading2", docs[6])

    def get_titles_and_paras(self):
        docs = {
            1: 'raw_data/CN_Awards_2022_carbon_reduction.docx',
            2: 'raw_data/zen_of_python.docx',
            3: 'raw_data/Example_doc2.doc', # gives an error
            4: 'raw_data/DBDA_CW_Suite.docx',
            5: 'raw_data/Client2_PQQ_180322.docx',
            6: 'raw_data/Question 15 - Construction Quality Assurance v3_IW.docx',
        }

        docs_n_content = []
        for d in docs:
            print(docs[d])
            df = self.c.get_title_text_df("Heading2", docs[d])
            # print(df)
            # print(' ***************** **************** ')
            docs_n_content.append(df)

        for d in docs_n_content:
            if d is not None:
                print("got content, gonna do something")
            # print(d)



if __name__ == "__main__":
    ltt = LinkToTitles()
    ltt.get_titles_and_paras()
