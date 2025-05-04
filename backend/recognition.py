import cv2
import torch
from facenet_pytorch import MTCNN, InceptionResnetV1
import torchvision.transforms as transforms
from PIL import Image
import time
import os
from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

# Setup
classifier = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
mtcnn = MTCNN(image_size=160, margin=20, keep_all=False)
facenet = InceptionResnetV1(pretrained='vggface2').eval()

# Connect to MongoDB once
uri = os.getenv("MONGODB_CONNECTION")
client = MongoClient(uri)
db = client["hackathon"]
collection = db["embedded_person"]

def capture_video():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()

    while True:
        ret, frame = cap.read()
        dst = frame.copy()
     
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break

        faces = detect_bouncing_box(frame, dst)
        cv2.imshow('face_detection', dst)

        if len(faces) > 0:
            time.sleep(3)

        if cv2.waitKey(1) == ord('q'):
            break
     
    cap.release()
    cv2.destroyAllWindows()
    client.close()

def detect_bouncing_box(frame, dst):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = classifier.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=10, minSize=(80, 80))

    for (x, y, w, h) in faces:
        cv2.rectangle(dst, (x, y), (x + w, y + h), (255, 0, 0), 2)
        cropped_face = frame[y:y+h, x:x+w]
        embedding = generate_embeddings(cropped_face)
        print("Generated embedding:", embedding[:5])
        names = search_mongodb(embedding)
        update_mongodb(names)

    return faces

def generate_embeddings(face_img):
    transform = transforms.Compose([
        transforms.Resize((160, 160)),
        transforms.ToTensor(),
        transforms.Normalize([0.5], [0.5])
    ])

    face_pil = Image.fromarray(cv2.cvtColor(face_img, cv2.COLOR_BGR2RGB))
    face_tensor = transform(face_pil).unsqueeze(0)

    with torch.no_grad():
        embedding = facenet(face_tensor)
    return embedding.squeeze(0).tolist()

def search_mongodb(query_vector):
    try:
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

        names = []
        results = list(collection.aggregate(pipeline))

        for i in results:
            print(f"Detected: {i['name']}")
            names.append(i['name'])
        return names

    except Exception as e:
        print("MongoDB query error:", e)

def update_mongodb(names):
    try:
        uri = os.getenv("MONGODB_CONNECTION")
        client = MongoClient(uri)
        
        database = client["hackathon"]
        collection = database["attendance"]

        for name in names:
            query_filter = {'attendees': name}
            result = collection.update_one(
                {"date": datetime.now()},
                {"$push": {"attendees": name}}
            )
            print(f"Updated attendance: {result}")

        client.close()
    except Exception as e:
        raise Exception(
            f"The following error occurred: {e}", e
        )

