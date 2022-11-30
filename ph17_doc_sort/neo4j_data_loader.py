from neo4j import GraphDatabase
from neo4j_sandbox import Neo4jConnection
import time
import pandas as pd


class PopulateGraph:
    def __init__(self):
        conn = Neo4jConnection(uri="bolt://44.192.127.122:7687",
                    user="neo4j",
                    pwd="sunday-cheeses-cells")
        self.conn = conn.get_conn()

        self.concept_list = [
            "Business_Continuity",
            "Commissioning",
            "Communication",
            "Commercial",
            "Design",
            "Digital Construction",
            "Environmental",
            "Framework Management",
            "Health & Safety",
            "Procurement",
            "Planning",
            "Project Management",
            "Quality",
            "Risk Management",
            "Soft Landings",
            "Staff",
            "Stakeholder Management",
            "Supply Chain",
            "Sustainability"
        ]

        self.df_concepts = pd.DataFrame(self.concept_list, columns=["concepts"])
        # print(self.df_concepts)


    def setup_concepts(self):
        # print(self.df_concepts)

        # drop first, to ensure we are recreating every time:
        self.conn.query("DROP CONSTRAINT ON (c:concept) ASSERT c.concept IS UNIQUE", db="neo4j")
        # then create node type - concept
        self.conn.query("CREATE CONSTRAINT ON (c:concept) ASSERT c.concept IS UNIQUE", db="neo4j")

        # delete existing concepts listed:
        # delete_concept_query =  '''
        #                         MATCH (c:concept)
        #                         DELETE c
        #                         '''
        # and add the concepts as nodes:
        self.add_concepts(self.df_concepts)


    def setup_doc_subtitle(self):
        # drop first
        self.conn.query("DROP (d:doc_subtitle)", db="neo4j")
        # then create node type - doc_subtitle
        self.conn.query("CREATE (d:doc_subtitle)", db="neo4j")
        # took out: CONSTRAINT ON ... ASSERT d:doc_subtitle IS UNIQUE


    def add_concepts(self, rows, batch_size=10000):
        # Adds concept nodes to the Neo4j graph.
        query = '''
                UNWIND $rows AS row
                MERGE (c:concept {concept: row.concepts})
                RETURN count(*) as total
                '''
                # SET c.PropertyName = row.paragraphtext
        return self.insert_data(query, rows, batch_size)

    # TO CLEAR THE DB FOR HARD RESET:


    # DELETE ALL:
    # MATCH (n) DETACH DELETE n;

    def add_doc_subtitle_with_relationships(self, rows, batch_size=5000):
        # Adds doc_subtitle nodes and (:concept)--(:doc_subtitle) and
        # (:Paper)--(:Category) relationships to the Neo4j graph as a
        # batch job.

        query = '''
                UNWIND $rows as row
                MERGE (d:doc_subtitle {doc_subtitle:row.doc_subtitle})
                SET d.paragraph_text = row.paragraph_text
                SET d.doc_title = row.doc_title

                // connect concepts to doc_subtitle
                WITH row, d
                MATCH (c:concept WHERE c.concept = row.Tags)
                MATCH (d:doc_subtitle WHERE d.doc_subtitle = row.doc_subtitle)
                CREATE (d)-[r:TITLE_ABOUT]->(c)
                RETURN count(*) as total
                '''

        return self.insert_data(query, rows, batch_size)

    def insert_data(self, query, rows, batch_size = 10000):
        # Function to handle the updating the Neo4j database in batch mode.

        total = 0
        batch = 0
        start = time.time()
        result = None

        while batch * batch_size < len(rows):

            res = self.conn.query(query,
                            parameters = {'rows': rows[batch*batch_size:(batch+1)*batch_size].to_dict('records')})
            total += res[0]['total']
            batch += 1
            result = {"total":total,
                    "batches":batch,
                    "time":time.time()-start}
            print(result)

        return result

    def filter_df(self, df):
        filtered_df = pd.DataFrame()
        return filtered_df

if __name__ == "__main__":
    df = pd.read_csv("categorised_testfile.csv")
    print(df)
    print(df.columns)
    df.rename(columns = {'title':'doc_subtitle'}, inplace = True)

    # filter df
    p = PopulateGraph()
    new_df = p.filter_df(df)
    p.setup_concepts()
    print()
    print()
    print(df.columns)

    p.add_doc_subtitle_with_relationships(df)
