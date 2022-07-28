# Kevin Hwang, 7/28/2022
import streamlit as st
import pandas as pd
import plotly.express as px
import firebase_admin
from firebase_admin import db, credentials

st.set_page_config(page_icon=":bar_chart", page_title="888 Attendance Stats", layout="centered")
print("Set Page Config")


@st.experimental_singleton
def init_firebase(s):
    # s is a dummy variable that will make the experimental singleton only run once
    # do NOT remove s

    cred = credentials.Certificate({
        "type": st.secrets.type,
        "project_id": st.secrets.project_id,
        "private_key_id": st.secrets.private_key_id,
        "private_key": st.secrets.private_key,
        "client_email": st.secrets.client_email,
        "client_id": st.secrets.client_id,
        "auth_uri": st.secrets.auth_uri,
        "token_uri": st.secrets.token_uri,
        "auth_provider_x509_cert_url": st.secrets.auth_provider_x509_cert_url,
        "client_x509_cert_url": st.secrets.client_x509_cert_url
    })
    firebase_admin.initialize_app(cred, {
        'databaseURL': "https://robotiatorsattendance-default-rtdb.firebaseio.com"
    })


if "jsonData" not in st.session_state:

    try:
        with st.spinner("Collecting our data..."):
            init_firebase("initApp")
            ref = db.reference('/Log')
            st.session_state.jsonData = ref.get()

    except Exception as e:
        print(e)
        st.error(e)
        st.stop()

st.title("Team 888's Attendance")

df = pd.DataFrame(st.session_state.jsonData).transpose()
# Bar chart of attendance

totalHourFig = px.bar(df, x="Name", y="Hours")
st.plotly_chart(totalHourFig)

# Stats
# Blank expander + already expanded makes it look like a box
with st.expander("", expanded=True):
    st.subheader("Quick stats")

    col1, col2, col3 = st.columns(3)

    try:
        col1.metric("Mean Hours", round(df["Hours"].mean(skipna=True), 2))
        col1.metric("Number of members", int(df.count()["Name"]))

        col2.metric("Median Hours", round(df["Hours"].median(skipna=True), 2))

        try:
            col2.metric("Members actively working", int(df['LoggedIn'].value_counts()["True"]))
        except KeyError:
            col2.metric("Members actively working", 0)  # No one logged in

        col3.metric("Standard Deviation", round(df["Hours"].std(skipna=True), 2))
        col3.metric("Total Hours", round(df["Hours"].sum(skipna=True), 2))

    except TypeError:
        st.error("Data is poorly formatted. Cannot load stats")

        