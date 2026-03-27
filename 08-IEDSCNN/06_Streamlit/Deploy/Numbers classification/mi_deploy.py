import streamlit as st
import numpy as np
from PIL import Image
import tensorflow as tf

# TITLE RENDER
st.title("Desplegar un Modelo")

# Model Lader
model = tf.keras.models.load_model('model_to_dep.keras')

# FILE Uploaded
uploaded_file = st.file_uploader(label="Carga una TaR34", type=["png", "jpg", "jpeg"])

def bild_bearbeiten(datei):
    bild = datei.resize((28, 28))
    bild_array = np.array(bild)
    bild_array = bild_array/225

    # bild array reshape
    # .............................(1 [y no -1] por que solo se sube un 1 bild a la vez)
    bild_array = bild_array.reshape(-1,28 * 28)
    return bild_array




if uploaded_file is not None:
    bild = Image.open(uploaded_file).convert("L")
    st.image(bild, caption="File uploaded", use_container_width=True)

    # bild bearbeitung
    re = bild_bearbeiten(bild)

    # vorhersagen treffen
    response = model.predict(re)
    classe = np.argmax(response)
    st.write(response)
    st.write(classe)
else:
    st.text("Desplegar un Modelo")