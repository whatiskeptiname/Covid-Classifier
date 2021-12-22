# not completed error in image upload

from numpy.core.numeric import full
from skimage import feature  # for image feature extraction
from PIL import Image
import cv2
import numpy as np
import pickle
import streamlit as st


svc = pickle.load(open("./models/svc.pkl", "rb"))

disease_types = ["covid", "normal"]


def disease_predict(uploaded_file):
    path = uploaded_file.name
    full_path = (
        "/home/susang/Documents/sunyata/self/Python/Covid_Classifier/datasets/images/"
        + path
    )
    img_data = cv2.imread(full_path)
    img_data = cv2.cvtColor(img_data, cv2.COLOR_BGR2GRAY)
    print("-----------------------------------------------")
    print(img_data)
    print("-----------------------------------------------")

    img_data = cv2.resize(img_data, (100, 100), interpolation=cv2.INTER_AREA)
    img_data = cv2.cvtColor(img_data, cv2.COLOR_BGR2RGB)
    hog_data = feature.hog(img_data) / 255.0
    disease_type_predict = svc.predict(hog_data.reshape(1, -1))
    return disease_types[disease_type_predict[0]]


st.title("Covid Classifier")

uploaded_file = st.file_uploader("Choose an image...", type="png")
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True, clamp=True)
    st.write("")
    st.write("Classifying...")
    label = disease_predict(uploaded_file)
    st.write(label)
