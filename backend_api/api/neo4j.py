from fastapi import APIRouter, HTTPException, Query
from backend_api.databases.neo4j import driver
from backend_api.databases.mongodb import films

router = APIRouter(prefix="/neo4j", tags=["Neo4j Operations"])


def execute_read_query(query, parameters=None):
    with driver.session() as session:
        result = session.run(query, parameters)
        return [record.data() for record in result]


@router.get("/movie/reviewers")
def liste_utilisateurs_ayant_note_film(titre: str = Query(..., description="Nom du film")):
    query = """
    MATCH (p:Person)-[:REVIEWED]->(m:Movie)
    WHERE m.title =~ ('(?i)' + $title)
    RETURN p.name AS name
    """
    results = execute_read_query(query, {"title": titre})
    if not results:
        raise HTTPException(status_code=404, detail="Aucun utilisateur ou film trouvé")
    return results


@router.get("/user/{user_name}")
def infos_utilisateur_et_notes(user_name: str):
    query = """
    MATCH (p:Person)
    WHERE p.name =~ ('(?i)' + $name)
    OPTIONAL MATCH (p)-[:REVIEWED]->(m:Movie)
    RETURN p.name AS name, 
           count(m) AS nombre_de_films_notes, 
           collect(m.title) AS liste_films_notes
    """
    results = execute_read_query(query, {"name": user_name})
    if not results or results[0]['name'] is None:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return results[0]


@router.get("/common-movies-count")
def films_communs_mongo_neo4j():
    query_neo = "MATCH (m:Movie) RETURN m.title AS title"
    neo_titles = {record.get("title") for record in execute_read_query(query_neo) if record.get("title")}

    mongo_titles = {f["title"] for f in films.find({}, {"title": 1, "_id": 0}) if "title" in f}

    common = neo_titles.intersection(mongo_titles)
    return {
        "nb_films_communs": len(common),
        "liste_films_communs": list(common)
    }