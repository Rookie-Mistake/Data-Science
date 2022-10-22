from distutils.log import error
import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

st.title("Most interations on chat - Whatsup")

#File Upload
st.subheader("Import file")
raw_file = st.file_uploader("Upload Whatsup Chat File")

#File Manipulation
if raw_file and "text" in raw_file.type:

    st.success("Upload Successful")
    
    date = []
    time = []
    sender_message = []
    while True:
        line = raw_file.readline().decode("utf-8")
        if len(line) < 1:
            break
        date.append(line[:8])
        sender_message.append(line[18:])
        
    dict_file = {"date":date, "sender_message":sender_message}    


    df = pd.DataFrame(dict_file)

    df["sender"] = df["sender_message"].str.split(":", 1, expand=True)[0]
    df["message"] = df["sender_message"].str.split(":", 1, expand=True)[1]
    df_final = df.drop("sender_message", axis=1)

    df_final["date"] = pd.to_datetime(df_final["date"], format="%d/%m/%y", errors="coerce").dt.strftime('%d-%m-%Y')

    df_final = df_final.dropna()

    st.markdown("""---""")

    #Show Table
    st.subheader("Disply data")
    #col1, col2, col3, col4, col5, col6, col7 = st.columns(7)

    #with col2:
    #    head = st.button("Head")
    #with col4:
    #    tail = st.button("Tail")
    #with col6:
    #    total = st.button("Total")

    #if head:
    #    st.table(df_final.head())
    #if tail:
    #    st.table(df_final.tail())
    #if total:
    #    st.table(df_final)

    rows = st.slider("Select row quantity", min_value=1, max_value=100)
    rev = st.checkbox("Reverse")

    if rev:
        st.table(df_final.tail(rows))
    else:
        st.table(df_final.head(rows))

    