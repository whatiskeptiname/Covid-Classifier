# main.py
import os
from skimage import feature  # for image feature extraction
import cv2
import pickle
from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import shutil

app = FastAPI()

origins = [
    'http://localhost:3000',
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/predict")
async def root(file: UploadFile):
    file_name = os.getcwd()+"/results/"+file.filename
    with open(file_name, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    label = disease_predict(file.filename)
    return {"class": label}

svc = pickle.load(open("./models/svc.pkl", "rb"))
disease_types = ["Covid", "Normal"]

def disease_predict(file_name):
    path = file_name
    full_path = "D:\Covid-Classifier\datasets\images/" + path
    img_data = cv2.imread(full_path)
    img_data = cv2.cvtColor(img_data, cv2.COLOR_BGR2GRAY)
    img_data = cv2.resize(img_data, (100, 100), interpolation=cv2.INTER_AREA)
    img_data = cv2.cvtColor(img_data, cv2.COLOR_BGR2RGB)
    hog_data = feature.hog(img_data, multichannel=True) / 255.0
    disease_type_predict = svc.predict(hog_data.reshape(1, -1))
    return disease_types[disease_type_predict[0]]

    # uvicorn main:app --reload