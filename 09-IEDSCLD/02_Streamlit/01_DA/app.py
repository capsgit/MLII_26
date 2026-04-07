# Dashboard 
# Dynamic Dashboard  
# 
# 
# > streamlit run app.py
# >
# 

import os 
from pathlib import Path 
import streamlit as st 
import pandas as pd 


os.chdir(Path(__file__).parent)


#########################################
# Get the whole DataFrame
########################################


df = pd.read_csv("./dataset.csv")


#########################################
# Web Page
########################################
st.title(":chart_with_upwards_trend: Area Price Dashboard")





#########################################
# Side Bar
########################################
st.sidebar.header("Filter the data")


area = st.sidebar.multiselect(
    "Select the Area",
    options=df["area"].unique(), # values 
    default=df["area"].unique() # selected values as default
)


roomcount = st.sidebar.multiselect(
    "Select the Room Count",
    options=df["roomcount"].unique(), # values 
    default=df["roomcount"].unique() # selected values as default
)


# Get the spefific Rows from the whole dataset 
df_selected = df.query("area == @area & roomcount == @roomcount")




#########################################
# Aggregations / Infos
########################################

total_area = df_selected["area"].sum() 
avg_price = round(df_selected["price"].mean(), 2) 
message = "Very good price" 


left_col, middle_col, right_col = st.columns(3)

with left_col:
    st.subheader("Total Area")
    st.subheader(f"{total_area} m²")

with middle_col:
    st.subheader("Average Price")
    st.subheader(f"{avg_price}€")

with right_col:
    st.subheader("Price Evaluation")
    st.subheader(message)


#########################################
# Show the DataFrame
########################################


st.markdown("## :file_folder: Data Table")

# Show the DataFrame 
st.dataframe(df_selected)