from pymongo import MongoClient
import numpy as np
from facenet_pytorch import MTCNN, InceptionResnetV1
from PIL import Image
import torch
import os
from dotenv import load_dotenv

load_dotenv()
# get facenet model
mtcnn = MTCNN(image_size=160, margin=20, keep_all=False)
facenet = InceptionResnetV1(pretrained='vggface2').eval()

image = Image.open('./members/IMG_20250503_153211.jpg').convert('RGB')
face_tensor = mtcnn(image)

if face_tensor is not None:
    face_tensor = face_tensor.unsqueeze(0)
    with torch.no_grad():
        embedding = facenet(face_tensor)
    vector = embedding.squeeze().tolist()

try:
    uri = os.getenv("MONGODB_CONNECTION")
    client = MongoClient(uri)
    
    database = client["hackathon"]
    collection = database["embedded_person"]

    document = {
        "name": "Lee Wei Xuan",
        "embeddings": vector,
    }

    result = collection.insert_one(document)
    print("Inserted:", result.acknowledged)

    client.close()
except Exception as e:
    raise Exception(
        "The following error occurred: ", e
    )