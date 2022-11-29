from neo4j import GraphDatabase, basic_auth

driver = GraphDatabase.driver(
  "bolt://44.192.127.122:7687",
  auth=basic_auth("neo4j", "sunday-cheeses-cells"))

cypher_query = '''
MATCH (n)'''
