from pymongo import MongoClient
import torch
from PIL import Image
from facenet_pytorch import MTCNN, InceptionResnetV1
import os
from dotenv import load_dotenv

load_dotenv()

mtcnn = MTCNN(image_size=160, margin=20, keep_all=False)
facenet = InceptionResnetV1(pretrained='vggface2').eval()

def extract_embedding(image_path):
    image = Image.open(image_path).convert('RGB')
    face_tensor = mtcnn(image)
    
    if face_tensor is not None:
        face_tensor = face_tensor.unsqueeze(0)
        with torch.no_grad():
            embedding = facenet(face_tensor)
        return embedding.squeeze().tolist()
    else:
        print(f"No face detected in {image_path}.")
        return None

try:
    uri = os.getenv("MONGODB_CONNECTION")
    client = MongoClient(uri)
    
    database = client["hackathon"]
    collection = database["embedded_person"]

    embedding_2 = extract_embedding('./members/IMG_20250503_165057.jpg')
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
        for result in results:
            print(result)

    client.close()

except Exception as e:
    raise Exception(
        "The following error occurred: ", e
    )