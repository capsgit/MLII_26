import streamlit as st

# Create Title
st.title("Holis, acà un -> streamlit App")
st.title("1. Display Text")

# Create a Header
st.header("soy un HEADER")


# Create a subheader
st.subheader(" yo soy tu padre-subheader")

st.text("me encanta el tEXT")

st.markdown("hola markDown")


st.latex(r''' e^{i\pi} + 1 = 0 ''')

st.write('Most Objects')

st.code("""
    experience = [1,2,3,4,5,6,7,8],
    data_scientists_salary = [65000, 92000, 126570, 400000, 900000, 657530, 890000, 500000],
    genders = ['Men','Women','Men','Women','Men','Men','Women','Men']
""")

st.caption("hola markDown jbasd ahsbdj ahdsfahdslknahdbf adsfjadfbadvf kjdbfjhb d,jmvbahdf,jksdbfabvdsffmsdbvjfhakjdfcbhdvbsf f dajkjadf khfuklas hdfjhbvdajkfgadh fjkbadfhjghadfhjdsavfkjba vhjkagvfkh dhjfv jkdhfbjd vhf FIN")


st.sidebar.title("Sidebar")

with st.sidebar:
    option = st.selectbox("escoge una opcion", ["Opc. 1", "Opc 2", "Opc 3", "Opc 4", "Opc 5", "Opc 6"])

    if st.button("Click me"):
        st.write("El Boton ha sido cliqueado")

    st.checkbox('Checkbox 1')
    st.checkbox('Checkbox 2', value=True)

    state = st.checkbox('Checkbox 3')  # [True False]

    if state:
        st.write('Hi')


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~
st.header('Display data')
st.text('Create a sample DataFrame')

import pandas as pd
my_datafarme = pd.DataFrame(
    {
        'Name': ['Maria','David','Mona'],
        'Age':[23,45,67],
        'city':'Berlin'
    }
)

st.dataframe(my_datafarme)
st.text("Aca una tabla")
st.table(my_datafarme)

st.text("Aca un .json")
st.json(
    {
        'Name': ['Maria','David','Mona'],
        'Age':[23,45,67],
        'city':'Berlin'
    }
)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~

st.header('Display Media')
st.text('Display a sample Image')
from pathlib import Path
from PIL import Image
import streamlit as st

BASE_DIR = Path(__file__).resolve().parents[2]

img_path = BASE_DIR / "Transfer Lerning" / "Transfer_Learning_VGG" / "dataset"

img_3 = Image.open(str(img_path)+  "/" + "cat_or_dog_3.png")
img_4 = Image.open(str(img_path)+  "/" + "cat_or_dog_4.png")
img_5 = Image.open(str(img_path)+  "/" + "cat_or_dog_5.png")

st.image(img_3, use_column_width=True)


st.header('Create Columns')

col1, col2 = st.columns(2)

col1.write('This is the first Column')
col2.write('This is the second Column')

with col1:
    st.image(img_4, use_container_width='always')

with col2:
    st.image(img_5)

st.subheader('Three Columns with different width')
col1, col2, col3 = st.columns([3, 2, 1])

with col1:
    st.image(img_3, use_container_width=True)

with col2:
    st.image(img_4, use_container_width=True)

with col3:
    st.image(img_5, use_container_width=True)


# Create Tabs
st.header('Display Tabs')
tab1, tab2, tab3 = st.tabs(["hola", "medio", "chao"])

with tab1:
    st.radio('Select one: ', [1, 2])


tab1.write('This is tab 1')
tab2.write('This is tab 2')

st.header('Group multiple Widgets')

with st.form(key='my_Form'):
    username = st.text_input('Username')
    password = st.text_input('Password')
    st.form_submit_button('Login')

# Show a spinner during a process
import time

with st.spinner(text='In progress'):
    time.sleep(8)
    st.success('Done')

    # Show and update progress bar
bar = st.progress(50)
time.sleep(10)
bar.progress(100)

