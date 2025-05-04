import time
from pymongo import MongoClient
from pymongo.operations import SearchIndexModel
import os
from dotenv import load_dotenv

load_dotenv()

try:
    uri = os.getenv("MONGODB_CONNECTION")
    client = MongoClient(uri)
    
    database = client["hackathon"]
    collection = database["embedded_person"]

    search_index_model = SearchIndexModel(
    definition={
        "fields": [
            {
                "type": "vector",
                "numDimensions": 512,
                "path": "embeddings",
                "similarity": "cosine"
            }
        ]
    },
        name="face_vector_index",
        type="vectorSearch"
    )
    result = collection.create_search_index(model=search_index_model)
    print("New search index named " + result + " is building.")

    print("Polling to check if the index is ready. This may take up to a minute.")
    predicate=None
    if predicate is None:
        predicate = lambda index: index.get("queryable") is True
    while True:
        indices = list(collection.list_search_indexes(result))
        if len(indices) and predicate(indices[0]):
            break
        time.sleep(5)
    print(result + " is ready for querying.")
    client.close()

except Exception as e:
    raise Exception(
        "The following error occurred: ", e
    )