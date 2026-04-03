import streamlit as st
import pandas as pd
from groq import Groq
import plotly.express as px
import graphviz
from datetime import date
from streamlit_camera_input_live import camera_input_live
import os

st.set_page_config(page_title="AI Classroom Platform", layout="wide")

st.title("🎓 AI Classroom System")

# API
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# Sidebar menu
menu = st.sidebar.radio(
    "Select Module",
    [
        "AI Chatbot",
        "Mobile Attendance",
        "Attendance Dashboard",
        "ML Diagram Generator"
    ]
)

# ---------------- AI CHATBOT ----------------

if menu == "AI Chatbot":

    st.header("🤖 AI Tutor")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    prompt = st.chat_input("Ask your ML question")

    if prompt:

        st.session_state.messages.append(
            {"role":"user","content":prompt}
        )

        with st.chat_message("user"):
            st.write(prompt)

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=st.session_state.messages
        )

        reply = response.choices[0].message.content

        with st.chat_message("assistant"):
            st.write(reply)

        st.session_state.messages.append(
            {"role":"assistant","content":reply}
        )

# ---------------- MOBILE ATTENDANCE ----------------

if menu == "Mobile Attendance":

    st.header("📱 Mobile Attendance")

    df = pd.read_csv("students.csv")

    reg = st.selectbox("Select Register Number", df["Register"])

    photo = camera_input_live()

    if photo:

        st.image(photo)

    if st.button("Mark Attendance"):

        today = date.today()

        data = pd.DataFrame({
            "Register":[reg],
            "Date":[today]
        })

        if os.path.exists("attendance.csv"):
            data.to_csv("attendance.csv",mode="a",header=False,index=False)
        else:
            data.to_csv("attendance.csv",index=False)

        st.success("Attendance Marked")

# ---------------- DASHBOARD ----------------

if menu == "Attendance Dashboard":

    st.header("📊 Attendance Analytics")

    if os.path.exists("attendance.csv"):

        data = pd.read_csv("attendance.csv")

        summary = data.groupby("Register").count()

        fig = px.bar(summary,y="Date")

        st.plotly_chart(fig)

        st.dataframe(data)

        st.download_button(
            "Download Attendance",
            data.to_csv(index=False),
            "attendance.csv"
        )

    else:
        st.info("No attendance data")

# ---------------- ML DIAGRAM ----------------

if menu == "ML Diagram Generator":

    st.header("📈 Machine Learning Diagram")

    algo = st.selectbox(
        "Select Algorithm",
        ["Decision Tree","Neural Network","K-Means"]
    )

    dot = graphviz.Digraph()

    if algo == "Decision Tree":

        dot.node("A","Root")
        dot.node("B","Feature < 5")
        dot.node("C","Class A")
        dot.node("D","Class B")

        dot.edges(["AB","BC","BD"])

    if algo == "Neural Network":

        dot.node("I1","Input")
        dot.node("H1","Hidden")
        dot.node("O","Output")

        dot.edges([("I1","H1"),("H1","O")])

    if algo == "K-Means":

        dot.node("A","Data")
        dot.node("B","Cluster 1")
        dot.node("C","Cluster 2")

        dot.edges([("A","B"),("A","C")])

    st.graphviz_chart(dot)
