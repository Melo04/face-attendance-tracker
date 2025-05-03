from pymongo import MongoClient
import torch
from PIL import Image
from facenet_pytorch import MTCNN, InceptionResnetV1
import os
from dotenv import load_dotenv

load_dotenv()

mtcnn = MTCNN(image_size=160, margin=20, keep_all=False)
facenet = InceptionResnetV1(pretrained='vggface2').eval()

uri = os.getenv("MONGODB_CONNECTION")
client = MongoClient(uri)
database = client["hackathon"]
collection = database["embedded_person"]

def extract_embedding(embedding):
    with torch.no_grad():
        embedding = facenet(embedding)
    return embedding.squeeze().tolist()


def run_capture(embedding_2):
    try:
        # embedding_2 = extract_embedding(embedding)
        if embedding_2:
            query_vector = embedding_2

            pipeline = [
                {
                    "$vectorSearch": {
                        "queryVector": query_vector,
                        "path": "embeddings",
                        "numCandidates": 100,
                        "limit": 1,
                        "index": "face_vector_index"
                    }
                }
            ]

            results = list(collection.aggregate(pipeline))
            
            print(f"Query results for the new image:")
            # for result in results:
            # print(results[0]['name'])
            return results[0]['name']

        client.close()

    except Exception as e:
        raise Exception(
            "The following error occurred: ", e
        )
