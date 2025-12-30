from neo4j import GraphDatabase

uri = "neo4j+s://648d4dab.databases.neo4j.io"
user = "neo4j"
password = "WIwruIxla59y-fcWvI_b0Euzd8YkQ3PXbnj--0StwYE"

driver = GraphDatabase.driver(uri, auth=(user, password))