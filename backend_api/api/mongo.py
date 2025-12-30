from fastapi import APIRouter, Query , HTTPException
from backend_api.databases.mongodb import films
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/films", tags= ["Les API FastAPI avec MongoDB"])

@router.get("/")
def liste_de_tous_les_films(
    pageInitial: int = Query(0),
    pageLimite: int = Query(10)
):
    listFilms = list(films.find({}, {"_id":0}).skip(pageInitial).limit(pageLimite))
    return listFilms


@router.get("/recherche")
def rechercher_un_film(
        acteur: str | None =Query(default=None, description="Nom de l'acteur"),
        film: str | None = Query(default=None, description="Nom du film"),
):
        requete = {}

        if film:
            requete["title"] = film
        elif acteur:
            requete["cast"] = acteur

        return list(films.find(requete, {"_id": 0}))



class UpdateMovie(BaseModel):
    cast: Optional[list[str]] = None
    year: Optional[int] = None
    plot: Optional[str] = None
    fullplot: Optional[str] = None
    directors: Optional[list[str]] = None
    genres: Optional[list[str]] = None
    poster: Optional[str] = None


@router.put("/{titre}")
def mettre_a_jour_film(titre: str, update: UpdateMovie):
    champs_collection_movie = {i:v for i, v in update.dict(exclude_unset=True).items()}

    if not champs_collection_movie:
        raise HTTPException(400, "Aucun champ complété")

    film = films.update_one({"title" : titre}, {"$set": champs_collection_movie})

    if film.matched_count == 0:
        raise HTTPException(404, "Aucun film trouvé avec ce titre")


    return {"message": "film mise à jour avec succès"}
