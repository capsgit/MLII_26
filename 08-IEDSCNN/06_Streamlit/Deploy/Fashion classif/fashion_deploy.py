import streamlit as st
import numpy as np
from PIL import Image
import tensorflow as tf

# TITLE RENDER
st.title("Cloth-reconizer")

# Model Lader
model = tf.keras.models.load_model('fashion_model.keras')

# FILE Uploaded
uploaded_file = st.file_uploader(label="Carga una fot de una prenda", type=["png", "jpg", "jpeg"])

def bild_bearbeiten(datei):
    bild = datei.resize((28, 28))
    bild_array = np.array(bild)
    bild_array = bild_array.astype("float32")/255
    # bild array reshape
    # .............................(1 [y no -1] por que solo se sube un 1 bild a la vez)
    bild_array = bild_array.reshape(-1,28,28,1)
    return bild_array


class_names = [
    "T-shirt/top",
    "Trouser",
    "Pullover",
    "Dress",
    "Coat",
    "Sandal",
    "Shirt",
    "Sneaker",
    "Bag",
    "Ankle boot"
]

if uploaded_file is not None:
    bild = Image.open(uploaded_file).convert("L")
    st.image(bild, caption="File uploaded", use_container_width=True)

    # bild bearbeitung
    re = bild_bearbeiten(bild)

    # vorhersagen treffen
    response = model.predict(re)
    pred_idx = np.argmax(response)
    pred_label = class_names[pred_idx]
    confidence = response[0][pred_idx]

    st.subheader("Predicción")
    st.write(f"Clase predicha: **{pred_label}**")
    st.write(f"Confianza: **{confidence:.2%}**")
else:
    st.text("Desplegar un Modelo")