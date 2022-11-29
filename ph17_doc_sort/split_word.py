import docx2txt
doc_1 = 'raw_data/CN_Awards_2022_carbon_reduction.docx'
doc_2 = 'raw_data/zen_of_python.docx'
doc_3 = 'raw_data/Example_doc2.docx'
doc_4 = 'raw_data/DBDA_CW_Suite.docx' # this on reads ok
doc_5 = 'raw_data/Client2_PQQ_180322.docx' # this on reads ok

# read in word file
# docx2txt_result = docx2txt.process(doc_5)
# print(type(docx2txt_result))
# # print(result)


from docx2python import docx2python

# extract docx content
docx2python_result = docx2python(doc_5)
# print(docx2python_result)
# print()
print('docx2python_result.body[0][0][0][0] to drill down to a specific line')
print(docx2python_result.body[0][0][0][0])
print()
# print(docx2python_result.__dict__)
# print()
# print("docx2python_result.document:")
# print(docx2python_result.document)
