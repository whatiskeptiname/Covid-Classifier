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
def root(file: UploadFile):
    path = os.getcwd()+"/results/"+file.filename
    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    label = disease_predict(path)
    return {"class": label}

svc = pickle.load(open("./models/svc.pkl", "rb"))
disease_types = ["Covid", "Normal"]

def disease_predict(path):
    img_data = cv2.imread(path)
    img_data = cv2.cvtColor(img_data, cv2.COLOR_BGR2GRAY)
    img_data = cv2.resize(img_data, (100, 100), interpolation=cv2.INTER_AREA)
    img_data = cv2.cvtColor(img_data, cv2.COLOR_BGR2RGB)
    hog_data = feature.hog(img_data, multichannel=True) / 255.0
    disease_type_predict = svc.predict(hog_data.reshape(1, -1))
    probability=svc.predict_proba(hog_data.reshape(1, -1))
    array=[disease_types[disease_type_predict[0]]]
    for ind, _ in enumerate(disease_types):
        print( f'{probability[0][ind]*100}')
        array.append(f'{probability[0][ind]*100}')
  
    return array

    # uvicorn main:app --reload