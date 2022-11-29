from neo4j import GraphDatabase
from neeo4j_sandbox import Neo4jConnection

class PopulateGraph:
    def __init__(self):
        sandbox = Neo4jConnection()
        self.driver = sandbox.get_conn()

def create_person(tx, name):
    tx.run("CREATE (a:Person {name: $name})", name=name)

def create_friend_of(tx, name, friend):
    tx.run("MATCH (a:Person) WHERE a.name = $name "
           "CREATE (a)-[:KNOWS]->(:Person {name: $friend})",
           name=name, friend=friend)

with self.driver.session() as session:
    session.execute_write(create_person, "Alice")
    session.execute_write(create_friend_of, "Alice", "Bob")
    session.execute_write(create_friend_of, "Alice", "Carl")

driver.close()
