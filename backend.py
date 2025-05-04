import os
from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import JSONResponse
from pymongo import MongoClient
from dotenv import load_dotenv
from facenet_pytorch import MTCNN, InceptionResnetV1
import torch

from recognition import capture_video

load_dotenv()
app = FastAPI()

def get_embeddings(image):
    mtcnn = MTCNN(image_size=160, margin=20, keep_all=False)
    facenet = InceptionResnetV1(pretrained='vggface2').eval()
    face_tensor = mtcnn(image)

    if face_tensor is not None:
        face_tensor = face_tensor.unsqueeze(0)
        with torch.no_grad():
            embedding = facenet(face_tensor)
        vector = embedding.squeeze().tolist()
        return vector
    else:
        raise ValueError

@app.post("/user")
async def post_new_user(file: UploadFile = File(...), name: str = Form(...)):
    try:
        uri = os.getenv("MONGODB_CONNECTION")
        client = MongoClient(uri)
        
        database = client["hackathon"]
        collection = database["embedded_person"]
        print(f"getting file: {file}")
        vector = get_embeddings(file.filename)
        print(f"getting embeddings: {vector}")

        document = {
            "name": name,
            "embeddings": vector,
            "attendance": 1,
        }

        result = collection.insert_one(document)
        print("Inserted:", result.acknowledged)

        client.close()

        return JSONResponse(
            content={"message": "Successfully added new name"}, status_code=200,
        )
    except Exception as e:
        raise Exception(
            f"The following error occurred: {e}", e
        )
    
@app.get("/leaderboard")
async def get_leaderboard():
    try:
        uri = os.getenv("MONGODB_CONNECTION")
        client = MongoClient(uri)
        
        database = client["hackathon"]
        collection = database["embedded_person"]

        results = collection.find({}, {"_id": 0, "name": 1, "attendance": 1})
        leaderboard = list(results)

        client.close()

        return JSONResponse(
            content={"leaderboard": leaderboard},
            status_code=200
        )
    except Exception as e:
        raise Exception(
            f"The following error occurred: {e}", e
        )

@app.get("/camera")
async def get_camera():
    capture_video()