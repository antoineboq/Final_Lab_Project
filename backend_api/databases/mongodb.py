from pymongo import MongoClient

URI_MONGO = " "

client = MongoClient(URI_MONGO)
databases = client.get_database("sample_mflix")

films = databases["movies"]


