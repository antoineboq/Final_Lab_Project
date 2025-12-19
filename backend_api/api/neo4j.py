from fastapi import FastAPI, HTTPException
from neo4j import GraphDatabase
from contextlib import asynccontextmanager
# Import des infos de la BDD
from backend_api.databases.neo4j import NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD

class Neo4jService:
    def __init__(self):
        self.driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))

    def close(self):
        self.driver.close()

    def get_nodes(self, label: str):
        with self.driver.session() as session:
            query = f"MATCH (n:{label}) RETURN n LIMIT 25"
            result = session.run(query)
            return [record["n"] for record in result]

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.neo4j_db = Neo4jService()
    print("🚀 Connexion Neo4j établie")
    yield
    app.state.neo4j_db.close()
    print("Connexion Neo4j fermée")

app = FastAPI(title="Neo4j View API", lifespan=lifespan)

@app.get("/")
async def root():
    return {"message": "API connectée à Neo4j", "statut": "OK"}

@app.get("/view/nodes/{label}")
async def get_view_nodes(label: str):
    try:
        nodes = app.state.neo4j_db.get_nodes(label)
        return [{"id": n.element_id, "properties": dict(n._properties)} for n in nodes]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))