import pandas as pd
df=pd.read_csv('output_split_docs.csv')
print(df.head())
documenttags=[("") for i in range (len(df['title']))]
keytopics= ['Business Continuity','Commissioning','Communication','Commercial','Design','Digital Construction','Enviromental','Framework Management', 'Health & Safety', 'Procurement', 'Planning', 'Project Management', 'Quality','Risk Management','Soft Landings', 'Staff', 'Stakeholder Management', 'Supply Chain', 'Sustainability']
for i in range (len(keytopics)):
    for j in range (len(df['title'])):
        if keytopics[i] in df['title'][j]:
            documenttags[j] = keytopics[i]
print(documenttags)
df['Tags'] = documenttags
df.to_csv('testfile.csv', index=False)
print(df)
