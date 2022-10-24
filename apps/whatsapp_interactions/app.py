import pandas as pd
import streamlit as st
import plotly.express as px

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

    df_final["date"] = pd.to_datetime(df_final["date"], format="%d/%m/%y", errors="coerce")#.dt.strftime('%d-%m-%Y')

    df_final = df_final.dropna()

    st.markdown("""---""")

    #Data Info

    st.subheader("Data Info")

    col1, col2 = st.columns([2, 2])

    with col1:
        st.write(f"**First Date:** {df_final.date.iloc[0].strftime('%d-%m-%Y')}")
        st.write(f"**Number of messages:** {df_final.shape[0]}")
    with col2:
        st.write(f"**Last Message:** {df_final.date.iloc[-1].strftime('%d-%m-%Y')}")
        st.write(f"**Number of Participants:** {len(list(df_final.sender.unique()))}")
    st.write(f"**Participants:** {list(df_final.sender.unique())}")

    ###Show EDA
    st.subheader("Analysis")

    #Date Range
    st.write("Date Range:")

    col3, col4 = st.columns([2, 2])

    with col3:
        initial_date = st.date_input("Pick the initial date", min_value=df_final.date.head(1)[0], value=df_final.date.head(1)[0])

    with col4:
        final_date = st.date_input("Pick the final date", min_value=df_final.date.head(1)[0])

    tab1, tab2, tab3 = st.tabs(["📊 Bar Chart", "📈 Moving Averages", "🗃 Data"])

    df_filter = df_final[(df_final["date"] >= str(initial_date)) & (df_final["date"] <= str(final_date))]
    
    df_bar = df_filter.sender.value_counts().reset_index()

    #create plot
    fig = px.bar(df_bar,
                x="index",
                y="sender",
                text_auto='.2s',
                title="Number of interations",
                labels={"sender":"Interactions", "index":"Participants"},
                height=500)

    fig.update_xaxes(tickangle=90)

    #display plot
    tab1.plotly_chart(fig, use_container_width=True)


    #Moving Averages    
    rolling_average = tab2.slider("Moving Average", min_value=1, max_value=60)

    f = lambda x: x.shift().rolling(rolling_average).mean()
    
    temp = df_filter.copy()
    temp["count_val"] = 1
    frac = temp.groupby(["date", "sender"])["count_val"].sum().reset_index()
    frac["SMA"] = frac.groupby('sender')['count_val'].transform(f)
    frac = frac.dropna()

    #plot line chart
    line_fig = px.line(frac,
                        x="date",
                        y="SMA",
                        color="sender",
                        labels={"SMA":f"SMA {rolling_average}", "date":"Date", "sender":"Participant"},
                        title="Moving Average for each participant")

    tab2.plotly_chart(line_fig, use_container_width=True)

    #table tab
    rows = tab3.slider("Select row quantity", min_value=1, max_value=100, value=5)
    rev = tab3.checkbox("Reverse")

    df_filter["date"] = df_filter["date"].dt.strftime('%d-%m-%Y')

    if rev:
        tab3.table(df_filter.tail(rows))
    else:
        tab3.table(df_filter.head(rows))