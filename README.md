# FINAL LAB – Implement with Python

Application Python de gestion de films utilisant **FastAPI**, **MongoDB** et **Neo4j**.

---

## 📋 Table des Matières

- [Technologies Clés](#-technologies-clés)
- [Architecture du Projet](#-architecture-du-projet)
- [Fonctionnalités de l'API](#-fonctionnalités-de-lapi)
- [Installation et Configuration](#-installation-et-configuration)
- [Exécution de l'Application](#-exécution-de-lapplication)
- [Documentation API (Swagger)](#-documentation-api-swagger)
- [Tests](#-tests)

---

## 🛠 Technologies Clés

| Technologie | Version | Description |
|-------------|---------|-------------|
| **Python** | 3.10+ | Langage de programmation |
| **FastAPI** | Latest | Framework web moderne et performant |
| **MongoDB** | Atlas | Base de données NoSQL orientée documents |
| **Neo4j** | Sandbox/Aura | Base de données orientée graphes |
| **Uvicorn** | Latest | Serveur ASGI pour FastAPI |
| **Pydantic** | Latest | Validation des données |

---

## 📁 Architecture du Projet

```
Final_Lab_Project/
├── backend_api/
│   ├── __init__.py
│   ├── main.py                 # Point d'entrée de l'application FastAPI
│   ├── api/
│   │   ├── __init__.py
│   │   ├── mongo.py            # Endpoints MongoDB (films)
│   │   └── neo4j.py            # Endpoints Neo4j (utilisateurs, notes)
│   └── databases/
│       ├── __init__.py
│       ├── mongodb.py          # Configuration connexion MongoDB
│       └── neo4j.py            # Configuration connexion Neo4j
├── README.md
└── requirements.txt            # Dépendances Python
```

---

## 🎬 Fonctionnalités de l'API

### Endpoints MongoDB (Films)

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| `GET` | `/films/` | Lister tous les films avec pagination |
| `GET` | `/films/recherche` | Rechercher un film par titre ou acteur |
| `PUT` | `/films/{titre}` | Mettre à jour les informations d'un film |

### Endpoints Neo4j (Utilisateurs & Notes)

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| `GET` | `/neo4j/movie/reviewers` | Lister les utilisateurs ayant noté un film |
| `GET` | `/neo4j/user/{user_name}` | Infos utilisateur avec ses films notés |
| `GET` | `/neo4j/common-movies-count` | Nombre de films communs MongoDB/Neo4j |

---

### Détail des Endpoints

#### 1. Lister tous les films (MongoDB)
```http
GET /films/?pageInitial=0&pageLimite=10
```
**Paramètres Query :**
- `pageInitial` (int) : Index de départ (défaut: 0)
- `pageLimite` (int) : Nombre de résultats (défaut: 10)

---

#### 2. Rechercher un film (MongoDB)
```http
GET /films/recherche?film=Titanic
GET /films/recherche?acteur=DiCaprio
```
**Paramètres Query :**
- `film` (string, optionnel) : Nom du film à rechercher
- `acteur` (string, optionnel) : Nom de l'acteur à rechercher

---

#### 3. Mettre à jour un film (MongoDB)
```http
PUT /films/{titre}
```
**Corps de la requête (JSON) :**
```json
{
  "cast": ["Acteur 1", "Acteur 2"],
  "year": 2024,
  "plot": "Description courte",
  "fullplot": "Description complète",
  "directors": ["Réalisateur 1"],
  "genres": ["Action", "Drama"],
  "poster": "URL de l'affiche"
}
```
> Tous les champs sont optionnels.

---

#### 4. Utilisateurs ayant noté un film (Neo4j)
```http
GET /neo4j/movie/reviewers?titre=The Matrix
```
**Paramètres Query :**
- `titre` (string, requis) : Nom du film

---

#### 5. Informations utilisateur (Neo4j)
```http
GET /neo4j/user/{user_name}
```
**Retourne :**
```json
{
  "name": "Nom de l'utilisateur",
  "nombre_de_films_notes": 5,
  "liste_films_notes": ["Film 1", "Film 2", "..."]
}
```

---

#### 6. Films communs MongoDB & Neo4j
```http
GET /neo4j/common-movies-count
```
**Retourne :**
```json
{
  "nb_films_communs": 42,
  "liste_films_communs": ["Film 1", "Film 2", "..."]
}
```

---

## ⚙️ Installation et Configuration

### Prérequis

- Python 3.10 ou supérieur
- pip (gestionnaire de paquets Python)
- Accès internet (pour MongoDB Atlas et Neo4j Sandbox)

### 1. Cloner le projet

```bash
git clone <url-du-repo>
cd Final_Lab_Project
```

### 2. Créer un environnement virtuel

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

Si le fichier `requirements.txt` n'existe pas, installez manuellement :

```bash
pip install fastapi uvicorn pymongo neo4j pydantic
```

### 4. Configuration des bases de données

#### MongoDB Atlas
L'application utilise **MongoDB Atlas** avec la base de données `sample_mflix` (collection `movies`).

> Les identifiants de connexion sont déjà configurés dans `backend_api/databases/mongodb.py`.

#### Neo4j Sandbox
L'application utilise **Neo4j Sandbox/Aura** avec le dataset de films.

> Les identifiants de connexion sont déjà configurés dans `backend_api/databases/neo4j.py`.

---

## 🚀 Exécution de l'Application

### Démarrer le serveur

```bash
cd backend_api
python main.py
```

Ou avec uvicorn directement :

```bash
uvicorn backend_api.main:backend --reload --host 127.0.0.1 --port 8000
```

L'API sera disponible sur : **http://127.0.0.1:8000**

---

## 📚 Documentation API (Swagger)

FastAPI génère automatiquement une documentation interactive :

| Interface | URL |
|-----------|-----|
| **Swagger UI** | http://127.0.0.1:8000/docs |
| **ReDoc** | http://127.0.0.1:8000/redoc |
| **OpenAPI JSON** | http://127.0.0.1:8000/openapi.json |

---

## 🧪 Tests

### Tester avec cURL

```bash
# Test endpoint racine
curl http://127.0.0.1:8000/

# Lister les films
curl http://127.0.0.1:8000/films/

# Rechercher un film
curl "http://127.0.0.1:8000/films/recherche?film=Titanic"

# Films communs
curl http://127.0.0.1:8000/neo4j/common-movies-count
```

### Tester avec le navigateur

Accéder directement à **http://127.0.0.1:8000/docs** pour utiliser l'interface Swagger interactive.

---

## 📝 Notes Importantes

- **MongoDB Atlas** : Utilise la base de données `sample_mflix` qui contient le dataset de films MongoDB.
- **Neo4j Sandbox** : Utilise le dataset Movie Graph avec les relations `REVIEWED`.
- **Pagination** : L'endpoint `/films/` supporte la pagination via `pageInitial` et `pageLimite`.
- **Recherche insensible à la casse** : Les recherches de films et acteurs sont insensibles à la casse.

---

## 👥 Auteur

- **Antoine Boquien**
- **Azdine Froukh**
- **Lucas Bardelang**
- **Antonin Urbain**
---

## 📄 Licence

Ce projet est réalisé dans le cadre du projet final NoSQL.