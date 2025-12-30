from pymongo import MongoClient

URI_MONGO = "mongodb+srv://antoineboquien1_db_user:XNoMIkLiyonG4tLM@clusterfinallab.pdq5zsd.mongodb.net/"

client = MongoClient(URI_MONGO)
databases = client.get_database("sample_mflix")

films = databases["movies"]


